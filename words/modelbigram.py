import time
import vocabulary as vocabularyuni
import vocabularybigram as vocabularybi
import pymongo

client = pymongo.MongoClient()
db = client.wordnetdb
trainingdata = db.trainingdata


class Model(object):

    vocabulary = {}
    vocabularybigram = {}
    scoremodel = {}
    mininum = 999

    def __init__(self, relation, word):

        # Assigns score on bigrams base on unigram scores
        self.vocabulary = vocabularyuni.createvocabulary(relation, word)
        self.vocabularybigram = vocabularybi.createvocabulary(relation, word)

        for word1 in self.vocabularybigram:

            if word1 == 'END' or word1 == 'START':
                score = 0
            else:
                score = vocabularyuni.getScore(word1, self.vocabulary)
            
            for word2 in self.vocabularybigram[word1]:
                if word2 != 'END' and word2 != 'START':
                    score = score + vocabularyuni.getScore(word2, self.vocabulary)

                if word2 == 'END' or word2 == 'START' or word1 == 'END' or word1 == 'START':
                    score = 0

                # elif vocabularyuni.getScore(word1, self.vocabulary) == 0 or vocabularyuni.getScore(word2, self.vocabulary) == 0:
                #     score = 0

                if self.scoremodel.get(word1) == None:
                    self.scoremodel[word1] = {}
                self.scoremodel[word1][word2] = score
                # print(word1, word2, score)
        # end of assigning scores
        
        # set score for sentences
        for traing_item in trainingdata.find({ 'relation': relation }):
            score = self.getTotalScore(traing_item['sentence'])
            if score < self.mininum:
                self.mininum = score

    def getTotalScore(self, sentence):
        # time.sleep(0.5) # remove lag from db
        # print('Score Model: ', self.scoremodel)
        bigrams = vocabularybi.getBigram(sentence)
        total = 0
        for word1 in bigrams:
            # if word1 in self.scoremodel:
            #     for word2 in bigrams[word1]:
            #         if word2 in self.scoremodel[word1]:
            #             total = total + self.scoremodel[word1][word2]
            #         else:
            #             continue
            # else:
            #     continue
            for word2 in bigrams[word1]:
                total = total + vocabularyuni.getScore(word1, self.vocabulary) + vocabularyuni.getScore(word2, self.vocabulary)
        return total

    def predict(self, sentence):
        score = self.getTotalScore(sentence)
        # print('Self minimum: ', self.mininum)
        # print('Score:', score)
        if score >= self.mininum:
            return True
        else:
            return False


if __name__ == '__main__':
    model = Model('Synonymy', 'BASEWORD')
    print('Training SVM from Model')
    for training_item in trainingdata.find({ 'relation': 'Synonymy' }):
        print('-----------------------------------------')
        print('Sentence:', training_item['sentence'])
        score = model.getTotalScore(training_item['sentence'])
        print('Score:', score)
        print('-----------------------------------------')

    # print('-----------------------------------------')
    # print('-----------------------------------------')
    # print('------------END OF TRAING UNIT TEST--------------')
    # print('-----------------------------------------')
    # print('-----------------------------------------')
    # print('MODELING UNIT TEST: ')
    # sentence = 'Ang lapis o panulat ay gigamit upang magpahayag'
    # print('IF synonymy for:', sentence)
    # print('Classification:', model.predict(sentence))