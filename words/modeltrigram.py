import words.utils as utils
import words.vocabulary as vocabularyuni
import words.helpers as helpers


class ModelWords(object):

    vocabularysubword = {}
    vocabularybaseword = {}
    highest_words_sub = {}
    highest_words_base = {}
    def __init__(self, relation):
        self.vocabularysubword = vocabularyuni.createvocabulary(relation, 'SUBWORD')
        self.vocabularybaseword =  vocabularyuni.createvocabulary(relation, 'BASEWORD')
        self.highest_words_sub = helpers.getHighestWords(relation, 'SUBWORD')
        self.highest_words_base = helpers.getHighestWords(relation, 'BASEWORD')


    def getWords(self, sentence):

        trigrams = utils.getTrigrams(sentence)

        # basewords
        voc = self.vocabularybaseword
        highest_words = self.highest_words_base
        highest_score = 0
        highest_word = ""
        for trigram in trigrams:
            score = 0
            
            score = vocabularyuni.getScore(trigram[0], voc)
            score = score + vocabularyuni.getScore(trigram[2], voc)
            if score > highest_score and not trigram[1] in highest_words:
                highest_score = score
                highest_word = trigram[1]
        baseword = highest_word

        # subwords
        voc = self.vocabularysubword
        highest_words = self.highest_words_sub
        highest_score = 0
        highest_word = ""
        for trigram in trigrams:
            score = 0
            
            score = vocabularyuni.getScore(trigram[0], voc)
            score = score + vocabularyuni.getScore(trigram[2], voc)
            if score > highest_score and not trigram[1] in highest_words and not trigram[1] == baseword:
                highest_score = score
                highest_word = trigram[1]
        subword = highest_word

        return baseword, subword

if __name__ == '__main__':
    modelHypo = ModelWords('Hypnomy')
    base, sub = modelHypo.getWords('Ang upuan ay isang uri ng kagamitan')
    print(base, sub)
