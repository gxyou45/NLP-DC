# -*- coding: utf-8 -*-
import kenlm
import jieba
import numpy as np
import pickle
import pypinyin
import pinyin
import codecs
import os
import sys
import re
import time
import string
import math
from pypinyin import pinyin, lazy_pinyin
import pinyin
from collections import Counter

#########################################################################################
#                                                                                       #
#                                  DATA/MODEL LOADING                                   #
#                                                                                       #
#########################################################################################

print 'Loading models...'

jieba.initialize()
jieba.load_userdict("../data/dict/words_newjieba.data")

#bimodel_path = './kenmodels/zhwiki_bigram.klm'
bimodel_path = '../Model/final-2gram.arpa'
bimodel = kenlm.Model(bimodel_path)
print 'Loaded bigram language model from {}'.format(bimodel_path)

#trimodel_path = './kenmodels/zhwiki_trigram.klm'
trimodel_path = '../Model/final-3gram.arpa'
trimodel = kenlm.Model(trimodel_path)
print 'Loaded trigram language model from {}'.format(trimodel_path)

#_4model_path = './kenmodels/zhwiki_4gram.arpa'
_4model_path = '../Model/final-4gram.arpa'
_4model = kenlm.Model(_4model_path)
print 'Loaded 4-gram language model from {}'.format(_4model_path)

#wordmodel_path = './kenmodels/zhwiki_word_bigram.arpa'
wordmodel_path = '../Model/final-word-bigram.arpa'
wordmodel = kenlm.Model(wordmodel_path)
print 'Loaded word-level bigram language model from {}'.format(wordmodel_path)

text_path = '../data/wikipedia/cn_wiki.txt'
counter_path = '../data/dict/counter_jieba_py2.pkl'#wikipedia/cn_wiki_counter.pkl'

# Load the character Counter (字频统计)
if os.path.exists(counter_path):
    print 'Loading Counter from file: {}'.format(counter_path)
    counter = pickle.load(open(counter_path, 'rb'))
else:
    print 'Generating Counter from text file: {}'.format(text_path)
    counter = Counter((codecs.open(text_path, 'r', encoding='utf-8').read()))
    pickle.dump(counter, open(counter_path, 'wb'))
    print 'Dumped Counter to {}'.format(counter_path)

total = sum(counter.values()) # Total number of characters in text

# 形近字dictionary
xjz_dict_path = '../data/dict/xjz_py2.pkl'
if os.path.exists(xjz_dict_path):
    xingjinzi = pickle.load(open(xjz_dict_path, 'rb'))
else:
    xingjinzi = {}
    pickle.dump(xingjinzi, open(xjz_dict_path, 'wb'))

# 常见错误dictionary
common_dict_path = '../data/dict/common_py2.pkl'#./data/
if os.path.exists(common_dict_path):
    common = pickle.load(open(common_dict_path, 'rb'))
else:
    common = {}
    pickle.dump(common, open(common_dict_path, 'wb'))
common_mistakes = common.keys()

# 加载形近字dictionary
sims_dict_path = '../data/dict/sims_py2.pickle' # Path of similar shape characters dict
if os.path.exists(sims_dict_path):
    sims = pickle.load(open(sims_dict_path, 'rb'))
    print 'Loaded similar shape dict from file: {}'.format(sims_dict_path)
else:
    sims = {}
    pickle.dump(sims, open(sims_dict_path, 'wb'))

# 加载音近字dictionary
simp_dict_path = '../data/dict/simp_simplified_py2.pickle' # Path of similar pronunciation characters dict
if os.path.exists(simp_dict_path):
    simp = pickle.load(open(simp_dict_path, 'rb'))
    print 'Loaded similar pronunciation dict from file: {}'.format(simp_dict_path)
else:
    simp = {}
    pickle.dump(simp, open(simp_dict_path, 'wb'))


print 'Models loaded.'


#########################################################################################
#                                                                                       #
#                                  ERROR DETECTION                                      #
#                                                                                       #
#########################################################################################

def overlap(l1, l2): 
    # Detect whether two intervals l1 and l2 overlap
    # inputs: l1, l2 are lists representing intervals
    if l1[0] < l2[0]:
        if l1[1] <= l2[0]:
            return False
        else:
            return True
    elif l1[0] == l2[0]:
        return True
    else:
        if l1[0] >= l2[1]:
            return False
        else:
            return True

def get_ranges(outranges, segranges):
    # Get the overlap ranges of outranges and segranges
    # outranges: ranges corresponding to score outliers
    # segranges: ranges corresponding to word segmentation scores
    overlap_ranges = set()
    for segrange in segranges:
        for outrange in outranges:
            if overlap(outrange, segrange):
                overlap_ranges.add(tuple(segrange))
    return [list(overlap_range) for overlap_range in overlap_ranges]

