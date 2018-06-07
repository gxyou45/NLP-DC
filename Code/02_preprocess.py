import jieba
import jieba.posseg as pseg

inpath1 = 'SampleSet/S_WithError_00001-00350.txt'
inpath2 = 'SampleSet/S_WithoutError_10001-10350.txt'

def readfile(inpath):
    for line in open(inpath, 'r'):
        elems = line.split('\t')
        yield elems

def cut(line,cut_all=True, HMM=True):
    line = line.strip()
    seglist = jieba.cut(line, cut_all=cut_all, HMM=HMM)
    print '|'.join(seglist)
    return seglist 


if __name__ == '__main__':
    lines = readfile(inpath1)
    for line in lines:
        inputstr = line[2]
        seglist = cut(inputstr, False)    
        postag = jieba.posseg.cut(inputstr)
        for i in postag:
            print i
        exit()



