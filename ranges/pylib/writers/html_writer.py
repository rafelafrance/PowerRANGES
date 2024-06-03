import dataclasses
import html
import itertools
import random
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import ClassVar

import jinja2
from traiter.pylib.darwin_core import DarwinCore

from ranges.pylib.occurrences import Occurrence, Occurrences
from ranges.pylib.rules.base import Base

COLOR_COUNT = 15
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])


@dataclasses.dataclass(kw_only=True)
class HtmlWriterRow:
    occurrence_id: str
    info_fields: dict[str, str]
    formatted_text: dict[str, str] = dataclasses.field(default_factory=dict)


class CssClasses:
    def __init__(self, spotlight: str = ""):
        self.classes = {}
        self.spotlight = spotlight

    def __getitem__(self, key):
        if self.spotlight and key.find(self.spotlight) > -1:
            return "ccx"
        if key not in self.classes:
            self.classes[key] = next(BACKGROUNDS)
        return self.classes[key]


@dataclasses.dataclass
class SpeciesCount:
    total: int = 0
    with_traits: int | str = 0


class HtmlWriter:
    template_dir: ClassVar[Path] = Path.cwd() / "ranges/pylib/writers/templates"
    template: ClassVar[str] = "html_writer.html"

    def __init__(self, html_file, spotlight=""):
        self.html_file = html_file
        self.css_classes = CssClasses(spotlight)
        self.formatted = []

    def write(self, occurrences: Occurrences):
        species_count = defaultdict(lambda: SpeciesCount())
        trait_count = defaultdict(int)

        with_data = []

        with_traits = 0

        for occur in occurrences.occurrences:
            has_traits = 1 if occur.has_traits else 0
            with_traits += has_traits

            # Calculate per trait counts
            for trait in occur.all_traits:
                trait_count[trait._trait] += 1

            if occur.has_parse:
                with_data.append(occur)

            if occurrences.summary_field:
                name = occur.info_fields.get(occurrences.summary_field, "").strip()
                species_count[name].total += 1
                species_count[name].with_traits += has_traits

        trait_count = dict(sorted(trait_count.items()))
        trait_count["Grand total"] = sum(c for c in trait_count.values())

        species_count = dict(sorted(species_count.items()))

        species_count["Total"] = SpeciesCount(
            total=len(occurrences.occurrences), with_traits=with_traits
        )

        if occurrences.sample:
            if len(with_data) > occurrences.sample:
                with_data = random.sample(with_data, occurrences.sample)
            species_count["Output limit"] = SpeciesCount(
                total=len(with_data), with_traits=""
            )

        for occur in with_data:
            self.formatted.append(
                HtmlWriterRow(
                    occurrence_id=occur.occurrence_id,
                    info_fields=occur.info_fields,
                    formatted_text=self.format_text(occur),
                ),
            )

        self.write_template(
            species_count=species_count,
            summary_field=occurrences.summary_field,
            trait_count=trait_count,
        )

    def format_text(self, occurrence: Occurrence) -> dict[str, str]:
        formatted_text = {}
        for name, raw_text in occurrence.parse_fields.items():
            traits = occurrence.traits.get(name)
            text = self.format_text_field(raw_text, traits)
            formatted_text[name] = text
        return formatted_text

    def format_text_field(self, raw_text: str, traits: list[Base]):
        """Wrap traits in the text with <spans> that can be formatted with CSS."""
        frags = []
        prev = 0

        if traits:
            for trait in traits:
                start = trait.start
                end = trait.end

                if prev < start:
                    frags.append(html.escape(raw_text[prev:start]))

                cls = self.css_classes[trait.key]

                dwc = DarwinCore()
                dwc = trait.to_dwc(dwc).flatten()

                title = ", ".join(f"{k}:&nbsp;{v}" for k, v in dwc.items())

                frags.extend(
                    (
                        f'<span class="{cls}" title="{title}">',
                        html.escape(raw_text[start:end]),
                        "</span>",
                    )
                )
                prev = end

        if len(raw_text) > prev:
            frags.append(html.escape(raw_text[prev:]))

        text = "".join(frags)
        return text

    def write_template(self, species_count=None, summary_field=None, trait_count=None):
        species_count = species_count if species_count else {}
        trait_count = trait_count if trait_count else {}

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True,
        )

        template = env.get_template(self.template).render(
            now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
            file_name=self.html_file.stem,
            rows=self.formatted,
            species_count=species_count,
            summary_field=summary_field,
            trait_count=trait_count,
        )

        with self.html_file.open("w") as html_file:
            html_file.write(template)
