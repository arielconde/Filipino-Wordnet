import os
import sys
import random
import utils
from sentences.modelbigram import ModelSentence as ModelSentence
from words.modeltrigram import ModelWords as ModelWords

def run(relation):
    print(relation);
    sentencemodel = ModelSentence(relation)
    wordmodel = ModelWords(relation)
    fsyn = open('sen_' + relation + '.txt', 'w');
    
    # work on the first 10 articles
    n = 100
    files = os.listdir('./articles')
    for i in range(0, n):
        file_index = random.randint(0, len(files));
        f = open('./articles/' + files[file_index], 'r')
        article = f.read()
        sentences = utils.delim_sentences(article)
        for sentence in sentences:

            #  A sentence with synonymy is found
            if (sentencemodel.predict(sentence)):
                to_write = sentence + '.\n';
                fsyn.write(to_write);
        f.close()

if __name__ == '__main__':
    run(sys.argv[1])