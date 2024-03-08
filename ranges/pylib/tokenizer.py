from spacy.lang.char_classes import ALPHA
from traiter.pylib.pipes import tokenizer


def setup(nlp):
    tokenizer.setup_tokenizer(nlp)  # Normal setup

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
            rf"(?<=\d)[{ALPHA}]+",  # Break on a digit followed by letter
        ],
    )
