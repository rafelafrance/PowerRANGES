from spacy.tokens import Span


def clear_tokens(ent: Span) -> None:
    """Clear tokens in an entity."""
    for token in ent:
        token._.trait = None
        token._.flag = ""
        token._.term = ""
