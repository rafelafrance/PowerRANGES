import json
import traceback
from pathlib import Path

from ranges.pylib import occurrence, pipeline


def process_occurrences(
    csv_file: Path,
    json_dir: Path,
    id_field: str,
    info_fields: list[str] | None = None,
    parse_fields: list[str] | None = None,
    overwrite_fields: list[str] | None = None,
    *,
    debug: bool = False,
) -> str:
    info_fields = info_fields or []
    parse_fields = parse_fields or []
    overwrite_fields = overwrite_fields or []

    try:
        occurrences = occurrence.read_occurrences(
            csv_file,
            id_field=id_field,
            info_fields=info_fields,
            parse_fields=parse_fields,
            overwrite_fields=overwrite_fields,
        )

        nlp = pipeline.build()
        occurrence.parse_occurrences(occurrences, nlp)

        json_file = json_dir / f"{csv_file.stem}.jsonl"
        with json_file.open("w") as out:
            for occur in occurrences:
                as_dict = occur.as_dict()
                json.dump(as_dict, out)
                out.write("\n")

    except:  # noqa: E722
        if debug:
            print(traceback.format_exc())
        return csv_file.stem

    return ""
