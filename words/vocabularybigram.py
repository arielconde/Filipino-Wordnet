import utils
import pymongo

client = pymongo.MongoClient()
db = client.wordnetdb
trainingdata = db.trainingdata

# relation = Hyponym, Synonym, Meronym, Holynym
# word = BASEWORD, SUBWORD
def createvocabulary(relation, word):
    model = {
        "START": {},
        "END": {}
    }

    for training_item in trainingdata.find():
        if training_item['sentence'] == None or training_item['relation'] != relation:
            continue
        else:
            # get the position of the word type to be modelled
            if word == 'BASEWORD':
                position = int(training_item['baseword_pos'])
            elif word == 'SUBWORD':
                position = int(training_item['subword_pos'])
            else:
                print('Invalid word type, while creating vocabulary. Vocabulary.py 35\n');
                return

            sen = utils.create_template(training_item['sentence'], position)

            # print(sen)
            model = append_vocabulary(sen, model)

    return model


# create a bigram vocabulary
def append_vocabulary(sen, model):

    tokens = utils.tokenize(sen)
    # print tokens
    
    if tokens[0] in model["START"]:
        model["START"][tokens[0]] = model["START"][tokens[0]] + 1
    else:
        model["START"][tokens[0]] = 1

    token_prev = tokens[0]

    # print tokens

    for token in tokens[1:]:

        if model.get(token_prev) == None:
            model[token_prev] = {}
        
        if model[token_prev].get(token) == None:
            model[token_prev][token] = 1

        token_prev = token


    # then assign probabilty for the last token be end token
    if model.get(token_prev) == None:
        model[token_prev] = {}
    model[token_prev]["END"] = 1

    return model

# helper
def getBigram(sentence):

    tokens = utils.tokenize(sentence)

    model = {
        "START": {},
        "END": {}
    }

    if tokens[0] in model["START"]:
        model["START"][tokens[0]] = model["START"][tokens[0]] + 1
    else:
        model["START"][tokens[0]] = 1

    token_prev = tokens[0]

    # print tokens

    for token in tokens[1:]:

        if model.get(token_prev) == None:
            model[token_prev] = {}
        
        if model[token_prev].get(token) == None:
            model[token_prev][token] = 1

        token_prev = token


    # then assign probabilty for the last token be end token
    if model.get(token_prev) == None:
        model[token_prev] = {}
    model[token_prev]["END"] = 1

    return model


if __name__ == '__main__':
    vocabulary = createvocabulary('Hypnomy', 'BASEWORD')
    for word1 in vocabulary:
        for word2 in vocabulary[word1]:
            print(word1, word2)