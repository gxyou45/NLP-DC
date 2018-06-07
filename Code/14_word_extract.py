import re
import emoji
from text_cleaner import remove
from text_cleaner.processor.common import ASCII, SYMBOLS_AND_PUNCTUATION_EXTENSION, GENERAL_PUNCTUATION
from text_cleaner.processor.chinese import CHINESE, CHINESE_SYMBOLS_AND_PUNCTUATION
import math
import sys

emoji_pattern = re.compile(
        u'(\U0001F1F2\U0001F1F4)|'       # Macau flag
        u'([\U0001F1E6-\U0001F1FF]{2})|' # flags
        u'([\U0001F600-\U0001F64F])'     # emoticons
        "+", flags=re.UNICODE)
en_pattern = "[a-zA-Z0-9]+"

def preprocess(s):
    new_str = ''
    for i in s:
        # remove emoji
        if i not in emoji.UNICODE_EMOJI:
            new_str = new_str+i
    new_str = emoji_pattern.sub('', new_str)
    new_str = re.sub(en_pattern,'', new_str)
    new_str = SYMBOLS_AND_PUNCTUATION_EXTENSION.remove(new_str)
    new_str = GENERAL_PUNCTUATION.remove(new_str)
    new_str = CHINESE_SYMBOLS_AND_PUNCTUATION.remove(new_str)
    new_str = ' '.join(new_str.split())
    return new_str

def get_segment(s):
    words = []
    slist = s.split(' ')
    # print(slist)
    for segment in slist:
        segment = "$" + segment + "$"
#        for i, char in enumerate(segment):
#             for j in range(i+1, i+maxlen+1):
#                 if j > len(segment):
#                     break
#                 w = segment[i:j]
#                 print("1:",w)
#                 words.append(w) 
        for j in range(1, len(segment)-1):
            w = segment[j: min(maxlen + j,  len(segment))]
            words.append(w) 
    return words

def getRight(ngramsort):
    outpath = "../data/freqright.data"
    sys.stdout = open(outpath, 'wt')
    ngram = ""
    pause = False
    sameWord = []
    for curr in ngramsort:
    #     print("curr", curr)
        if pause:
            break
        if ngram == "":
            sameWord.append(curr)
            ngram = curr
        else:
            if curr.startswith(ngram):
                sameWord.append(curr)
    #             print("1",sameWord)
            else:
                if not sameWord: # sameword is empty
                    pause = False
                    sameWord.append(curr)
                    ngram = curr
                    continue
                right = {}
                freq = 0
                for w in sameWord:
                    if w.startswith(ngram) == False:
                        break
                    if w == ngram:
                        continue
                    freq += 1
                    neww = w[:len(ngram)-1]
                    right[neww] = right.get(neww, 0) + 1
                res= 0.0
                for t in right.keys():
                    p = right[t] * 1.0 / freq
                    res += -1 * p * math.log(p)
                print(ngram,freq,res)
                newlist = []
                for w in sameWord:
                    if w != ngram:
                        newlist.append(w)
                sameWord = newlist
                if not sameWord:
                    pause = False
                    sameWord.append(curr)
                    ngram = curr
                    continue
                ngram = sameWord[0]
                if curr.startswith(ngram):
                    sameWord.append(curr)
                else:
                    pause = True

def getLeft(revngramsort):
    outpath = "../data/freqleft.data"
    sys.stdout = open(outpath, 'wt')
    ngram = ""
    pause = False
    sameWord = []
    for curr in revngramsort:
    #     print("curr", curr)
        if pause:
            break
        if ngram == "":
            sameWord.append(curr)
            ngram = curr
        else:
            if curr.startswith(ngram):
                sameWord.append(curr)
                pause = False
    #             print("1",sameWord)
            else:
                if not sameWord: # sameword is empty
                    pause = False
                    sameWord.append(curr)
                    ngram = curr
                    continue
                left = {}
                freq = 0
                for w in sameWord:
                    if w.startswith(ngram) == False:
                        break
                    if w == ngram:
                        continue
                    freq += 1
                    neww = w[:len(ngram)-1]
                    left[neww] = left.get(neww, 0) + 1
                res= 0.0
                for t in left.keys():
                    p = left[t] * 1.0 / freq
                    res += -1 * p * math.log(p)
                print(ngram,freq,res)
                newlist = []
                for w in sameWord:
                    if w != ngram:
                        newlist.append(w)
                sameWord = newlist
                if not sameWord:
                    pause = False
                    sameWord.append(curr)
                    ngram = curr
                    continue
                ngram = sameWord[0]
                if curr.startswith(ngram):
                    sameWord.append(curr)
                else:
                    pause = True

