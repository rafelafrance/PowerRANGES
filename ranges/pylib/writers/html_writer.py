import dataclasses
import html
import itertools
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import jinja2

COLOR_COUNT = 15
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])

TEMPLATE_DIR: Path = Path.cwd() / "ranges/pylib/writers/templates"
TEMPLATE: str = "html_writer.html"


@dataclasses.dataclass
class SummaryCounts:
    total: int = 0
    with_traits: int | str = 0


@dataclasses.dataclass(kw_only=True)
class HtmlWriterRow:
    occurrence_id: str
    source: str
    info_fields: dict[str, str]
    formatted_text: dict[str, str] = dataclasses.field(default_factory=dict)
    overwrite_fields: dict[str, str] = dataclasses.field(default_factory=dict)


class CssClasses:
    def __init__(self):
        self.classes = {}

    def __getitem__(self, key):
        if key not in self.classes:
            self.classes[key] = next(BACKGROUNDS)
        return self.classes[key]


def write_html(
    html_file: Path,
    occurrences: list[dict[str, Any]],
    id_field: str,
    summary_field: str = "",
) -> None:
    css_classes = CssClasses()

    formatted = [
        HtmlWriterRow(
            occurrence_id=occur[id_field],
            source=occur["source"],
            info_fields=occur["info_fields"],
            formatted_text=format_text(occur, css_classes),
            overwrite_fields=format_overwrite_field(occur, css_classes),
        )
        for occur in occurrences
    ]

    write_template(occurrences, html_file, formatted, summary_field)


def write_template(
    occurrences: list[dict[str, Any]],
    html_file: Path,
    formatted: list[HtmlWriterRow],
    summary_field: str,
):
    species_count = summary_by_field(occurrences, summary_field)
    trait_count = summary_by_trait(occurrences)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
        autoescape=True,
    )

    template = env.get_template(TEMPLATE).render(
        now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
        file_name=html_file.stem,
        rows=formatted,
        species_count=species_count,
        summary_field=summary_field,
        trait_count=trait_count,
    )

    with html_file.open("w") as html_file:
        html_file.write(template)


def format_overwrite_field(occur: dict[str, Any], css_classes: CssClasses):
    formatted_text = {}
    for name, raw_text in occur["overwrite_fields"].items():
        cls = css_classes[name]
        text = f'<span class="{cls}" title="This {name} value gets passed thru">'
        text += html.escape(raw_text)
        text += "</span>"
        formatted_text[name] = text
    return formatted_text


def format_text(occur: dict[str, Any], css_classes: CssClasses) -> dict[str, str]:
    formatted_text = {}
    for field, raw_text in occur["parse_fields"].items():
        traits = [t for t in occur["traits"] if t["_field"] == field]
        text = format_text_fields(raw_text, traits, css_classes)
        formatted_text[field] = text
    return formatted_text


def format_text_fields(
    raw_text: str, traits: list[dict[str, any]], css_classes: CssClasses
) -> str:
    """Wrap traits in the text with <spans> that can be formatted with CSS."""
    frags = defaultdict(lambda: {"raw": "", "cls": "", "title": []})
    prev = 0

    for trait in traits:
        start = trait["_start"]
        end = trait["_end"]

        if prev < start:
            frags[(prev, start)]["raw"] = raw_text[prev:start]

        frags[(start, end)]["raw"] = raw_text[start:end]
        frags[(start, end)]["cls"] = css_classes[trait["_trait"]]

        title = [f"{k} {v}" for k, v in trait.items() if not k.startswith("_")]
        title = f"{trait['_trait']}:" + ", ".join(title)
        frags[(start, end)]["title"].append(title)

        prev = end

    if len(raw_text) > prev:
        frags[(prev, len(raw_text))]["raw"] = raw_text[prev:]

    text = []
    for frag in frags.values():
        if frag["cls"]:
            title = "; ".join(frag["title"])
            cls = frag["cls"]
            text.extend(
                (
                    f'<span class="{cls}" title="{title}">',
                    html.escape(frag["raw"]),
                    "</span>",
                )
            )
        else:
            text.append(html.escape(frag["raw"]))

    text = "".join(text)
    return text


def summary_by_field(
    occurrences: list[dict[str, Any]], summary_field: str
) -> dict[str, SummaryCounts]:
    if not summary_field:
        return {}

    counts = defaultdict(lambda: SummaryCounts())

    for occur in occurrences:
        name = occur["info_fields"].get(summary_field, "").strip()
        counts[name].total += 1
        counts[name].with_traits += 1 if occur["traits"] else 0

    counts = dict(sorted(counts.items()))
    counts["Total"] = SummaryCounts(
        total=len(occurrences),
        with_traits=sum(c.with_traits for c in counts.values()),
    )

    return counts


def summary_by_trait(occurrences: list[dict[str, Any]]) -> dict[str, int]:
    counts = defaultdict(int)

    for occur in occurrences:
        for trait in occur["traits"]:
            counts[trait["_trait"]] += 1

    counts = dict(sorted(counts.items()))
    counts["Total"] = sum(c for c in counts.values())

    return counts