def merge_ranges(ranges):
    # Merge overlapping ranges
    # ranges: list of ranges
    ranges.sort()
    saved = ranges[0][:]
    results = []
    for st, en in ranges:
        if st <= saved[1]:
            saved[1] = max(saved[1], en)
        else:
            results.append(saved[:])
            saved[0] = st
            saved[1] = en
    results.append(saved[:])
    return results

def get_score(s, model):
    '''
    Get the scores from model
    input - s: input segment (windows of words)
            model: ngram model (2,3 or 4)
    output - the score generated by the kenlm model
    '''
    return model.score(' '.join(s), bos=False, eos=False)

def get_wordmodel_score(ss):
    '''
    Get the score of word-segmented sentence from word-level language model
    input - s: input sentence
    output - the score generated by kenlm biword-gram model
    ''' 
    cuts = jieba.lcut(ss, HMM=True) #HMM: new word discovery
    seg_sentence = ' '.join(cuts)

    #print 'The segmented sentence is {}'.format(seg_sentence), end=' ')
    score = wordmodel.score(seg_sentence, bos=False, eos=False) / len(cuts) - len(cuts)
    #print 'The score is {}'.format(round(score, 4)))
    return score

def get_model(k):
    '''
    Get the model based on input k to decide the model of 'k'-gram
    input - k: k to indicate k gram
    output - the model name
    '''
    return {
        2: bimodel,
        3: trimodel,
        4: _4model,
    }.get(k, bimodel) # Return the bigram model as default

def mad_based_outlier(points, threshold=1.4):
    # points: list
    # Smaller threshold gives more outliers
    points = np.array(points)
    if len(points.shape) == 1:
        points = points[:, None]

    # get the median of all points
    median = np.median(points, axis=0) 
    # deviation from the median
    diff = np.sqrt(np.sum((points - median)**2, axis=-1))
    # median absolute deviation
    med_abs_deviation = np.median(diff) 
    z_score = 0.6745 * diff / med_abs_deviation
    
    points = points.flatten()
    outindices = np.where((z_score > threshold) & (points < median))
    outliers = points[outindices]
    #print 'Mad based outlier scores are {}'.format(outliers))
    return list(outindices[0]), outliers

def score_sentence(ss):
    '''
    scan the sentence ss with windows of sizes 2, 3, and 4 and get the sentence score respectively
    input - ss: the input sentence
    '''
    hngrams = [] # hierachical ngrams
    hscores = [] # hierachical scores
    havg_scores = [] # hierachical smoothed scores for each character

    for k in [2, 3, 4]:
        ngrams = []
        scores = []
        for i in range(len(ss) - k + 1):
            ngram = ss[i:i+k]
            ngrams.append(ngram)
            score = get_score(ngram, model=get_model(k))
            scores.append(score)

        hngrams.append(ngrams)
        zipped = zip(ngrams, [round(score, 3) for score in scores])
        # print list(zipped))
        hscores.append(scores)

        # Pad the scores list for moving window average
        for _ in range(k-1): 
            scores.insert(0, scores[0])
            scores.append(scores[-1])

        avg_scores = [sum(scores[i:i+k]) / len(scores[i:i+k]) for i in range(len(ss))]
        havg_scores.append(avg_scores)

    # average score for each character in the sentence
    per_word_scores = list(np.average(np.array(havg_scores), axis=0)) 

    outindices, _ = mad_based_outlier(np.array(list(per_word_scores)), threshold=1.2)
    if outindices:
        outranges = merge_ranges([[outindex, outindex+1] for outindex in outindices])
        print 'outranges are {}'.format(outranges)
    else:
        outranges = []
        print 'No outranges.'
    return per_word_scores, hscores, outranges


#########################################################################################
#                                                                                       #
#                                 ERROR CORRECTION                                      #
#                                                                                       #
#########################################################################################

def prepare_freq_list(inpath='../data/dict/token_freq_pos_jieba.txt'):
    '''
    construct self dict with data
    '''
    word_freq = {}
    with open(inpath, 'r') as f:
        for line in f:
            info = line.split()
            word = info[0]
            frequency = info[1]
            word_freq[word] = frequency
        return word_freq

