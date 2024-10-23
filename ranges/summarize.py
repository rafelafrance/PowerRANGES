#!/usr/bin/env python3
import argparse
import json
import logging
import textwrap
from pathlib import Path

from pylib.writers import summary_writer
from util.pylib import log


def main():
    log.started()
    args = parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Reading JSONL data.")
    by_institution = {}
    all_occurrences = []

    for path in sorted(args.json_dir.glob("*.jsonl")):
        msg = "Reading JSONL for " + path.stem
        logging.info(msg)
        with path.open() as jin:
            data = [json.loads(ln) for ln in jin]
        by_institution[path.stem] = data
        all_occurrences += data

    logging.info("Writing institution CSV files.")
    for name, occurrence in by_institution.items():
        msg = "Writing CSV for " + name
        logging.info(msg)
        summary_writer.write_summary(
            args.output_dir / f"{name}.csv",
            occurrence,
            args.summarize_by,
        )

    logging.info("Summarize all data.")
    summary_writer.write_summary(
        args.output_dir / "summarize_all.csv",
        all_occurrences,
        args.summarize_by,
    )

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Summarize information about vertebrates from GBIF.""",
        ),
    )

    arg_parser.add_argument(
        "--json-dir",
        metavar="PATH",
        type=Path,
        help="""Read JSON parses from this directory.""",
    )

    arg_parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Output files to this directory.""",
    )

    arg_parser.add_argument(
        "--summarize-by",
        metavar="COLUMN",
        default="scientificName",
        help="""Summarize counts by this field.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
