from language_model.language_model import LanguageModel
from flask import Flask
from flask import jsonify
import json

app = Flask(__name__)

FILE_PATH = "language_model.pickle"

LANGUAGE_MODEL = LanguageModel()


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/model/test')
def test_language_model():
    return LANGUAGE_MODEL.test_language_model()


@app.route('/model/top/<num_words>')
def get_top_n_words(num_words):

    print("NumWords={}, Message=\"Received request to return words with highest probability\"".format(num_words))

    result = LANGUAGE_MODEL.get_top_n_words(int(num_words))

    json_data = json.dumps(result, ensure_ascii=False)

    return json_data


if __name__ == '__main__':

    print("Message=\"Starting to load language model in memory\"")
    LANGUAGE_MODEL.load_model_data(FILE_PATH)
    print("Message=\"Finished loading language model in memory\"")

    app.run()
