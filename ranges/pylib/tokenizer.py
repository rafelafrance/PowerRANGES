from spacy.lang.char_classes import ALPHA
from traiter.pylib.pipes import tokenizer


def setup(nlp):
    tokenizer.setup_tokenizer(nlp)  # Normal setup

    tokenizer.append_prefix_regex(
        nlp,
        [
            "mm",  # Break on units
            # Always break on these characters
            "~",
        ],
    )

    tokenizer.append_infix_regex(
        nlp,
        [
            rf"(?<=[{ALPHA}])\.(?=[{ALPHA}\d])",  # Break on interior dot
            rf"(?<=[{ALPHA}])\.",  # Break on a dot
            rf"(?<=\d)(?=[{ALPHA}])",  # Break on digit followed by a letter
            rf"(?<=[{ALPHA}])(?=\d)",  # Break on letter followed by a digit
            # Always break on these characters
            "!",
            ",",
            "-",
            "/",
            ":",
            ";",
            "=",
            "~",
            '"',
            r"\(",
            r"\)",
            r"\+",
            r"\[",
            r"\]",
        ],
    )

    tokenizer.append_suffix_regex(
        nlp,
        [
            rf"(?<=\d)[{ALPHA}]+",  # Break on a digit followed by letters
            #
            # Break on a letter followed by digits but don't break up UUIDs
            r"(?<=[G-Zg-z])\d+",
            # Break on a key followed by digits. These overlap with UUIDs
            r"(?<=HF|hf|FA|fa)\d+",
        ],
    )
