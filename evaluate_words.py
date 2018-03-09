import sys
import os
import utils
import json
from words.modeltrigram import ModelWords as ModelWords

def run(relation, test_file):
    wordmodel = ModelWords(relation)
    
    with open(test_file) as data_ans:
        data = json.loads(data_ans.read())

    baseword_score = 0;
    subword_score = 0;

    for test_item in data:
        baseword, subword = wordmodel.getWords(test_item['sentence']);
        if (baseword == test_item['baseword']):
            baseword_score =  baseword_score + 1
        if (subword == test_item['subword']):
            subword_score = subword_score + 1

    print('Baseword Result:', baseword_score, "/", len(data))
    print("Subword Result:", subword_score, "/", len(data))

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])