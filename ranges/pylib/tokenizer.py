from spacy.lang.char_classes import ALPHA
from traiter.pylib.pipes import tokenizer


def setup(nlp):
    tokenizer.setup_tokenizer(nlp)  # Normal setup

    tokenizer.append_prefix_regex(
        nlp,
        [
            "mm",  # Break on units
        ],
    )

    tokenizer.append_infix_regex(
        nlp,
        [
            rf"(?<=[{ALPHA}])\.(?=[{ALPHA}])",  # Break on interior dot
            # Always break on these characters
            "=",
            "-",
            ",",
            ";",
            ":",
            '"',
            r"\[",
            r"\]",
            r"\(",
            r"\)",
        ],
    )

    tokenizer.append_suffix_regex(
        nlp,
        [
            rf"(?<=\d)[{ALPHA}]+",  # Break on a digit followed by letters
            # Break on a key followed by digits
            # Cannot use letters follwed by digits b/c of UUIDs
            r"(?<=SVL|svl|TOL|tol|ToL|HFL|hfl|EFN|efn|EAR|ear)\d+",
            r"(?<=TL|tl|TR|tr|HF|hf|FA|fa|SL|sl)\d+",
            r"(?<=n|t)\d+",
        ],
    )
