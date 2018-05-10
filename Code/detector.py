# -*- coding: utf-8 -*-
import sys
import pinyin
import jieba
import string
import re


def construct_dict(inpath):
    #construct self dict with data
    word_freq = {}
    with open(inpath, 'r') as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency
        return word_freq

def get_cn_dict(inpath):
    '''
    get all the frequency chinese words from inpath to form a string called word_dict 
    use the word in this dict to replace the words in given phrases
    if the replaced phrases is in the freqlist, put it in the candidate set
    '''
    word_dict = ""
    with open(inpath, 'r') as f:
        for word in f:
            word_dict += word.strip().decode('utf-8')
    return word_dict

def edits_dis_1(phrase, cn_dict):
    '''
    get a set of all the words that are 1 edit distance with the given phrase
    with the help of chinese dictionary cn_dict
    '''
    phrase = phrase.decode('utf-8')
    splits     = [(phrase[:i], phrase[i:])  for i in range(len(phrase) + 1)]
    #print "splits:", [split.encode('utf-8') for split in splits]
    deletes    = [L + R[1:]                 for L, R in splits if R]
    #print "deletes:", [delete for delete in deletes]
    transposes = [L + R[1] + R[0] + R[2:]   for L, R in splits if len(R)>1]
    #print "transposes:", transposes
    replaces   = [L + c + R[1:]             for L, R in splits if R for c in cn_dict]
    #print "replaces:", replaces
    inserts    = [L + c + R                 for L, R in splits for c in cn_dict]
    #print "inserts:", inserts
    return set(deletes + transposes + replaces + inserts)

def is_in_dict(phrases, word_freq):
    '''
    Judge if the phrase in phrases list are noticed in the given dictionary word_freq
    '''
    return set(phrase for phrase in phrases if phrase.encode("utf-8") in word_freq)

def get_candidate(phrase, cn_dict, word_freq):
    '''
    Sort the candidates phrases of a given phrase into three lists
    Return the three(or two) lists are: candidates_1, candidates_2, candidates_3
    '''
    candidates_1 = []
    candidates_2 = []
    #candidates_3 = []

    input_pinyin = pinyin.get(phrase, format="strip", delimiter = "/")
    all_candidates_set = edits_dis_1(phrase, cn_dict)
    candidates = list(is_in_dict(all_candidates_set, word_freq))
    
    for candidate in candidates:
        candidate_pinyin = pinyin.get(candidate, format="strip", delimiter = "/")
        if candidate_pinyin == input_pinyin:
            candidates_1.append(candidate)
        else:
            candidates_2.append(candidate)

    return candidates_1, candidates_2

def auto_correct( error_phrase, cn_dict, word_freq ):
        
    c1_order, c2_order = get_candidate(error_phrase, cn_dict, word_freq)
    # print c1_order, c2_order, c3_order
    if c1_order:
        return max(c1_order, key=word_freq.get )
    elif c2_order:
        return max(c2_order, key=word_freq.get )

if __name__ == '__main__':
    inpath1 = 'data/token_freq_pos_jieba.txt'
    inpath2 = 'data/4_freqlist_withEn'
    inpath3 = 'data/cn_dict.txt'
    
    # Step1: get frequency list
    print "Building jieba standard ist..."
    word_freq1 = construct_dict(inpath1)
    print len(word_freq1)

    print "Building self-build word list..."
    word_freq2 = construct_dict(inpath2)
    print len(word_freq2)
    
    # Step2: get chinese dictionary
    print "Getting chinese dictionary..."
    cn_dict = get_cn_dict(inpath3)
    print len(cn_dict)

    # Step3: test pinyin candicate
    print "Testing on getting candidate of ..."
    error_phrase = "舒学"
    #error_pinyin = pinyin.get(error_phrase, format="strip", delimiter="/")
    #a = edits_dis_1(error_phrase, cn_dict)
    #phrases_list = list(is_in_dict(a, word_freq2))
    #print len(phrases_list)
    #for p in phrases_list:
    #    print p.encode('utf-8')
    c1= auto_correct(error_phrase, cn_dict, word_freq2)
    print c1

    #DEMO
    #count = 0
    #for k,v in word_freq2.items():
    #    print(k, v)
    #    count += 1
    #    if count > 10:
    #        break

