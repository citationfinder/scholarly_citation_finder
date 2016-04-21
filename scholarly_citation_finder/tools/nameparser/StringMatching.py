from difflib import SequenceMatcher

def match_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()

def nearly_match(a, b, minimum_ratio=0.9):
    return match_ratio(a, b) >= minimum_ratio

def words_difference(a, b, max_num_words_difference=2):
    num_words_a = len(a.split(' '))
    num_words_b = len(b.split(' '))
    return abs(num_words_a - num_words_b) <= max_num_words_difference
