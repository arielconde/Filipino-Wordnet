"""
    This is a testing script
    This accepts two files
    1 - Testing Files
        Contains the raw article
    2 - Answers
        Contains the sentences tagged with the
        relation, baseword and subword

    usage:
    python runtest.py testfile1.txt answerfile1.txt
"""

import sys
import json
import os
import utils

from modelbigram import Model

""" 
[0] None, [1] Syn, [2] Hyp, [3] Holy, [4] Mero
"""


def evaluate(testfiletxt, answerfilejson, relation, logfile):

    REL_INDEX = 0
    if relation == 'Synonymy':
        REL_INDEX = 1
    elif relation == 'Hyponym':
        REL_INDEX = 2
    elif relation == 'Holynym':
        REL_INDEX = 3
    elif relation == 'Meronym':
        REL_INDEX = 4

    model = Model(relation)

    f = open(testfiletxt, 'r')
    text = f.read().replace("\\n", "").replace("'b'", "").replace("b'", "").replace("[", "").replace("]", "")

    sentences = utils.delim_sentences(text)

    with open(answerfilejson) as data_ans:
        data = json.loads(data_ans.read())

    print("-------------------------")
    print("\n", relation)
    score = 0
    for sentence in sentences:
        print('\n\nClassifying:', sentence)
        # print(model_syn.getTotalScore(sentence))
        prediction =  model.predict(sentence)
        sen_type = getType(data, sentence)
        print(':: Classification if', relation, ':\t', prediction)

        # one is our marker if syn
        if sen_type == REL_INDEX:
            ans = True
        else:
            ans = False
        print(':: From ANS file is', relation, ':\t', ans)

        if ans == prediction:
            score = score + 1
            print('Match')

    print('\n\nScore for', relation, ':', score, '/', len(sentences))
    to_write = "%f, %d, %d\n" % (score/len(sentences), score, len(sentences))
    logfile.write(to_write)
    

def getType(data, sentence):
    for datum in data:
        if datum['sentence'] == sentence:
            return int(datum['type'])
        else:
            continue

    return -1

if __name__ == '__main__':
    
    logfile =   open('evallog.csv', 'w')\

    files = os.listdir('tests/')
    logfile.write('Synonymy\n\n')
    count = 1
    for file in files:
        if 'TESTF' in file:
            answerfile = 'tests/' + file.replace('TESTF', 'ANSF').replace('.txt', '.json')
            print('Evaluating:', 'tests/' + file, ',', answerfile)
            logfile.write('File' + str(count) + ' ,')
            evaluate('tests/' + file, answerfile, 'Synonymy', logfile)
            # evaluate('tests/' + file, answerfile, 'Hyponym', logfile)
            count = count + 1
        else:
            continue

    logfile.write('Hyponym\n\n')
    count = 1
    for file in files:
        if 'TESTF' in file:
            answerfile = 'tests/' + file.replace('TESTF', 'ANSF').replace('.txt', '.json')
            print('Evaluating:', 'tests/' + file, ',', answerfile)
            logfile.write('File' + str(count) + ' ,')
            # evaluate('tests/' + file, answerfile, 'Synonymy', logfile)
            evaluate('tests/' + file, answerfile, 'Hyponym', logfile)
            count = count + 1
        else:
            continue

    logfile.close()