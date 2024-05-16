#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.occurrences import Occurrences
from pylib.writers import html_writer
from util.pylib import log


def main():
    log.started()
    args = parse_args()

    if args.html_dir:
        args.html_dir.mkdir(parents=True, exist_ok=True)

    if args.csv_dir:
        args.csv_dir.mkdir(parents=True, exist_ok=True)

    tsv_files = sorted(args.tsv_dir.glob("*"))
    for path in tsv_files:
        print(path.name)
        occurrences = Occurrences(
            path, args.id_field, args.parse_field, args.info_field
        )
        occurrences.parse()

        if args.html_dir:
            write_html(args.html_dir, path, occurrences, args.sample)

        break

    log.finished()


def write_html(html_dir: Path, path: Path, occurrences: Occurrences, sample: int):
    html_file = html_dir / f"{path.stem}.html"
    writer = html_writer.HtmlWriter(html_file)
    writer.write(occurrences, sample)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract information about vertebrates from GBIF TSV data dumps.
            """,
        ),
    )

    arg_parser.add_argument(
        "--tsv-dir",
        metavar="DIR",
        type=Path,
        required=True,
        help="""Get input TSV files from this directory.""",
    )

    arg_parser.add_argument(
        "--csv-dir",
        metavar="DIR",
        type=Path,
        help="""Put output CSV files into this directory.""",
    )

    arg_parser.add_argument(
        "--html-dir",
        metavar="DIR",
        type=Path,
        help="""Put output CSV files into this directory.""",
    )

    arg_parser.add_argument(
        "--id-field",
        metavar="COLUMN",
        help="""Use this field as the record ID.""",
    )

    arg_parser.add_argument(
        "--parse-field",
        metavar="COLUMN",
        action="append",
        help="""Parse this field.""",
    )

    arg_parser.add_argument(
        "--info-field",
        metavar="COLUMN",
        action="append",
        help="""Include, but don't parse_fields, this field in the output.""",
    )

    arg_parser.add_argument(
        "--sample",
        metavar="INT",
        type=int,
        help="""Randomly sample this many records from each input file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
