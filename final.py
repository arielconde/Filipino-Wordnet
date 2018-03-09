import os
import utils
from sentences.modelbigram import ModelSentence as ModelSentence
from words.modeltrigram import ModelWords as ModelWords

def run():
    sentencemodel = ModelSentence('Synonymy')
    wordmodel = ModelWords('Synonymy')
    fsyn = open('sen_syn.txt', 'w');
    
    # work on the first 10 articles
    n = 100
    files = os.listdir('./articles')
    for i in range(0, len(files)):
        f = open('./articles/' + files[i], 'r')
        article = f.read()
        sentences = utils.delim_sentences(article)
        for sentence in sentences:

            #  A sentence with synonymy is found
            if (sentencemodel.predict(sentence)):
                to_write = sentence + '\n';
                fsyn.write(to_write);
                print(files[i], ":", wordmodel.getWords(sentence))
        f.close()

if __name__ == '__main__':
    run()