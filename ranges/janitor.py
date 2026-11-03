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

from ranges.janitors.lacm_ranges_specimens_updated_new_data_dec2025 import (
    LACMRangesSpecimensUpdatedNewDataDec2025,
)
from ranges.janitors.tamu_ranged_all_traits_only_2sept2025_mod import (
    TamuRangesAllTraitsOnly2Sept2025Mod,
)
from ranges.pylib import log

CSVS = {
    # "Anourosorex_yamashinai_mod.csv": (AnourosorexYamashinaiMod,),
    # "Antrozous pallidus_mod.csv": (AntrozousPallidusMod,),
    # "CAS Y1&Y2 Trait Data Only (1).csv": (CasY1Y2TraitDataOnly,),
    # "CSULB_Sciuridae_Traits.csv": (CsulbSciuridaeTraits,),
    # "DMNS_Ranges_Traits_DMNS_Y1_mod.csv": (DmnsRangesTraits,),
    # "DMNS_Ranges_Traits_DMNS_Y2_mod.csv": (DmnsRangesTraits,),
    # "Eptesicus_mod.csv": (EptesicusMod,),
    # "FMNH_Test_Ranges_Traits (1).csv": (FmnhTestRangesTraits, fmnh_multi_row_cleaner),
    "LACM_Ranges_specimens_updated_new_data_Dec2025.csv": (
        LACMRangesSpecimensUpdatedNewDataDec2025,
    ),
    # "Microtus_mod.csv": (MicrotusMod,),
    # "MSB-Y1-Y2-traits_mod.csv": (MsbY1Y2TraitsMod,),
    # "mustela_mod.csv": (MustelaMod,),
    # "Myosorex_varius_mod.csv": (MyosorexVariusMod,),
    # "Myotis_mod.csv": (MyotisMod,),
    # "Neotoma_mod.csv": (NeotomaMod,),
    # "Notiosorex_crawfordi_mod.csv": (NotiosorexCrawfordiMod,),
    # "Peromyscus_Master.csv": (PeromyscusMaster,),
    # "Reithrodontomys_mod.csv": (ReithrodontomysMod,),
    # "Sorex_Master.csv": (SorexMaster,),
    # "Soriculus_Master.csv": (SoriculusMaster,),
    # "Suncus_Master.csv": (SuncusMaster,),
    # "Tamias speciosus_mod.csv": (TamiasSpeciosusMod,),
    "TAMU_RANGESALL_TraitsOnly2Sept2025_mod.csv": (
        TamuRangesAllTraitsOnly2Sept2025Mod,
    ),
    # "Thomomys bottae_mod.csv": (ThomomysBottaeMod,),
    # "TTU-NSF-Ranges-Data Corrections Next to Data-7-28-2025_mod.csv": (
    #     TtunsfRangesDataCorrections,
    # ),
    # "UMMZ_ranges_y2_final_mod.csv": (UmmzRangesY2FinalMod,),
    # "UWBM_Mamm_JSON_Attributes.csv": (UwbmMammJsonAttributes,),
    # "UWYMZ_Y1_mod.csv": (UwymzY1Mod, uwymz_y1_mod_multi_row_cleaner),
    # "UWYMZ_Y2_mod.csv": (UwymzY2Mod, uwymz_y2_mod_multi_row_cleaner),
}

COLUMN_ORDER = """
    occurrenceID scientificName
    body_mass
    calcar_length
    color
    ear_length ear_length_measured_from ear_length_2 ear_length_2_measured_from
        ear_length_3 ear_length_3_measured_from
    embryo_count embryo_count_left embryo_count_right
    embryo_length embryo_length_measured_from
    eventDate
    forearm_length
    hind_foot_length hind_foot_length_includes
    lactation_state lactation_description
    lifeStage
    nipple_state nipple_count nipple_size nipple_description
    ovary_description ovary_length_1 ovary_length_2 ovary_position
        ovary_width_1 ovary_width_2
    placental_scar_count placental_scars_left placental_scars_right
        placental_scars_present
    pregnancy_state
    sex
    tail_length
    tarsus_length
    testis_description testis_length_1 testis_length_2 testis_position
        testis_width_1 testis_width_2
    thumb_length thumb_length_includes
    tibia_length
    total_length
    tragus_length
    vagina_state
    wingspan
    """.split()


def main(args: argparse.Namespace) -> None:
    log.started()

    args.output_dir.mkdir(parents=True, exist_ok=True)

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

        columns = [c for c in COLUMN_ORDER if c in df.columns]
        columns += sorted(f for f in janitor_class.parsed_fields if f)
        columns += sorted(f for f in janitor_class.used_fields if f)
        columns += [c for c in df.columns if c not in columns and c]
        df = df[columns]

        path = args.output_dir / name
        df.to_csv(path, index=False)

    log.finished()


def per_row_cleaner(dirty: list[dict], janitor_class: Any) -> list[dict]:
    janitor_class.parsed_fields = set()
    janitor_class.used_fields = set()

    cleaned = []
    for row in tqdm(dirty):
        janitor = janitor_class(dirty=row)
        janitor.cleaner()
        janitor.clean |= {k: v for k, v in row.items() if k not in janitor.clean}
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
