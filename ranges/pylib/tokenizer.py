from traiter.pylib.pipes import tokenizer


def setup(nlp):
    tokenizer.setup_tokenizer(nlp)  # Normal setup

    # tokenizer.append_prefix_regex(
    #     nlp,
    #     [
    #         r"\[",
    #     ]
    # )

    tokenizer.append_infix_regex(
        nlp,
        [
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

    # tokenizer.append_suffix_regex(
    #     nlp,
    #     [
    #         '"',
    #     ]
    # )

    # tokenizer.append_infix_regex(
    #     nlp,
    #     [
    #         r"(?<=\d),(?=[A-Za-z])",  # Break on digit comma letter
    #     ]
    # )
    #
    # # Always break tokens on these characters
    # tokenizer.append_infix_regex(nlp, r""" = - \( \) \[ \] " : ; """.split())

    tokenizer.append_suffix_regex(
        nlp,
        [
            # r"(?<=,)[A-Za-z]+",  # Break on comma followed by letter
            r"(?<=\d)[A-Za-z]+",  # Break on a digit followed by letter
        ],
    )
