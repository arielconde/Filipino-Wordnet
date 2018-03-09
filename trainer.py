from flask import Flask, render_template, request, redirect
from os import listdir, remove
import utils
import json
import pymongo

# initialize flask app
app = Flask(__name__)
app.debug = True

# mongod db
client = pymongo.MongoClient()
db = client.wordnetdb
trainingdata = db.trainingdata

# variable to hold the articles for training
MAX_ARTICLE_COUNT = 1000
articles = []
article_names = []

ARTICLES_FOLDER = 'better_articles/'

def loadarticles():
    files = listdir(ARTICLES_FOLDER)
    article_ctr = 0
    for file in files:
        if article_ctr > MAX_ARTICLE_COUNT:
            break

        try:
            # initialize article element to containe sentences
            global articles
            articles.append([])
            article_names.append(file)
            # open the file
            f = open(ARTICLES_FOLDER + file, 'r')
            # get the text and perform string processing
            article = f.read().replace("\\n", "").replace("'b'", "").replace("b'", "").replace("[", "").replace("]", "")
            article = ''.join([i for i in article if not i.isdigit()])
            # seperate by comma
            sentences = utils.delim_sentences(article)
            for sentence in sentences:
                articles[article_ctr].append(sentence)                
            f.close()

        except Exception as e:
            print("Error in " + file)
            print(e)

        # increment
        article_ctr = article_ctr + 1

############################################
#
# PAGES
#
#

@app.route('/')
@app.route('/index')
def index():
    return "Trainer"


############################################
#
# Training page
#
#

@app.route('/sentence/<article_id>/<sentence_id>', methods=['GET', 'POST'])
def train_sentence(article_id, sentence_id):

    try:
        # save to database
        data_baseword     = request.form.get('baseword')
        data_subword      = request.form.get('subword')
        data_relation     = request.form.get('relation')
        data_sentence     = request.form.get('sentence')
        data_baseword_pos = request.form.get('baseword_pos')
        data_subword_pos  = request.form.get('subword_pos')

        training_entry = {
            "sentence"    : data_sentence,
            "relation"    : data_relation,
            "baseword"    : data_baseword,
            "subword"     : data_subword,
            "baseword_pos": data_baseword_pos,
            "subword_pos" : data_subword_pos
        }

        if data_relation == 'None' and data_sentence != None:
            insert_id = trainingdata.insert_one(training_entry).insert_id
        elif data_relation == None:
            # insert_id = trainingdata.insert_one(training_entry).insert_id
            print('Invalid data')
        else:
            insert_id = trainingdata.insert_one(training_entry).insert_id
        
    except Exception as e:
        print(e)

    # set id to int, it is str when received from the url
    int_article_id = int(article_id)
    int_sentence_id = int(sentence_id)
    isMove = False

    # avoid overflow
    print(str(int_sentence_id) + " : " + str(len(articles[int_article_id])))
    if int_sentence_id < len(articles[int_article_id]) - 1:
        sentence = articles[int_article_id][int_sentence_id]
    else: # move to the next sentence
        return redirect('/sentence/' + str(int(article_id) + 1) + '/0')

    tokens = utils.tokenize(sentence)

    next_id = int(sentence_id) + 1
    next_article_id = int(article_id) + 1
    return render_template('sentence.html', title=article_names[int_article_id].replace('.txt', ''), sentence=sentence, tokens=tokens,
        id=sentence_id, next_article_id=next_article_id, next_id = next_id, move_to_next=isMove)

@app.route('/delete/<article_name>/<next_id>', methods=['GET', 'POST'])
def delete_article(article_name, next_id):
    to_remove = ARTICLES_FOLDER + article_name + '.txt'
    print('Removing:', to_remove)
    remove(to_remove)
    return redirect('/sentence/' + next_id + '/0')

if __name__ == "__main__":
    loadarticles()
    app.run()