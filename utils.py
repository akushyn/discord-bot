from fuzzywuzzy import fuzz


def get_token_ratio(s1, s2):
    """
    Get token ratio between two strings
    """
    if s1 is None or s2 is None:
        ratio = 0
    elif s1 == s2:
        ratio = 100
    else:
        ratio = fuzz.token_set_ratio(s1, s2)

    return ratio
