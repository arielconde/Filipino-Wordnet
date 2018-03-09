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


def evaluate(testfiletxt, answerfilejson):
    f = open(testfiletxt, 'r')
    text = f.read().replace("\\n", "").replace("'b'", "").replace("b'", "").replace("[", "").replace("]", "")

    sentences = utils.delim_sentences(text)

    with open(answerfilejson) as data_ans:
        data = json.loads(data_ans.read())

    for sentence in sentences:
        print(sentence)

if __name__ == '__main__':
    
    files = os.listdir()
    for file in files:
        if 'TESTF' in file:
            answerfile = file.replace('TESTF', 'ANSF').replace('.txt', '.json')
            print('Evaluating:', file, ',', answerfile)
            evaluate(file, answerfile)
        else:
            continue