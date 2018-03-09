from flask import Flask, render_template, request, redirect
from os import listdir, remove
import utils
import json
import pymongo

from modelbigram import Model

# initialize flask app
app = Flask(__name__)
app.debug = True

@app.route('/')
@app.route('/index')
def index():
    return render_template('demo.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    article = request.form.get('article').replace("\\n", "").replace("'b'", "").replace("b'", "").replace("[", "").replace("]", "")
    relation = request.form.get('relation')
    # print('Article:', article)
    print(relation)
    results = getResults(article, relation)
    return render_template('results.html', results=results, relation=relation)

def getResults(article, relation):
    model = Model(relation)
    sentences = utils.delim_sentences(article)

    ret_val = []

    for sentence in sentences:
        classification = model.predict(sentence)
        temp_item = {"sentence": sentence, "classification": classification}
        ret_val.append(temp_item)
        # print(sentence)
        # print(classification)

    return ret_val


if __name__ == "__main__":
    app.run()