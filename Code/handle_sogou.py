#encoding=utf-8
import re
import pandas
import emoji
import jieba
from collections import Counter

def write_words_with_jieba(inpath, outpath):
    jieba.initialize()
    jieba.load_userdict("list/words_newjieba.data")
    outfile = open(outpath, 'w')
    with open(inpath, 'r') as f:
        lines = f.readlines()
    for line in lines:
        seg_list = jieba.cut(line.decode('utf-8'))
        word = ' '.join(seg_list)
        print word
        info = word.encode('utf-8')
        print >> outfile, info

def write_words_with_space(inpath, outpath):
    outfile = open(outpath, 'w')
    with open(inpath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        content = " ".join(line.decode('utf-8'))
        print >> outfile, content.encode('utf-8')

if __name__ == '__main__':
    inpath = 'finally.txt'
    outpath = 'finally_with_jieba.txt'
    write_words_with_jieba(inpath, outpath)