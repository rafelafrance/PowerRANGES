import dataclasses
import html
import itertools
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, NamedTuple

import jinja2
from traiter.pylib.darwin_core import DYN, DarwinCore
from traiter.pylib.rules.base import Base

from ranges.pylib.occurrences import Occurrence, Occurrences

COLOR_COUNT = 14
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])


class TraitRow(NamedTuple):
    label: str
    data: Any


class Sortable(NamedTuple):
    key: str
    start: int
    dwc: str
    title: str


@dataclasses.dataclass(kw_only=True)
class HtmlWriterRow:
    occurrence_id: str
    info_fields: dict[str, str]
    formatted_text: dict[str, str] = dataclasses.field(default_factory=dict)
    formatted_traits: dict[str, list[Sortable]] = dataclasses.field(
        default_factory=dict
    )


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


class HtmlWriter:
    template_dir: ClassVar[Path] = Path.cwd() / "ranges/pylib/writers/templates"
    template: ClassVar[str] = "html_writer.html"

    def __init__(self, html_file, spotlight=""):
        self.html_file = html_file
        self.css_classes = CssClasses(spotlight)
        self.formatted = []

    @staticmethod
    def has_traits(occurrences: Occurrences) -> list[Occurrence]:
        with_traits = [
            o for o in occurrences.occurrences if any(len(v) for v in o.traits.values())
        ]
        return with_traits

    def write(self, occurrences: Occurrences, sample: int):
        with_traits = self.has_traits(occurrences)
        trait_count = len(with_traits)
        if sample:
            with_traits = with_traits[:sample]

        for occur in with_traits:
            self.formatted.append(
                HtmlWriterRow(
                    occurrence_id=occur.occurrence_id,
                    info_fields=occur.info_fields,
                    formatted_text=self.format_text(occur),
                    formatted_traits=self.format_traits(occur),
                ),
            )

        summary = {
            "Total occurrences:": len(occurrences.occurrences),
            "With traits": trait_count,
            "Sampled": len(with_traits),
        }

        self.write_template(summary=summary)

    def format_text(self, occurrence: Occurrence) -> dict[str, str]:
        formatted_text = {}
        for name, raw_text in occurrence.parse_fields.items():
            traits = occurrence.traits.get(name)
            text = self.format_text_field(raw_text, traits) if traits else ""
            formatted_text[name] = text
        return formatted_text

    def format_text_field(self, raw_text: str, traits: list[Base]):
        """Wrap traits in the text with <spans> that can be formatted with CSS."""
        frags = []
        prev = 0

        for trait in traits:
            start = trait.start
            end = trait.end

            if prev < start:
                frags.append(html.escape(raw_text[prev:start]))

            cls = self.css_classes[trait.key]

            dwc = DarwinCore()
            dwc = trait.to_dwc(dwc).to_dict()

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

    def format_traits(self, occurrence: Occurrence) -> dict[str, Any]:
        formatted_traits = {}
        for name, raw_text in occurrence.parse_fields.items():
            if traits := occurrence.traits.get(name):
                text = self.format_trait_field(raw_text, traits)
                formatted_traits[name] = text
        return formatted_traits

    def format_trait_field(self, raw_text: str, traits: list[Base]):
        """Group traits for display in their own table."""
        formatted = []

        sortable = []
        for trait in traits:
            dwc = DarwinCore()
            sortable.append(
                Sortable(
                    key=trait._trait,
                    start=trait.start,
                    dwc=trait.to_dwc(dwc),
                    title=raw_text[trait.start : trait.end],
                ),
            )

        sortable = sorted(sortable)

        for key, grouped in itertools.groupby(sortable, key=lambda x: x.key):
            cls = self.css_classes[key]
            label = f'<span class="{cls}">{key}</span>'
            trait_list = []
            for trait in grouped:
                fields = {}
                dwc_dict = trait.dwc.to_dict()
                for k, v in dwc_dict.items():
                    fields = v if k == DYN else dwc_dict
                fields = ", ".join(
                    f'<span title="{trait.title}">{k}:&nbsp;{v}</span>'
                    for k, v in fields.items()
                )
                if fields:
                    trait_list.append(fields)

            if trait_list:
                formatted.append(
                    TraitRow(label, '<br/><hr class="sep"/>'.join(trait_list)),
                )

        return formatted

    def write_template(self, summary=None):
        summary = summary if summary else {}
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True,
        )

        template = env.get_template(self.template).render(
            now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
            file_name=self.html_file.stem,
            rows=self.formatted,
            summary=summary,
        )

        with self.html_file.open("w") as html_file:
            html_file.write(template)