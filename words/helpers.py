import words.vocabulary as vocabularyuni
import numpy as np

def getHighestWords(relation, word_type):
    voc = vocabularyuni.createvocabulary(relation, word_type);
    n = 12
    highest_words = []
    for i in range(0, n):
        highest_token = '_____'
        for index, token in enumerate(voc):
            if vocabularyuni.getOccurence(token, voc) > vocabularyuni.getOccurence(highest_token, voc):
                highest_token = token
        highest_words.append(highest_token);
        del voc[highest_token]
    return highest_words


if __name__ == '__main__':
    words = getHighestWords('Hypnomy', 'SUBWORD');
    for word in words:
        print(word)