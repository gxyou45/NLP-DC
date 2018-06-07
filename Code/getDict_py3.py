#encoding=utf-8
##########################################################################################
#
#file to preprocess the weibo data and get a frequency list from weibo data based on jieba
#
##########################################################################################
import json
import re
import pandas
#from opencc import OpenCC
import emoji
import jieba
from collections import Counter

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
  #  openCC = OpenCC('t2s')


    for line in lines:
        content = line[1]

        #TODO1: function should take in *content* from the above line
        #traditional chinese to simpler chinese & Capital letter to non-capital
        #save in 2_preprocessed
 #       content = openCC.convert(content).lower()        
        processed = content # the thing to be saved

        info = '%s\t%s' % (line[0].encode('utf-8'), processed.encode('utf-8'))
        print >> outfile, info

def get_all_in_one(inpath, outpath):
    outfile = open(outpath, 'w')
    lines = get_lines(inpath)
    content = []
    for line in lines:
        if len(line) >= 2:
            content.append(line[1].decode('utf=8'))
    one_str = ''.join(content)
    one_str = one_str.encode('utf-8')
    print >> outfile, content

def preprocess_filter(inpath, outpath):
    #outfile = open(outpath, 'r+b')
    lines = get_lines(inpath)
    content = []
    for line in lines:
        if len(line) >= 2:
            content.append(line[1].decode('utf-8'))
    print type(content)
    one_str = ''.join(content)

    print "Finish joining to one string\n"

    tag_pattern = u"\u0023+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0023"
    id_pattern = u"\u0040+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u003A"
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    mail_pattern = "^\\s*\\w+(?:\\.{0,1}[\\w-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\\.[a-zA-Z]+\\s*$"
    other_emoji = u"\[+[\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\]"
    url_pattern1 = "//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    pattern = tag_pattern+'|'+id_pattern+'|'+url_pattern+'|'+mail_pattern+'|'+other_emoji+'|'+url_pattern1
    
    print "Finish defining patterns\n"
    
    #TODO1: join multiple space
    print "Deleting continuous spaces...\n"
    one_str = ' '.join(one_str.split())
    
    #TODO2: escape emoji
    print "Escaping emoji...\n"
    one_str = ''.join(c for c in one_str if c not in emoji.UNICODE_EMOJI)

    #TODO3: escape tag/id/url/mail
    print "Escaping tag/id/url/mail...\n"
    one_str = re.sub(pattern, '', one_str)
    
    #TODO4: escape num
    print "Escapting num...\n"
    filtered = re.sub('\d+', '', one_str)
    info = filtered.encode('utf-8')
    #info = '%s\t%s' % (line[0].encode('utf-8'), filtered.encode('utf-8'))
    print "Writing to output\n"
    outfile = open(outpath, 'w')
    #print >> outfile, info
    for ch in info:
        outfile.write(str(ch))

def get_words(inpath, outpath):
    #txt = get_lines(inpath)
    #print(type(txt))
    with open(inpath, 'r') as f:
        txt1 = f.readlines()
    #print(type(txt1))
    txt2 = ''.join(txt1)
    seg_list = jieba.cut(txt2)
    outfile = open(outpath, 'w')
    c = Counter()
    for x in seg_list:
        if len(x)>1 and x != '\r\n':
            c[x] += 1
    print("Finish building freq list, writing to file...\n")
    
    for (k,v) in c.most_common():
        info = '%s\t%s' % (k.encode('utf-8'), v)
        print >> outfile, info
    #with codecs.open(outpath, 'w', 'utf8') as f:
    #return seg_list

def filter_emoji(inpath, outpath):
    tag_pattern = u"\u0023+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0023"
    id_pattern = u"\u0040+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u003A"
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    mail_pattern = "^\\s*\\w+(?:\\.{0,1}[\\w-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\\.[a-zA-Z]+\\s*$"
    other_emoji = u"\[+[\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\]"
    url_pattern1 = "//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    pattern = tag_pattern+'|'+id_pattern+'|'+url_pattern+'|'+mail_pattern+'|'+other_emoji+'|'+url_pattern1

    with open(inpath, 'r') as f:
        txt = f.readlines()
    #outfile = open(outpath, 'w')    
    #TODO2: escape emoji
    print "Handling emoji...\n"
    #one_str = ''.join(re.sub(r'[^\w\s,]', '.', c) for c in txt)
    emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
    a_list='🤔 🙈 me así,bla es,se 😌 ds 💕👭👙'
    for d in a_list:
        if d in emojis_list: 
            print d
    #one_str = ''.join(c for c in txt if c not in emoji.UNICODE_EMOJI)
    #two_str = ''.join(d for d in txt if d in emoji.UNICODE_EMOJI)
    #print two_str
    #print "Escaping other emoji...\n"
    #one_str = re.sub(other_emoji, '', one_str)

    #print >> outfile, one_str


def extract_emojis(s):
    emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
    r = re.compile('|'.join(re.escape(p) for p in emojis_list))
    print(' '.join(re.findall(s)))

if __name__ == '__main__':
    inpath = 'data/chinese_word_correction_data.json'
    path1 = 'data/1_out'
    path2 = 'data/2_preprocessed'
    path3 = 'data/3_filtered'
    path4 = 'data/4_freqlist'
    path5 = '../data/3_filtered_withEn'
    path6 = '../data/5_clean_emoji'
    # parses the raw data into "key:contents"
    # step1: get text
    # parse(inpath, path1)
    # step2: tranditional chinese to simplfied chinese
    # preprocess(path1, path2)
    # step3: filter and merge
    # preprocess_filter(path2, path3)
    # step4: count the frequency
    #filter_emoji(path5, path6)
    #filter_emoji(path5,path6)
    emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
    a_list=''.join('🤔 🙈 me así,bla es,se 😌 ds 💕👭👙')
    print a_list
    for d in a_list:
        if d.encode in emojis_list: 
            print d
    # DEMO -- to check how it looks like 
    # use it as below
    #lines = get_lines(path4)
    #for idx, line in enumerate(lines):
    #    if idx>10:
    #        break
    #    print len(line), line[0]#, line[1]
    #    break 

    
    #preprocess(path1, path2)
