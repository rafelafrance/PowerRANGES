#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from util.pylib import log


def main():
    log.started()
    # args = parse_args()

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract information about vertebrates from GBIF data dumps, zip files
            containing several TSVs.
            """,
        ),
    )

    arg_parser.add_argument(
        "--zip-file",
        metavar="PATH",
        type=Path,
        required=True,
        help="""Zip file containing GBIF TSV data dumps.""",
    )

    arg_parser.add_argument(
        "--output-csv",
        metavar="PATH",
        type=Path,
        help="""Output the results to this CSV file.""",
    )

    arg_parser.add_argument(
        "--limit",
        type=int,
        help="""Only extract this many records.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
