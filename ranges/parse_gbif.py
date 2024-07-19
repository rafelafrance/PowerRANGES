#!/usr/bin/env python3
import argparse
import json
import logging
import multiprocessing
import os
import tempfile
import textwrap
from contextlib import contextmanager
from glob import glob
from pathlib import Path

from pylib.occurrence import sample_occurrences
from pylib.writers import csv_writer, html_writer, json_writer
from tqdm import tqdm
from util.pylib import log


def main():  # noqa: C901
    log.started()
    args = parse_args()

    if args.json_dir:
        args.json_dir.mkdir(parents=True, exist_ok=True)

    if args.output_dir:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    with get_json_dir(args.json_dir) as json_dir:
        if not args.skip_parse:
            if args.debug:
                single_process(args, json_dir)
            else:
                multiple_processes(args, json_dir)

        logging.info("Reading JSONL data.")
        by_institution = {}
        for path in sorted(args.json_dir.glob("*.jsonl")):
            msg = "Reading JSONL for " + path.stem
            logging.info(msg)
            with path.open() as jin:
                data = [json.loads(ln) for ln in jin]
            by_institution[path.stem] = data

    all_occurrences = []
    if args.csv_all or args.csv_sampled or args.html_all:
        for data in by_institution.values():
            all_occurrences += data

    if args.csv_institution and args.output_dir:
        logging.info("Writing institution CSV files.")
        for name, occurrence in by_institution.items():
            msg = "Institution CSV for " + name
            logging.info(msg)
            csv_writer.write_csv(
                args.output_dir / f"{name}.csv",
                occurrence,
                args.id_field,
                args.info_field,
                args.parse_field,
            )

    if args.csv_sampled and args.output_dir:
        logging.info("Writing sampled CSV file.")
        sampled = sample_occurrences(
            all_occurrences, args.csv_sample, args.sample_method
        )
        csv_writer.write_csv(
            args.output_dir / f"all_occurrences_sampled_{len(sampled)}.csv",
            sampled,
            args.id_field,
            args.info_field,
            args.parse_field,
        )

    if args.csv_all and args.output_dir:
        logging.info("Writing big CSV file.")
        csv_writer.write_csv(
            args.output_dir / "all_occurrences.csv",
            all_occurrences,
            args.id_field,
            args.info_field,
            args.parse_field,
        )

    if args.html_institution and args.output_dir:
        logging.info("Writing institution HTML files.")
        for name, occurrences in by_institution.items():
            msg = "Institution HTML for " + name
            logging.info(msg)
            sampled = sample_occurrences(
                occurrences, args.csv_sample, args.sample_method
            )
            html_writer.write_html(
                args.output_dir / f"sampled_{len(sampled)}_{name}.html",
                sampled,
                args.id_field,
                args.summary_field,
            )

    if args.html_all and args.output_dir:
        logging.info("Writing HTML file.")
        sampled = sample_occurrences(
            all_occurrences, args.csv_sample, args.sample_method
        )
        html_writer.write_html(
            args.output_dir / f"all_occurrences_sampled_{len(sampled)}.html",
            sampled,
            args.id_field,
            args.summary_field,
        )

    log.finished()


def single_process(args, json_dir):
    for tsv in tqdm(args.tsv_file):
        json_writer.process_occurrences(
            tsv,
            json_dir,
            args.id_field,
            args.info_field,
            args.parse_field,
            args.overwrite_field,
        )


def multiple_processes(args, json_dir):
    with tqdm(total=len(args.tsv_file)) as bar:
        with multiprocessing.Pool(processes=args.cpus) as pool:
            results = [
                pool.apply_async(
                    json_writer.process_occurrences,
                    args=(
                        tsv,
                        json_dir,
                        args.id_field,
                        args.info_field,
                        args.parse_field,
                        args.overwrite_field,
                    ),
                    callback=lambda _: bar.update(1),
                )
                for tsv in args.tsv_file
            ]
            fails = ", ".join([val for r in results if (val := r.get())])

    if fails:
        msg = f"The following extractions did not work: {fails}"
    else:
        msg = "All files parsed successfully."

    logging.info(msg)


@contextmanager
def get_json_dir(json_dir=None):
    dir_ = json_dir if json_dir else tempfile.mkdtemp()
    try:
        yield dir_
    finally:
        pass


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
        "--output-dir",
        metavar="PATH",
        type=Path,
        help="""Output files to this directory.""",
    )

    arg_parser.add_argument(
        "--csv-all",
        action="store_true",
        help="""Output all occurrences to a single CSV file.""",
    )

    arg_parser.add_argument(
        "--csv-sampled",
        action="store_true",
        help="""Output sampled occurrences to a CSV file.""",
    )

    arg_parser.add_argument(
        "--csv-institution",
        action="store_true",
        help="""Output institution occurrences to individual CSV files.""",
    )

    arg_parser.add_argument(
        "--html-all",
        action="store_true",
        help="""Output all occurrences (sampled) to a single HTML file.""",
    )

    arg_parser.add_argument(
        "--html-institution",
        action="store_true",
        help="""Output institution occurrences (sampled) to individual HTML files.""",
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
        "--csv-sample",
        type=int,
        default=10000,
        metavar="INT",
        help="""How many records to output for the sampled CSV report.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--html-sample",
        type=int,
        default=1000,
        metavar="INT",
        help="""How many records to output for the HTML reports.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--sample-method",
        choices=["fields", "traits"],
        default="traits",
        help="""How to sample the data for HTML output. "fields"=Sample records with
            any data in the parse fields. "traits"=Sample records with parsed traits
            "fields" is better at finding false negatives, and "traits" is better at
            false positives. (default: %(default)s)""",
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
        help="""This is here so that you may use prebuilt JSON files to output
            a CSV or HTML reports. Parsing can take a while.""",
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
