"""
    creates a vocabulary from the training data in the db
    in the form of
    word word_id
"""

import utils
import pymongo

client = pymongo.MongoClient()
db = client.wordnetdb
trainingdata = db.trainingdata

# create unigram vocabulary from the training sentences
# depending on the relation
# so its just comparing a word with a relation to a none
def createvocabulary(relation):

    # initialize vocabulary
    vocabulary = {}

    for training_sentence in trainingdata.find():
        if training_sentence['relation'] == relation:

            # tokenize the sentence
            tokens = utils.tokenize(training_sentence['sentence'])

            subword_pos = int(training_sentence['subword_pos'])
            baseword_pos = int(training_sentence['baseword_pos'])
            
            # iterate on tokens then add it to the vocabulary if it doenst exist yet
            # assign initial scores and occurence
            for token in tokens:
                # token is none and it is not a sub or base word
                if token == tokens[subword_pos] or token == tokens[baseword_pos]:
                    vocabulary[token] = {}
                    vocabulary[token]['score'] = 0
                    vocabulary[token]['occurence'] = 1
                elif vocabulary.get(token) == None:
                    vocabulary[token] = {}
                    vocabulary[token]['key'] = token
                    vocabulary[token]['score'] = 0
                    vocabulary[token]['occurence'] = 1
                else:
                    vocabulary[token]['score'] = vocabulary[token]['score'] + 0
                    vocabulary[token]['occurence'] = vocabulary[token]['occurence'] + 1

            # assign score considering the lenght from the base and subword
            # Two Mountain Model
            # 1 1 1 2 3 4 5 Baseword 5 4 3 2 1 1 1
            # 3 4 5 Subword 5 4 3 2 1 1 1 1 1 1 1
            for i in range(0, 4):

                score_to_add = 2

                token_pos_left = int(training_sentence['subword_pos']) - i # 5 - 1 = 4
                token_pos_right = int(training_sentence['subword_pos']) + i # 5 + 1 = 6
                
                if token_pos_left >= 0 and token_pos_left != subword_pos and token_pos_left != baseword_pos:
                    token_left = tokens[token_pos_left]
                    vocabulary[token_left]['score'] = vocabulary[token_left]['score'] + score_to_add
                if token_pos_right < len(tokens):
                    token_right = tokens[token_pos_right]
                    vocabulary[token_right]['score'] = vocabulary[token_right]['score'] + score_to_add

                token_pos_left = int(training_sentence['baseword_pos']) - i # 5 - 1 = 4
                token_pos_right = int(training_sentence['baseword_pos']) + i # 5 + 1 = 6

                if token_pos_left >= 0:
                    token_left = tokens[token_pos_left]
                    vocabulary[token_left]['score'] = vocabulary[token_left]['score'] + score_to_add
                if token_pos_right < len(tokens) and token_pos_right != subword_pos and token_pos_right != baseword_pos:
                    token_right = tokens[token_pos_right]
                    vocabulary[token_right]['score'] = vocabulary[token_right]['score'] + score_to_add

    return vocabulary

def getWord(word):
    if vocabulary.get(word) != None:
        return vocabulary[word]
    else:
        return 0

def getScore(word, vocabulary):
    ret_val = 0
    if vocabulary.get(word) != None:
        return vocabulary[word]['score'] / vocabulary[word]['occurence']
        # return vocabulary[word]['score']
    else:
        return 0

# sorts the vocabulary by occurences
# with this we can get the key values we need
def sortVocabularyByScore(vocabulary):
    new_voc = []
    voc_count = len(vocabulary)
    for i in range(0, voc_count):
        highest = None
        for index, token in enumerate(vocabulary):
            if highest == None:
                highest = token
            else:
                if vocabulary[highest]['score'] < vocabulary[token]['score']:
                    highest = token
        new_voc.append(vocabulary[highest])
        del vocabulary[highest]
    return new_voc

# returns the array of values, and the total
def getRepresentation(sentence, vocabulary):
    representation = []
    total = 0
    tokens = utils.tokenize(sentence)
    for token in tokens:
        if vocabulary.get(token) != None:
            rep_score = vocabulary[token]['score']
            # rep_score = vocabulary[token]['occurence']
            representation.append(rep_score)
            total = total + rep_score
        else:
            representation.append(0)
    
    return representation, total




if __name__ == '__main__':
    vocabulary = createvocabulary('Hypnomy')
    # for index, token in enumerate(vocabulary):
    #     # print("%d\t: %s %d \t %d" % (index, token, vocabulary[token]['score'], vocabulary[token]['occurence']))
    #     prob = vocabulary[token]['score']
    #     print("%f\t%s" % (prob, token))

    # # print(getRepresentation('Ang aleman ay isang bayan sa europa.', vocabulary))

    # words = sortVocabularyByScore(vocabulary)
    # for word in words:
    #     print(word)
    print(vocabulary['ang'])