def prepare_dict(inpath='../data/dict/cn_dict.txt'):
    '''
    use the word in this dict to replace the words in given phrases
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
    phrase = phrase#.decode('utf-8')
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
    print c1_order, c2_order
    if c1_order:
        return max(c1_order, key=word_freq.get )
    elif c2_order:
        return max(c2_order, key=word_freq.get )
    else:
        return error_phrase

def get_wordmodel_score(ss):
    # Get the score of word-segmented sentence from word-level language model
    cuts = jieba.lcut(ss, HMM=True)
    seg_sentence = ' '.join(cuts)
    ####print 'The segmented sentence is {}'.format(seg_sentence), end=' ')
    score = wordmodel.score(seg_sentence, bos=False, eos=False) / len(cuts) - len(cuts)
    ####print 'The score is {}'.format(round(score, 4)))
    return score

def getf(char):
    try:
        counter[char] / total
    except:
        ####print total)
        return 0
    return counter[char] / total

def get_xingjinzi(in_char):
    return set(xingjinzi.get(in_char, []))

def get_simpronunciation(in_char):
    return simp.get(in_char, set())

def gen_chars(in_char, frac=2):
    # Get confusion characters of in_char from the confusion sets
    # frac: get top 1/frac in terms of character frequency
    chars_set = get_simpronunciation(in_char).union(get_xingjinzi(in_char))
    if not chars_set:
        chars_set = {in_char}
    chars_set.add(in_char)
    chars_list = list(chars_set)
    return sorted(chars_list, key=lambda k: getf(k), reverse=True)[:len(chars_list)//frac+1]

def correct_ngram_2(ss, st, en):
    # Correct the ngram character by character
    # Returns the corrected ngram
    mingram = ss[st:en]
    for i, m in enumerate(mingram):
        mc = gen_chars(m) # Possible corrections for character m in mingram
        print 'Number of possible replacements for {} is {}'.format(m, len(mc))
        print mc
        mg = max(mc, key=lambda k: get_wordmodel_score(ss[:st] + mingram[:i] + k + mingram[i+1:] + ss[en:]) + math.log(5)**(k == m))
        mingram = mingram[:i] + mg + mingram[i+1:]
    return mingram

def correct(ss):
    '''
    Correct sentence ss
    '''
    freq_file = '../data/dict/token_freq_pos_jieba.txt'
    word_freq = prepare_freq_list(freq_file)
    cn_dict_file = '../data/dict/cn_dict.txt'
    cn_dict = prepare_dict(cn_dict_file)

    # Returns list of tuples (word, st, en)  mode='search'
    tokens = list(jieba.tokenize(ss))
    ss = ss.encode('utf-8')
    print 'Segmented sentence is {}'.format(''.join([str(token).decode().encode('utf=8') for token in tokens]))

    segranges = [[token[1], token[2]] for token in tokens]
    _, _, outranges = score_sentence(ss)
    if outranges:
        correct_ranges = merge_ranges(get_ranges(outranges, segranges))
        for correct_range in correct_ranges:
            print 'Correct range is {}'.format(correct_range)
            st, en = correct_range
            print 'Possible wrong ngram is {}'.format(ss[st:en])
            possible_wrong = ss[st:en]
            # seg_list = jieba.cut(possible_wrong)
            # error_string = ", ".join(seg_list)
            # errors = error_string.split(", ")
            # cgram = ""
            # for error in errors:
            cgram = auto_correct(possible_wrong, cn_dict, word_freq)
            ss = ss[:st] + cgram + ss[en:]
            print 'Corrected ngram 1 is {}'.format(cgram)
            cgram2 = correct_ngram_2(ss, st, en)
            print 'Corrected ngram 2 is {}'.format(cgram2)
            ss = ss[:st] + cgram2 + ss[en:]
    else:
        correct_ranges = []
        print 'No ngram to correct.'
    return ss, correct_ranges


#########################################################################################
#                                                                                       #
#                                    TEST / MAIN                                        #
#                                                                                       #
#########################################################################################

def main():
    # Load data
    processed_file = '../data/sighan/processed/sighan15_A2_training_py2.pkl'
    dataset = pickle.load(codecs.open(processed_file, 'rb')) # Loads a list of tuples: [(PASSAGE, [(location, wrong, correction)])]
    total_errors = 0
    reported_errors = 0
    detected_errors = 0
    for entry in dataset:
        # Error detection
        sentence, spelling_errors = entry
        print 'The sentence is {}'.format(sentence.encode('utf-8'))
        # Error correction
        corrected_ss, correct_ranges = correct(sentence)
        reported_errors += len(correct_ranges)
        print 'Corrected sentence is {}'.format(corrected_ss.encode('utf-8'))
        # Reference
        for spelling_error in spelling_errors:
            total_errors += 1
            location, wrong, correction = spelling_error
            print '{} at {} should be {}'.format(wrong.decode('utf-8').endoce('utf-8'), location, correction)
            for correct_range in correct_ranges:
                if location >= correct_range[0] and location < correct_range[1]:
                    detected_errors += 1
        print '-------------------------------------------------------------------------------------'
    print 'Number of total errors is {}'.format(total_errors) # Total number of errors in the ground truth labelled data
    print 'Number of detected errors is {}'.format(detected_errors) # Number of errors correctly detected by the algorithm
    print 'Number of reported errors is {}'.format(reported_errors) # Total number of errors reported by the algorithm


if __name__=='__main__':
    main()
