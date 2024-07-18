import json
import traceback
from pathlib import Path

from ranges.pylib import occurrence, pipeline


def process_occurrences(
    tsv_file: Path,
    json_dir: Path,
    id_field: str,
    info_fields=None,
    parse_fields=None,
    overwrite_fields=None,
    *,
    debug: bool = False,
) -> str:
    info_fields = info_fields if info_fields else []
    parse_fields = parse_fields if parse_fields else []
    overwrite_fields = overwrite_fields if overwrite_fields else []

    try:
        occurrences = occurrence.read_occurrences(
            tsv_file,
            id_field=id_field,
            info_fields=info_fields,
            parse_fields=parse_fields,
            overwrite_fields=overwrite_fields,
        )

        nlp = pipeline.build()
        occurrence.parse_occurrences(occurrences, nlp)

        json_file = json_dir / f"{tsv_file.stem}.jsonl"
        with json_file.open("w") as out:
            for occur in occurrences:
                as_dict = occur.as_dict()
                json.dump(as_dict, out)
                out.write("\n")

    except:  # noqa: E722
        if debug:
            print(traceback.format_exc())
        return tsv_file.stem

    return ""
