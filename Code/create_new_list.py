#encoding=utf-8
import re
import pandas
import emoji
import jieba
from collections import Counter

def get_lines(inpath):
    for id, line in enumerate(open(inpath, 'r')):
        if id is 1:
            print line.split('\t')
        yield line.split('\t')

def get_words(inpath, outpath):
    outfile = open(outpath, 'w')
    with open(inpath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        content = line.split('\t')

        info = '%s\t%s' % (content[0].decode('utf-8').encode('utf-8'), content[1].decode('utf-8').encode('utf-8'))
        print >> outfile, info

if __name__ == '__main__':
    inpath = 'words_sort.data'
    outpath = 'words_newjiba.data'
    get_words(inpath, outpath)