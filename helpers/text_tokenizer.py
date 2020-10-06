import re
from cache.names_cache import is_word_name
from configuration import NAME_JOKER_SIGN, NUMBER_JOKER_SIGN

def token_to_words(sentence):
    """

    :param sentence:
    :return:
    """

    regex = '([\w]{0,})'
    regex_of_word = re.findall(regex, sentence)

    words = [x.lower() for x in regex_of_word if x is not '']

    return words


def get_word_formatted(word):
    if is_word_name(word):
        return NAME_JOKER_SIGN

    if word.isdigit():
        return NUMBER_JOKER_SIGN

    return word
