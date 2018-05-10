#encoding=utf-8
#from pymongo import MongoClient
import json
import re
import pandas
from opencc import OpenCC
import emoji

def parse(inpath, outpath):
    """ Takes in a list of dictionaries, where each dictionary contains information in a weibo. 
        Parses the raw data into 'key:contents', where key is in the format of 'uid#pubTime'
    """
    with open(inpath) as infile:
        data = json.load(infile)

    outfile = open(outpath, 'w')
    for d in data:
        key = '%s#%s' % (d[u'id'], d[u'pubTime'])
        info = '%s\t%s' % (key.encode('utf-8'), d[u'content'].encode('utf-8'))
        print >> outfile, info


def get_lines(inpath):
    for line in open(inpath, 'r'):
        yield line.split('\t')


def preprocess_t2s(inpath, outpath):
    outfile = open(outpath, 'r+b')
    lines = get_lines(inpath) #generator
    
    #define opencc converter
    openCC = OpenCC('t2s')


    for line in lines:
        content = line[1]

        #TODO1: function should take in *content* from the above line
        #traditional chinese to simpler chinese & Capital letter to non-capital
        #save in 2_preprocessed
        content = openCC.convert(content).lower()        
        processed = content # the thing to be saved

        info = '%s\t%s' % (line[0].encode('utf-8'), processed.encode('utf-8'))
        print >> outfile, info


def preprocess_filter(inpath, outpath):
    outfile = open(outpath, 'r+b')
    lines = get_lines(inpath)

    tag_pattern = u"\u0023+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0023"
    id_pattern = u"\u0040+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u003A"
    #title_pattern = u"\u0030+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0031"
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    mail_pattern = "^\\s*\\w+(?:\\.{0,1}[\\w-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\\.[a-zA-Z]+\\s*$"
    other_emoji = u"\[+[\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\]"
    pattern = tag_pattern+'|'+id_pattern+'|'+url_pattern+'|'+mail_pattern+'|'+other_emoji
 
    content = content.decode('utf-8')
    
    #TODO1: join multiple space
    content = ' '.join(content.split())

            #TODO2: escape emoji
            content = ''.join(c for c in content if c not in emoji.UNICODE_EMOJI)

            #TODO3: escape tag/id/url/mail
            filtered = re.sub(pattern, '', content)
            print(filtered)
        
            info = '%s\t%s' % (line[0].encode('utf-8'), filtered.encode('utf-8'))
            print >> outfile, info


if __name__ == '__main__':
    inpath = '../data/chinese_word_correction_data.json'
    path1 = '1_out'
    path2 = '2_preprocessed'
    path3 = '3_filtered'
    # parses the raw data into "key:contents"
    # step1
    # parse(inpath, path1)
    # step2
    # preprocess(path1, path2)
    # step3
    preprocess_filter(path2, path3)
    # DEMO -- to check how it looks like 
    # use it as below
    lines = get_lines(path2)
    for line in lines:
        print len(line), line[0], line[1]
        break 

    
    #preprocess(path1, path2)
