from spacy.tokens import Span

# When parsing is "E" an abbreviation for Ear or Embryo.
# I need a way to determine this for each invocation of the parsing function
# (I'm actually doing this per CSV column), but changing Traiter to handle this crap is
# a no go. My current solution is to attach a non-parsable suffix to the text being
# parsed and use that as a flag in the parsers. The flag must be a suffix so it doesn't
# move trait offsets and I choose a spelling to defeat Traiter so it doesn't interfere
# with normal parsing.
EMBRYO = "eemmbbrryyoo"
LENGTH = "lleennggtthh"
EAR = "eeaarr"
NONE = ""

EMBRYO_LEN = len(EMBRYO)
LENGTH_LEN = len(LENGTH)
EAR_LEN = len(EAR)


def e_is_embryo(text: str) -> bool:
    return text.endswith(EMBRYO)


def remove_embryo_flag(ent: Span, *, ambiguous: bool) -> tuple[str, int]:
    if len(ent.text) >= EMBRYO_LEN and ambiguous:
        return ent.text.removesuffix(EMBRYO), ent.end_char - EMBRYO_LEN
    return ent.text, ent.end_char


def l_is_length(text: str) -> bool:
    return text.endswith(LENGTH)


def remove_length_flag(ent: Span, *, ambiguous: bool) -> tuple[str, int]:
    if len(ent.text) >= LENGTH_LEN and ambiguous:
        return ent.text.removesuffix(LENGTH), ent.end_char - LENGTH_LEN
    return ent.text, ent.end_char
