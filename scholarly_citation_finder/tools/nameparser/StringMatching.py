from difflib import SequenceMatcher

def match_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def nearly_match(a, b):
    return match_ratio(a, b) >= 0.9
