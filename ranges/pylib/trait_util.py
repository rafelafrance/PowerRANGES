def clear_tokens(ent):
    """Clear tokens in an entity."""
    for token in ent:
        token._.trait = None
        token._.flag = ""
        token._.term = ""
