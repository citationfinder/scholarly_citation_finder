from difflib import SequenceMatcher

def match_ratio(a, b):
    '''
    Compute matching ratio of two strings.
    
    :param a: A string
    :param b: A string
    :return: Matching ratio
    '''
    return SequenceMatcher(None, a, b).ratio()

def nearly_match(a, b, minimum_ratio=0.9):
    '''
    Check if two strings nearly match.
    
    :param a: A string
    :param b: A string
    :param minimum_ratio: Optional minimum matching ratio
    :return: True, if strings nearly match. False otherwise.
    '''
    return match_ratio(a, b) >= minimum_ratio

def words_difference(a, b, max_num_words_difference=2):
    '''
    Check if words difference.
    
    :param a: Some words
    :param b: Some words
    :param max_num_words_difference: Maximum number of word difference
    :return: True, if words difference is smaller than the given tolerance
    '''
    num_words_a = len(a.split(' '))
    num_words_b = len(b.split(' '))
    return abs(num_words_a - num_words_b) <= max_num_words_difference
