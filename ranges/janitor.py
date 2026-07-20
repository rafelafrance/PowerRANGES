#!/usr/bin/env python3
import argparse
import csv
import logging
import textwrap
from glob import glob
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from ranges.janitors.anourosorex_yamashinai_mod import AnourosorexYamashinaiMod
from ranges.janitors.antrozous_pallidus_mod import AntrozousPallidusMod
from ranges.janitors.cas_y1_y2_trait_data_only import CasY1Y2TraitDataOnly
from ranges.janitors.csulb_sciuridae_traits import CsulbSciuridaeTraits
from ranges.janitors.dmns_ranges_traits_dmns import DmnsRangesTraits
from ranges.janitors.eptesicus_mod import EptesicusMod
from ranges.janitors.fmnh_test_ranges_traits import (
    FmnhTestRangesTraits,
    fmnh_multi_row_cleaner,
)
from ranges.janitors.lacm_ranges_specimens_updated_new_data_dec2025 import (
    LACMRangesSpecimensUpdatedNewDataDec2025,
)
from ranges.janitors.microtus_mod import MicrotusMod
from ranges.janitors.msb_y1_y2_traits_mod import MsbY1Y2TraitsMod
from ranges.janitors.mustela_mod import MustelaMod
from ranges.janitors.myosorex_varius_mod import MyosorexVariusMod
from ranges.janitors.myotis_mod import MyotisMod
from ranges.janitors.neotoma_mod import NeotomaMod
from ranges.janitors.notiosorex_crawfordi_mod import NotiosorexCrawfordiMod
from ranges.janitors.peromyscus_master import PeromyscusMaster
from ranges.janitors.reithrodontomys_mod import ReithrodontomysMod
from ranges.janitors.sorex_master import SorexMaster
from ranges.pylib import log

CSVS = {
    "Anourosorex_yamashinai_mod.csv": (AnourosorexYamashinaiMod,),
    "Antrozous pallidus_mod.csv": (AntrozousPallidusMod,),
    "CAS Y1&Y2 Trait Data Only (1).csv": (CasY1Y2TraitDataOnly,),
    "CSULB_Sciuridae_Traits.csv": (CsulbSciuridaeTraits,),
    "DMNS_Ranges_Traits_DMNS_Y1_mod.csv": (DmnsRangesTraits,),
    "DMNS_Ranges_Traits_DMNS_Y2_mod.csv": (DmnsRangesTraits,),
    "Eptesicus_mod.csv": (EptesicusMod,),
    "FMNH_Test_Ranges_Traits (1).csv": (FmnhTestRangesTraits, fmnh_multi_row_cleaner),
    "LACM_Ranges_specimens_updated_new_data_Dec2025.csv": (
        LACMRangesSpecimensUpdatedNewDataDec2025,
    ),
    "Microtus_mod.csv": (MicrotusMod,),
    "MSB-Y1-Y2-traits_mod.csv": (MsbY1Y2TraitsMod,),
    "mustela_mod.csv": (MustelaMod,),
    "Myosorex_varius_mod.csv": (MyosorexVariusMod,),
    "Myotis_mod.csv": (MyotisMod,),
    "Neotoma_mod.csv": (NeotomaMod,),
    "Notiosorex_crawfordi_mod.csv": (NotiosorexCrawfordiMod,),
    "Peromyscus_Master.csv": (PeromyscusMaster,),
    "Reithrodontomys_mod.csv": (ReithrodontomysMod,),
    "Sorex_Master.csv": (SorexMaster,),
    "Soriculus_Master.csv": None,
    "Suncus_Master.csv": None,
    "Tamias speciosus_mod.csv": None,
    "TAMU_RANGESALL_TraitsOnly2Sept2025_mod.csv": None,
    "Thomomys bottae_mod.csv": None,
    "TTU-NSF-Ranges-Data Corrections Next to Data-7-28-2025_mod.csv": None,
    "UMMZ_ranges_y2_final_mod.csv": None,
    "UWBM_Mamm_JSON_Attributes.csv": None,
    "UWYMZ_Y1_mod.csv": None,
    "UWYMZ_Y2_mod.csv": None,
}


def main(args: argparse.Namespace) -> None:
    log.started()

    # args.output_dir.mkdir(parents=True, exist_ok=True)
    # to_csv(args)

    for name, janitor in CSVS.items():
        if not janitor:
            continue
        logging.info(name)

        janitor_class = janitor[0]

        cleaner = janitor[1] if len(janitor) > 1 else per_row_cleaner

        in_name = args.csv_dir / name

        with in_name.open() as in_csv:
            reader = csv.DictReader(in_csv)
            dirty = [dict(r) for r in reader]

        cleaned = cleaner(dirty, janitor_class)

        df = pd.DataFrame(cleaned)
        path = args.output_dir / name
        df.to_csv(path, index=False)

    log.finished()


def per_row_cleaner(dirty: list[dict], janitor_class: Any) -> list[dict]:
    cleaned = []
    for row in tqdm(dirty):
        janitor = janitor_class(dirty=row)
        janitor.cleaner()
        cleaned.append(janitor.clean)
    return cleaned


def to_csv(args: argparse.Namespace) -> None:
    args.csv_dir.mkdir(parents=True, exist_ok=True)
    for path in args.glob:
        logging.info(f"Converting {path}")
        df = pd.read_csv(path) if path.suffix == ".csv" else pd.read_excel(path)
        out_csv = args.csv_dir / f"{path.stem}.csv"
        df.to_csv(out_csv, index=False)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            Normalize data from previous extractions.

            All happy datasets are alike;
            each unhappy dataset is unhappy in its own way.
            """
        ),
    )

    arg_parser.add_argument(
        "--glob",
        required=True,
        action="append",
        metavar="GLOB",
        help="""Input this CSV. Wild cards must be quoted""",
    )

    arg_parser.add_argument(
        "--csv-dir",
        required=True,
        metavar="PATH",
        type=Path,
        help="""Store CSV files to this directory.""",
    )

    arg_parser.add_argument(
        "--output-dir",
        required=True,
        metavar="PATH",
        type=Path,
        help="""Output files to this directory.""",
    )

    args = arg_parser.parse_args()

    all_paths = []
    for path in args.glob:
        paths = glob(path)  # noqa: PTH207
        all_paths += paths
    args.glob = [Path(f) for f in sorted(all_paths)]

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    main(ARGS)
