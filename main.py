from language_model.language_model import LanguageModel
from flask import Flask
from flask import request
import json
from helpers.text_tokenizer import token_to_words
from helpers.utils import get_elapsed_time
from cache.names_cache import initialize_names_cache
from configuration import LANGUAGE_MODEL_FILE_PATH
import time


app = Flask(__name__)

LANGUAGE_MODEL = LanguageModel()


@app.route('/')
def hello():
    return "Welcome to the Language Model Service !!!"


@app.route('/model/top/<num_words>')
def get_top_n_words(num_words):

    print("NumWords={}, Message=\"Received request to return words with highest probability\"".format(num_words))

    result = LANGUAGE_MODEL.get_top_n_words(int(num_words))

    json_data = json.dumps(result, ensure_ascii=False)

    return json_data


@app.route('/model/query', methods=["GET"])
def get_next_word_suggestion():

    start_time = time.time()

    sentence = request.args["sentence"]

    words = token_to_words(sentence)

    result = LANGUAGE_MODEL.get_next_word(words, 1000)

    json_data = json.dumps(result, ensure_ascii=False)

    print("Query=\"model/query\", ElapsedTime={}, Message=\"Request\"".format(get_elapsed_time(start_time)))

    return json_data


# @app.route('/model/nextusingcurrent', methods=["GET"])
# def get_next_word_suggestion_using_current():
#
#     start_time = time.time()
#
#     sentence = request.args["sentence"]
#     current_written_word = request.args["current"]
#
#     words = token_to_words(sentence)
#
#     result = LANGUAGE_MODEL.get_next_word(words, 1000)
#
#     json_data = json.dumps(result, ensure_ascii=False)
#
#     print("Query=\"model/query\", ElapsedTime={}, Message=\"Request\"".format(get_elapsed_time(start_time)))
#
#     return json_data


@app.route('/model/words/frequency', methods=["GET"])
def get_word_occurrences():

    start_time = time.time()

    words_list = json.loads(request.args["words"])

    result = LANGUAGE_MODEL.get_words_frequency(words_list)

    json_data = json.dumps(result, ensure_ascii=False)

    print("Query=\"model/query/frequency\", ElapsedTime={}, WordsCount={}, Message=\"Request\"".format(get_elapsed_time(start_time), len(words_list)))

    return json_data


if __name__ == '__main__':

    initialize_names_cache()

    print("Message=\"Starting to load language model in memory\"")
    LANGUAGE_MODEL.load_model_data(LANGUAGE_MODEL_FILE_PATH)
    print("Message=\"Finished loading language model in memory\"")

    print("Message=\"Starting language model service.\"")
    app.run()
