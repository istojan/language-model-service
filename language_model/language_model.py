from operator import attrgetter
import pickle
from language_model.probability_node import ProbabilityNode


class LanguageModel:

    def __init__(self):
        self.total_words_count = 0
        self.probability_nodes = dict()
        self.sorted_probabiliy_nodes = list()

    def test_language_model(self):
        print([ [node.word, node.probability] for node in self.sorted_probability_nodes[:5]])
        for node2 in self.sorted_probability_nodes[:5]:
            print("Word: {}, Count: {}, Prob: {}, Children: {}, ProbChildren: {}".format(node2.word, node2.word_count, node2.probability, len(node2.children_nodes), len(node2.sorted_probability_nodes)))
            print([[node.word, node.probability] for node in node2.sorted_probability_nodes[:5]])

        return "Test Successful !!!"

    def get_top_n_words(self, n):
        return [ [node.word, node.probability] for node in self.sorted_probability_nodes[:n]]

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
