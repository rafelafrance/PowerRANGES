#!/usr/bin/env python3
import argparse
import logging
import multiprocessing
import os
import tempfile
import textwrap
from contextlib import contextmanager
from glob import glob
from pathlib import Path

import pandas as pd
from pylib.writers import csv_writer, html_writer
from tqdm import tqdm
from util.pylib import log


def main():
    log.started()
    args = parse_args()

    if args.csv_dir and not args.csv_dir.exists():
        args.csv_dir.mkdir(parents=True, exist_ok=True)

    with get_csv_dir(args.csv_dir) as csv_dir:
        if args.debug:
            single_process(args, csv_dir)
        else:
            multiple_processes(args, csv_dir)

        merged = sorted([pd.read_csv(f) for f in csv_dir.glob("*.csv")])
        merged = pd.concat(merged, axis="rows")

        if args.csv_file:
            merged.to_csv(args.csv_file, index=False)

        if args.html_file:
            html_writer.write_html(merged)

    log.finished()


def single_process(args, csv_dir):
    if args.skip_parse:
        return

    for tsv in tqdm(args.tsv_file):
        csv_writer.process_occurrences(
            tsv,
            csv_dir,
            args.id_field,
            args.info_field,
            args.parse_field,
            args.overwrite_field,
        )


def multiple_processes(args, csv_dir):
    if args.skip_parse:
        return

    with tqdm(total=len(args.tsv_file)) as bar:
        with multiprocessing.Pool(processes=args.cpus) as pool:
            results = [
                pool.apply_async(
                    csv_writer.process_occurrences,
                    args=(
                        tsv,
                        csv_dir,
                        args.id_field,
                        args.info_field,
                        args.parse_field,
                        args.overwrite_field,
                    ),
                    callback=lambda _: bar.update(1),
                )
                for tsv in args.tsv_file
            ]
            fails = ", ".join(r.get() for r in results)

    if fails:
        msg = f"The following extractions did not work: {fails}"
    else:
        msg = "All files parsed successfully."

    logging.info(msg)


@contextmanager
def get_csv_dir(csv_dir=None):
    dir_ = csv_dir if csv_dir else tempfile.mkdtemp()
    try:
        yield dir_
    finally:
        pass


# def write_html(html_dir: Path, occurrences: list[Occurrence]) -> None:
#     html_file = html_dir / f"{tsv_file.stem}.html"
#     writer = html_writer.HtmlWriter(html_file)
#     writer.write(occurrences)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Extract information about vertebrates from GBIF TSV data dumps.""",
        ),
    )

    arg_parser.add_argument(
        "--tsv-file",
        type=Path,
        action="append",
        required=True,
        metavar="PATH",
        help="""Get input this TSV. Wild cards must be quoted""",
    )

    arg_parser.add_argument(
        "--json-dir",
        metavar="PATH",
        type=Path,
        help="""Put JSON parses into this directory. If this is not used a temporary
            directory gets created.""",
    )

    arg_parser.add_argument(
        "--csv-file",
        metavar="PATH",
        type=Path,
        help="""Output occurrences into this CSV file.""",
    )

    arg_parser.add_argument(
        "--html-file",
        metavar="PATH",
        type=Path,
        help="""Output sampled occurrences into this HTML file.""",
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
        "--overwrite-field",
        metavar="COLUMN",
        action="append",
        help="""Use this field as is if it has data otherwise use a parsed field.""",
    )

    arg_parser.add_argument(
        "--summary-field",
        metavar="COLUMN",
        help="""Summarize counts of this field.""",
    )

    arg_parser.add_argument(
        "--sample",
        type=int,
        default=1000,
        metavar="INT",
        help="""How many records to output for the HTML reports. Only used if
            --html-file is selected. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--sample-method",
        choices=["records", "traits"],
        default="records",
        help="""How to sample the data for HTML output. This only used if --html-file
            is selected. records=Sample records with any data in the parse fields.
            traits=Sample records with parsed traits. (default: %(default)s)""",
    )

    keep = 4
    cpus = min(10, os.cpu_count() - keep if os.cpu_count() > keep else 1)
    arg_parser.add_argument(
        "--cpus",
        type=int,
        default=cpus,
        help=f"""Number of CPU processors to use.
            Default will use {cpus} out of {os.cpu_count()} CPUs.
            """,
    )

    arg_parser.add_argument(
        "--debug",
        action="store_true",
        help="""Runs extractions in a single process for debugging purposes.
            Note that multiple processes sometimes hang while printing to stderr or
            stdout.""",
    )

    arg_parser.add_argument(
        "--skip-parse",
        action="store_true",
        help="""This is here so that you may use prebuilt CSV files to output
            a final CSV or HTML report. Parsing can take a while.""",
    )

    args = arg_parser.parse_args()

    if args.summary_field and args.summary_field not in args.info_field:
        args.info_field.append(args.summary_field)

    tsv_file = []
    for tsv in args.tsv_file:
        tsv_file += glob(str(tsv))  # noqa: PTH207
    args.tsv_file = [Path(f) for f in sorted(tsv_file)]

    return args


if __name__ == "__main__":
    main()
