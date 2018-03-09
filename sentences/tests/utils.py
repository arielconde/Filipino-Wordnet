import re

# seperate sentences by period
# to do
# seperate by thought, single compound sentences
def delim_sentences(article):
    temp_arr_sen = str(article).split('.')
    sentences = []
    for sentence in temp_arr_sen:
        if len(sentence) > 2:
            # sentences.append(sentence.strip())
            sentence = clean_paren(sentence)
            # sentences = sentences + sentence.strip().split(',')
            sentences.append(sentence.strip())
    return sentences


""" 
    tokenize
"""
def tokenize(sentence):
    tokens = [];
    splitted_words = re.split(' |\n|\t ', sentence.lstrip())
    for word in splitted_words:
        if word.isspace():
            continue
        tokens.append(''.join(e for e in word.lower() if e.isalnum()))

    return tokens

def create_template(sentence, base_pos, sub_pos):
    tokens = tokenize(sentence)

    sen_temp = ""
    for index, token in enumerate(tokens):
        if index == base_pos:
            if len(sen_temp) == 0:
                sen_temp = '_____'
            else:
                sen_temp = sen_temp + ' _____'
        elif index == sub_pos:
            if len(sen_temp) == 0:
                sen_temp = '_____'
            else:
                sen_temp = sen_temp + ' _____'
        else:
            if len(sen_temp) == 0:
                sen_temp = token
            else:
                sen_temp = sen_temp + ' ' + token

    return sen_temp

def clean_paren(test_str):
    ret = ''
    skip1c = 0
    skip2c = 0
    for i in test_str:
        if i == '[':
            skip1c += 1
        elif i == '(':
            skip2c += 1
        elif i == ']' and skip1c > 0:
            skip1c -= 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip1c == 0 and skip2c == 0:
            ret += i
    return ret