import re


def token_to_words(sentence):
    """

    :param sentence:
    :return:
    """

    regex = '([\w]{0,})'
    regex_of_word = re.findall(regex, sentence)

    words = [x.lower() for x in regex_of_word if x is not '']

    return words
