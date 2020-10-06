from operator import attrgetter
import pickle
from language_model.probability_node import ProbabilityNode
from helpers.text_tokenizer import get_word_formatted
import json


class LanguageModel:

    def __init__(self):
        self.total_words_count = 0
        self.probability_nodes = dict()
        self.sorted_probability_nodes = list()

    def test_language_model(self):
        print([ [node.word, node.probability] for node in self.sorted_probability_nodes[:5]])
        for node2 in self.sorted_probability_nodes[:5]:
            print("Word: {}, Count: {}, Prob: {}, Children: {}, ProbChildren: {}".format(node2.word, node2.word_count, node2.probability, len(node2.children_nodes), len(node2.sorted_probability_nodes)))
            print([[node.word, node.probability] for node in node2.sorted_probability_nodes[:5]])

        return "Test Successful !!!"

    def get_top_n_words(self, n):
        return [ [node.word, node.probability] for node in self.sorted_probability_nodes[:n]]

    def get_next_word(self, words_sequence, n):
        words_to_use = min(2, len(words_sequence))
        words = words_sequence[-words_to_use:]
        print("Extracted last k words are: {}".format(words))

        result_list = list()

        for i in range(0, words_to_use, 1):

            formatted_word = get_word_formatted(words[i])

            current_node = self.probability_nodes.get(formatted_word, None)

            if current_node is None:
                continue

            path_exists = True

            for j in range(i+1, words_to_use, 1):
                child_word_formatted = get_word_formatted(words[j])
                if child_word_formatted not in current_node.children_nodes:
                    path_exists = False
                    break

                current_node = current_node.children_nodes[child_word_formatted]

            if path_exists:
                result_list.extend([[node.word, node.probability, i+1] for node in current_node.sorted_probability_nodes[:n]])
                # break

        return result_list

    # def get_next_word_using_current(self, words_sequence, n):
    #     words_to_use = min(2, len(words_sequence))
    #     words = words_sequence[-words_to_use:]
    #     print("Extracted last k words are: {}".format(words))
    #
    #     result_list = list()
    #
    #     for i in range(0, words_to_use, 1):
    #
    #         formatted_word = get_word_formatted(words[i])
    #
    #         current_node = self.probability_nodes.get(formatted_word, None)
    #
    #         if current_node is None:
    #             continue
    #
    #         path_exists = True
    #
    #         for j in range(i+1, words_to_use, 1):
    #             child_word_formatted = get_word_formatted(words[j])
    #             if child_word_formatted not in current_node.children_nodes:
    #                 path_exists = False
    #                 break
    #
    #             current_node = current_node.children_nodes[child_word_formatted]
    #
    #         if path_exists:
    #             result_list.extend([[node.word, node.probability, i+1] for node in current_node.sorted_probability_nodes[:n]])
    #             # break
    #
    #     return result_list


    def get_words_frequency(self, words_list):
        """
        For a list of words, return the number of appearances of each word. If the word doesn't appear in the data set
        on which the language model was trained or appears less than the specified minimum threshold of appearances to
        be trimmed out of the language model, we return 0.
        """

        result = dict()

        for word in words_list:
            count = 0
            if word in self.probability_nodes:
                count = self.probability_nodes[word].word_count

            result[word] = count

        return result

    def load_model_data(self, file_path):
        with open(file_path, "rb") as language_model:
            model_data = pickle.load(language_model)
            print("Loading model data with total words: {}".format(model_data[0]))
            self.total_words_count = model_data[0]
            self.probability_nodes = model_data[1]
            self.sorted_probability_nodes = model_data[2]


def sort_probability_list(probability_nodes):
    sorted_probability_nodes = sorted(probability_nodes, key=attrgetter("probability"), reverse=True)
    return sorted_probability_nodes
