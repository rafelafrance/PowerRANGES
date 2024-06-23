import dataclasses

# import html
import itertools

# import random
# from datetime import datetime
from pathlib import Path

# import jinja2
# from traiter.pylib.darwin_core import DarwinCore
#
# from ranges.pylib.occurrence import Occurrence
# from ranges.pylib.rules.base import Base

COLOR_COUNT = 15
BACKGROUNDS = itertools.cycle([f"cc{i}" for i in range(COLOR_COUNT)])

TEMPLATE_DIR: Path = Path.cwd() / "ranges/pylib/writers/templates"
TEMPLATE: str = "html_writer.html"


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


# class HtmlWriter:
#
#     def __init__(self, html_file):
#         self.html_file = html_file
#         self.css_classes = CssClasses()
#         self.formatted = []


# def write_html(merged):
#     # Limit output to rows with data in any of the parse fields
#     with_data = [o for o in occurrences.occurrences if o.has_parse]
#
#     # Limit the occurrences to the sample size
#     if occurrences.sample and len(with_data) > occurrences.sample:
#         with_data = random.sample(with_data, occurrences.sample)
#
#     # Output formatted rows
#     for occur in with_data:
#         self.formatted.append(
#             HtmlWriterRow(
#                 occurrence_id=occur.occurrence_id,
#                 source=occur.source,
#                 info_fields=occur.info_fields,
#                 formatted_text=self.format_text(occur),
#                 overwrite_fields=self.format_overwrite_field(occur),
#             ),
#         )
#
#     self.write_template(occurrences=occurrences)


# def write_template(self, occurrences):
#     species_count = occurrences.summary_by_field()
#     trait_count = occurrences.summary_by_trait()
#
#     env = jinja2.Environment(
#         loader=jinja2.FileSystemLoader(self.template_dir),
#         autoescape=True,
#     )
#
#     template = env.get_template(self.template).render(
#         now=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"),
#         file_name=self.html_file.stem,
#         rows=self.formatted,
#         species_count=species_count,
#         summary_field=occurrences.summary_field,
#         trait_count=trait_count,
#     )
#
#     with self.html_file.open("w") as html_file:
#         html_file.write(template)
#
#
# def format_overwrite_field(self, occur):
#     formatted_text = {}
#     for name, raw_text in occur.overwrite_fields.items():
#         cls = self.css_classes[name]
#         text = f'<span class="{cls}" title=f"This {name} value gets passed thru">'
#         text += html.escape(raw_text)
#         text += "</span>"
#         formatted_text[name] = text
#     return formatted_text
#
#
# def format_text(self, occurrence: Occurrence) -> dict[str, str]:
#     formatted_text = {}
#     for name, raw_text in occurrence.parse_fields.items():
#         traits = occurrence.traits.get(name)
#         text = self.format_text_field(raw_text, traits)
#         formatted_text[name] = text
#     return formatted_text
#
#
# def format_text_field(self, raw_text: str, traits: list[Base]):
#     """Wrap traits in the text with <spans> that can be formatted with CSS."""
#     frags = []
#     prev = 0
#
#     if traits:
#         for trait in traits:
#             start = trait.start
#             end = trait.end
#
#             if prev < start:
#                 frags.append(html.escape(raw_text[prev:start]))
#
#             cls = self.css_classes[trait.key]
#
#             dwc = DarwinCore()
#             dwc = trait.to_dwc(dwc).flatten()
#
#             title = ", ".join(f"{k}:&nbsp;{v}" for k, v in dwc.items())
#
#             frags.extend(
#                 (
#                     f'<span class="{cls}" title="{title}">',
#                     html.escape(raw_text[start:end]),
#                     "</span>",
#                 )
#             )
#             prev = end
#
#     if len(raw_text) > prev:
#         frags.append(html.escape(raw_text[prev:]))
#
#     text = "".join(frags)
#     return text


# def summary_by_field(self) -> dict[str, SummaryCounts]:
#     if not self.summary_field:
#         return {}
#
#     if self._summary_by_field is None:
#         counts = defaultdict(lambda: SummaryCounts())
#
#         for occur in self.occurrences:
#             name = occur.info_fields.get(self.summary_field, "").strip()
#             counts[name].total += 1
#             counts[name].with_traits += 1 if occur.has_traits else 0
#
#         counts = dict(sorted(counts.items()))
#         counts["Total"] = SummaryCounts(
#             total=len(self.occurrences),
#             with_traits=sum(c.with_traits for c in counts.values()),
#         )
#         self._summary_by_field = counts
#
#     return self._summary_by_field

# def summary_by_trait(self) -> dict[str, int]:
#     if self._summary_by_trait is None:
#         counts = defaultdict(int)
#
#         for occur in self.occurrences:
#             for trait in occur.all_traits:
#                 counts[trait[0]] += 1
#
#         counts = dict(sorted(counts.items()))
#         counts["Total"] = sum(c for c in counts.values())
#         self._summary_by_trait = counts
#
#     return self._summary_by_trait
