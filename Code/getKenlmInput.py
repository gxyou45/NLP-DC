# -*- coding: utf-8 -*-
import sys
import jieba
import string
import re

def parse(inpath, outpath):
    """ Takes in a list of dictionaries, where each dictionary contains information in a weibo. 
        Parses the raw data into 'key:contents', where key is in the format of 'uid#pubTime'
    """
    with open(inpath) as infile:
        data = json.load(infile)

    outfile = open(outpath, 'w')
    for d in data:
        #key = '%s#%s' % (d[u'id'], d[u'pubTime'])
        info = '%s\t%s' % (d[u'content'].encode('utf-8'))
        print >> outfile, info

def get_words(inpath, outpath):
    with open(inpath, 'r') as f:
        data = f.readlines()
    
    outfile = open(outpath, 'w')
    for d in data:
        seg_list = jieba.cut(d)
        word = ' '.join(seg_list)
        word = ' '.join(word.split())
        #print word
        info = word.encode('utf-8')
        print >> outfile, info
    
def get_chars(inpath, outpath):
    with open(inpath, 'r') as f:
        data = f.readlines()
    
    outfile = open(outpath, 'w')
    for d in data:
        word = ' '.join(d.decode('utf-8'))
        word = ' '.join(word.split())
        #print word
        info = word.encode('utf-8')
        print >> outfile, info

if __name__ == '__main__':
    inpath = '../data/finally.txt'
    outpath = '../data/finalbaidu_with_space'
    outpath1 = '../data/finalbaidu_with_jieba'
    get_chars(inpath, outpath)
    get_words(inpath, outpath1)
