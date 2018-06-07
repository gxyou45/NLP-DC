# -*- coding: utf-8 -*-
from langconv import *

def t2s(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

def readfile(inpath):
    for line in open(inpath, 'r'):
        yield line


def parser(inpath, outpath):
    lines = readfile(inpath)
    NID = 'Nid'
    WRONGPOS = 'wrong_position'
    outfile = open(outpath, 'w')
    for line in lines:
        try: 
            if NID in line: 
    	        Nid = line.split('"')[1]
            elif ('<P>' in line) and ('</P>' in line): 
                traditional = line[3:-5].decode('utf-8')
                simplified = t2s(traditional)
            elif WRONGPOS in line:
                wrong_position = line.split('=')[1][:-2]
                info = '%s\t%s\t%s' % (Nid, wrong_position, simplified)
                print >> outfile, info.encode('utf-8')
        except:
            print line

if __name__ == "__main__":
    inpath1 = 'SampleSet/Bakeoff2013_SampleSet_WithError_00001-00350.txt'
    outpath1 = 'SampleSet/S_WithError_00001-00350.txt'
    inpath2 = 'SampleSet/Bakeoff2013_SampleSet_WithoutError_10001-10350.txt'
    outpath2 = 'SampleSet/S_WithoutError_10001-10350.txt'

    parser(inpath1, outpath1)
    parser(inpath2, outpath2)




