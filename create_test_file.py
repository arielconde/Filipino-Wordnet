# Creates a test file for word classifier
import os
import sys
import random
import utils
from words.modeltrigram import ModelWords as ModelWords

def main(relation):
    print('Creating test file for', relation)
    f = open('sen_' + relation + '.txt', 'r')
    fans = open('ans_file2_' + relation +'.json', 'w')
    wordmodel = ModelWords(relation)
    text = f.read()
    
    data = []

    sentences = utils.delim_sentences(text)
    for sentence in sentences:
        print('-------\nSen:', sentence)
        baseword, subword = wordmodel.getWords(sentence)
        print(':::', baseword, subword)
        isCorrect = input("Is correct? [ENTER] YES --- [NO] NO")

        if len(isCorrect) == 0:
            temp = {'sentence': sentence, 'baseword': baseword, 'subword': subword} 
            data.append(temp)
            continue

        # else:
        #     r = random.randint(0, 10)
        #     if (r > 7):
        #         temp = {'sentence': sentence, 'baseword': baseword, 'subword': subword}
        #         data.append(temp)


        # baseword = input('Enter baseword: ')
        # if len(baseword) == 0:
        #     continue
        # subword = input('Enter subword: ')

    fans.write("[\n")
    for index, item in enumerate(data):
        if index == len(data) - 1:
            item['sentence'] = item['sentence'].replace('"', '')
            to_write = '\t{"baseword": "%s", "subword": "%s", "sentence": "%s"}\n' % (item['baseword'], item['subword'], item['sentence'])
            fans.write(to_write)
        else:
            item['sentence'] = item['sentence'].replace('"', '')
            to_write = '\t{"baseword": "%s", "subword": "%s", "sentence": "%s"},\n' % (item['baseword'], item['subword'], item['sentence'])
            fans.write(to_write)
    fans.write("]")

if __name__ == '__main__':
    main(sys.argv[1]); 