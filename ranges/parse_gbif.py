#!/usr/bin/env python3

import argparse
import textwrap
from pathlib import Path

from pylib.occurrences import Occurrences
from pylib.writers import csv_writer, html_writer
from util.pylib import log


def main():
    log.started()
    args = parse_args()

    if args.html_dir:
        args.html_dir.mkdir(parents=True, exist_ok=True)

    if args.csv_dir:
        args.csv_dir.mkdir(parents=True, exist_ok=True)

    tsv_files = sorted(args.tsv_dir.glob("*"))
    for input_tsv in tsv_files:
        print(input_tsv.name)
        occurrences = Occurrences(
            path=input_tsv,
            id_field=args.id_field,
            info_fields=args.info_field,
            parse_fields=args.parse_field,
            summary_field=args.summary_field,
            sample=args.sample,
        )
        occurrences.parse()

        if args.html_dir:
            write_html(args.html_dir, input_tsv, occurrences)

        if args.csv_dir:
            write_csv(args.csv_dir, input_tsv, occurrences)

    log.finished()


def write_html(html_dir: Path, input_tsv: Path, occurrences: Occurrences) -> None:
    html_file = html_dir / f"{input_tsv.stem}.html"
    writer = html_writer.HtmlWriter(html_file)
    writer.write(occurrences)


def write_csv(csv_dir: Path, input_tsv: Path, occurrences: Occurrences) -> None:
    csv_file = csv_dir / f"{input_tsv.stem}.csv"
    writer = csv_writer.CsvWriter(csv_file)
    writer.write(occurrences)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Extract information about vertebrates from GBIF TSV data dumps.""",
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
        "--summary-field",
        metavar="COLUMN",
        help="""Summarize counts of this field.""",
    )

    arg_parser.add_argument(
        "--sample",
        type=int,
        metavar="INT",
        help="""How many records to output for the HTML report.""",
    )

    args = arg_parser.parse_args()

    if args.summary_field and args.summary_field not in args.info_field:
        args.info_field.append(args.summary_field)

    return args


if __name__ == "__main__":
    main()
