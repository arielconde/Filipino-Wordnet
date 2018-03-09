import utils
import os
from random import randint
from sentences.modelbigram import ModelSentence as sentencemodel

def create_test_file(filepath, filename):
    f = open(filepath, 'r')
    fileans = './words/tests/ANSF' + filename.replace('.txt', '.json')
    text = f.read().replace("\\n", "").replace("'b'", "").replace("b'", "").replace("[", "").replace("]", "")

    sentences = utils.delim_sentences(text)

    data = []

    for sentence in sentences:
        print(sentence)
        sen_type = input("Enter type: [0] None, [1] Syn, [2] Hyp, [3] Holy, [4] Mero \nType: ")

        temp = {'sentence': sentence, 'type': sen_type}
        data.append(temp)

    fans = open(fileans, 'w')
    fans.write("[\n")
    for index, item in enumerate(data):
        if index == len(data) - 1:
            to_write = '\t{"type": "%s", "sentence": "%s"}\n' % (item['type'], item['sentence'], )
            fans.write(to_write)
        else:
            to_write = '\t{"type": "%s", "sentence": "%s"},\n' % (item['type'], item['sentence'], )
            fans.write(to_write)
    fans.write("]")

    ftxt = open('./words/tests/TESTF' + filename, 'w')
    ftxt.write(text)
    ftxt.close()

    f.close()
    fans.close()

if __name__ == '__main__':
    # create_test_file('testfile1.txt')
    files = os.listdir('./articles')

    n_tests = int(input("Input no. test files to be created: "))
    for i in range(0, n_tests):
        file_index = randint(0, len(files))
        path = './articles/' + files[file_index]
        print('Creating test file for:', files[file_index])
        create_test_file(path, files[file_index])