def mergeEntropy(rightpath, leftpath):
    
    with open(rightpath, 'r') as rf:
        rightline = rf.readlines() 
    with open(leftpath, 'r') as lf:
        leftline = lf.readlines() 
        
    outpath = "../data/merge.tmp"
    sys.stdout = open(outpath, 'wt')
    newlines = rightline + leftline
    for line in rightline:
        print(line)
    for line in leftline:
        print(line)
        
    sortFile(mergetmp, mergetmp2)
    
    outpath = "../data/merge_entropy.data"
    sys.stdout = open(outpath, 'wt')
    f = open(mergetmp2, 'r')
    line1 = ""
    line2 = ""
    line1 = f.readline()
    line2 = f.readline()
    while True:
        if line1 == "" or line2 == "":
            break
        seg1 = line1.split("\t")
        seg2 = line2.split("\t")
        if seg1[0] != seg2[0]
            line1 = line2
            line2 = f.readline()
            continue
        if len(seg1) < 2:
            line1 = line2
            line2 = f.readline()
            continue
            
        le = float(seg1[1]) if len(seg1) == 2 else float(seg2[1])
        re = float(seg1[2]) if len(seg1) == 3 else float(seg2[2])
        freq = int(seg1[1]) if len(seg1) == 3 else int(seg2[1])
        print(seg1[0],freq, e)
        line1 = f.readline()
        line2 = f.readline()

def extractWords(freqFile, entropyFile):
    with open(freqFile, 'r') as f:
        fr = f.readlines() 
    with open(entropyFile, 'r') as f:
        er = f.readlines() 
    
    outpath = "words.data"
    sys.stdout = open(outpath, 'wt')
    
    freq = {}
    for line in fr:
        seg = line.split("\t")
        if len(seg) < 3:
            continue
        freq[seg[0]] = int(seg[1])
    
    for line in er:
        seg = line.split("\t")
        if len(seg) == 3:
            continue
        w = seg[0]
        f = int(seg[1])
        e = float(seg[2])
        max = -1
        for s in range(1, len(w)):
            lw = w[:s]
            rw = w[s:]
            if lw not in freq.keys() or rw not in freq.keyw():
                continue
            ff = freq[lw] * freq[rw]
            if ff > max:
                max = ff
        pf = f * 200000.0 / max
        if pf < 10 or e < 2:
            continue
        print(w, pf, e)

def main():
    s = "🇩🇪-消防车🚒//@app菌:哈哈哈哈哈哈哈哈 谈个恋爱还不够生气的//@一个阿呆仔:学猪叫那个真笑出猪声[允悲]//@梨 园西池水: 哈哈哈哈哈哈哈哈哈哈//@太皇太后您有喜啦:哈哈哈哈哈哈哈哈哈怎么这么好笑ˊ_>ˋ"
    s = preprocess(s)
    maxlen = 5
    seqlen = len(s)
    segmentList = get_segment(s)
    ngramsort = sorted(segmentList)
    getRight(ngramsort)
    revngramsort = [c[::-1] for c in ngramsort]
    getLeft(revngramsort)
    mergeEntropy("../data/freqright.data", "../data/freqleft.data")
    freqFile = "../data/freq.data"
    entropyFile = "../data/entropy.data"
    extractWords(freqFile, entropyFile)

if __name__ == '__main__':
    main()