# -*- coding: UTF-8 -*-


"""
preprocess.core
~~~~~~~~~~
Core components for emoji.
"""


import re
import sys
import emoji
import string

from emoji import unicode_codes

from text_cleaner import remove, keep
from text_cleaner.processor.common import ASCII, SYMBOLS_AND_PUNCTUATION_EXTENSION, GENERAL_PUNCTUATION
from text_cleaner.processor.chinese import CHINESE, CHINESE_SYMBOLS_AND_PUNCTUATION
from text_cleaner.processor.misc import RESTRICT_URL


__all__ = ['emojize', 'demojize', 'get_emoji_regexp','emoji_lis']


PY2 = sys.version_info[0] is 2

_EMOJI_REGEXP = None
_DEFAULT_DELIMITER = ":"

def escape_special(string):
    tag_pattern = u"\u0023+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0023"
    id_pattern = u"\u0040+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u003A"
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    mail_pattern = "^\\s*\\w+(?:\\.{0,1}[\\w-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\\.[a-zA-Z]+\\s*$"
    other_emoji = u"\[+[\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\]"
    url_pattern1 = "//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    pattern = tag_pattern+'|'+id_pattern+'|'+url_pattern+'|'+mail_pattern+'|'+other_emoji+'|'+url_pattern1

    one_str = re.sub(pattern, ' ', string)
    return one_str

def preprocess_filter(inpath, outpath):
    sys.stdout = open(outpath, 'wt')  
    with open(inpath, 'r') as f:
        lines = f.readlines()

    tag_pattern = u"\u0023+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u0023"
    id_pattern = u"\u0040+[\w\W\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\u003A"
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    mail_pattern = "^\\s*\\w+(?:\\.{0,1}[\\w-]+)*@[a-zA-Z0-9]+(?:[-.][a-zA-Z0-9]+)*\\.[a-zA-Z]+\\s*$"
    other_emoji = u"\[+[\u0020-\u007f\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff]+?\]"
    url_pattern1 = "//(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    pattern = tag_pattern+'|'+id_pattern+'|'+url_pattern+'|'+mail_pattern+'|'+other_emoji+'|'+url_pattern1

    line = ' '.join(lines)
    content = line
        #TODO: escape tag/id/url/mail
    filtered = re.sub(pattern, '', content)
    print(filtered)

def escape_emoji(string):
    new_str = ''
    for i in string:
        if i not in emoji.UNICODE_EMOJI:
            new_str = new_str + i
        else:
            new_str = new_str + '.'
    return new_str
  
def escape_emoji_file(inpath, outpath):
    """
    escape_emoji_file(path5, path6)
    """
    with open(inpath, 'r') as f:
        txt = f.readlines()              
    sys.stdout = open(outpath, 'wt')  
    one_str = ''.join(escape_emoji(c) for c in txt)
    print (one_str)

def escape_en_char(string):
    en_pattern = "[a-zA-Z0-9]+"
    one_str = re.sub(en_pattern, ' ', string)
    return one_str

def escape_en_file(inpath, outpath):
    """
    escape_en_file(path6, path7)
    """
    with open(inpath, 'r') as f:
        txt = f.readlines()              
    sys.stdout = open(outpath, 'wt')  
    one_str = ''.join(escape_en_char(c) for c in txt)
    print (one_str)

def escape_flag(text):
    """
    t = "高考、考研？ 从学德语到德国留学有多远？ 多会一门语言就业薪酬几何？ 🇩🇪🇫🇷🇯🇵🇰🇷🇪🇸🇮🇹🇷🇺"
    print(escape_flag(t))
    """
    emoji_pattern = re.compile(
        u'(\U0001F1F2\U0001F1F4)|'       # Macau flag
        u'([\U0001F1E6-\U0001F1FF]{2})|' # flags
        u'([\U0001F600-\U0001F64F])'     # emoticons
        "+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def escape_flag_file(inpath, outpath):
    """
    escape_flag_file(outpath7, outpath8)
    """
    with open(inpath, 'r') as f:
        txt = f.readlines()              
    sys.stdout = open(outpath, 'wt')  
    one_str = ''.join(escape_flag(c) for c in txt)
    print (one_str)

def escape_punc(string):
    s = CHINESE_SYMBOLS_AND_PUNCTUATION.remove(string)
    s = SYMBOLS_AND_PUNCTUATION_EXTENSION.remove(s)
    s = GENERAL_PUNCTUATION.remove(s)
    return s

def escape_punc_file(inpath, outpath):
    """
    escape_flag_file(outpath7, outpath8)
    """
    with open(inpath, 'r') as f:
        txt = f.readlines()              
    sys.stdout = open(outpath, 'wt')  
    one_str = ''.join(escape_punc(c) for c in txt)
    print (one_str)

def join_space(string):
    #TODO1: join multiple space
    string = ' '.join(string.split())
    return string
    
def join_space_file(inpath, outpath):
    with open(inpath, 'r') as f:
        txt = f.readlines()              
    sys.stdout = open(outpath, 'wt') 
    for c in txt:
        newline = ''.join(join_space(c))
        print (newline)

def handle_5gram(inpath, outpath):
    numeric_const_pattern = "[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?"
    with open(inpath, 'r') as f:
        txt = f.readlines()
    sys.stdout = open(outpath, 'wt')
    for c in txt:  
        one_str = re.sub(numeric_const_pattern, ' ', c)
        one_str = ''.join(one_str.split())
        print (one_str)

if __name__ == '__main__':
    inpath = '../data/2_preprocessed'
    outpath2 = '../data/2_preprocessed_nospecial'
    path5 = '../data/3_filtered_withEn'
    path6 = '../data/6_clean_emoji'
    outpath6 = '../data/6_preprocessed_noemoj;'
    path7 = '../data/7_clean_english'
    outpath7 = '../data/7_preprocessed_english'
    path8 = '../data/8_clean_flag'
    outpath8 = '../data/8_preprocessed_flag'
    outpath88 = '../data/8_preprocessed_flag_space'
    outpath9 = '../data/9_preprocessed_punc'
    outpath10 = '../data/10_preprocessed_space'

    #test = "关于《国家税务总局关于水资源费改税 后城镇公共供水企业增值税发票开具问题的公告 》的解读 根据《财政部 税务总局 水利部关于印发<扩大水资源税改革试点实施办法>的通知》（ 财税〔 〕 号），自 年 月 日起在北京、天津、山西、内蒙古、山东、河南、四川、陕西、宁夏 个省份..."
    #join_space_file(outpath8, outpath88)

    fiveg = '../data/weibo_5gram.data'
    outpathg = '../data/weibo_segment.data'
    handle_5gram(fiveg, outpathg)
    # s = "🇩🇪-9223330358968196918#1516422278 消防车🚒//@app菌:哈哈哈哈哈哈哈哈 谈个恋爱还不够生气的//@一个阿呆仔:学猪叫那个真笑出猪声[允悲]//@梨 园西池水: 哈哈哈哈哈哈哈哈哈哈//@太皇太后您有喜啦:哈哈哈哈哈哈哈哈哈怎么这么好笑ˊ_>ˋ"
    # print(s)
    # s = escape_emoji(s)
    # print(s)
    # s = escape_en_char(s)
    # print(s)
    # s = CHINESE_SYMBOLS_AND_PUNCTUATION.remove(s)
    # print(s)
    # s = SYMBOLS_AND_PUNCTUATION_EXTENSION.remove(s)
    # s = GENERAL_PUNCTUATION.remove(s)
    # print(s)
    # s = escape_flag(s)
    # print(s)
    # s = join_space(s)
    # print(s)




