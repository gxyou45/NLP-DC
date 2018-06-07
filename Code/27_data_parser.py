import pandas as pd
import codecs 


def baidu_10000_2df():
    path = 'data/baidu_10000.txt'
    f = codecs.open(path, 'r')
    data = f.read().split('\r')
    header = data[0].split('\t')
    result = []
    for i in range(1,len(data)):
	result.append(data[i].split('\t'))
    df = pd.DataFrame(result, columns=header)
    print 'Shape of dataframe generated by baidu_10000: ', df.shape
    #print df.columns
    #print df[header[0]]
    return df


def baidu_10000_2list():
    """Returns a list of strings, which are corrected sentences.
    """
    df = baidu_10000_2df()
    result_idx = df.columns[-1]
    result = []
    N = len(df)
    for i in range(N):
        line = df.iloc[i]
        info = line[2-int(line[result_idx])] 
        result.append(info)
        print info 
    #print type(result)
    #print len(result) 
    return result    



def sogo_internet_2list(path):
    f = codecs.open(path, 'r')
    data = f.read().split('\n')
    result = []
    for i in range(len(data)):
        if i % 2 == 0:
            info = data[i].split('\t')[0]
            result.append(info)          
    #print 'Number of lines in Sogo_internet.txt: ', len(result)
    return result


def gen_label_internet():
    data_internet = sogo_internet_2list('data/sogo_internet.txt')
    data_drama_movies = sogo_internet_2list('data/sogo_drama_movies.txt')
    
    for i in range(len(data_internet)):
        data_label = [datalist[i], [1,0,0]]
    df = pd.DataFrame(data_label,columns=['X_string','Y'])


def gen_corpus(frompath):
    f = open(frompath, 'r')
    for line in f:
        print line.split('\t')[-1].strip('\n')
 
if __name__ == '__main__':
    #baidu_10000_2list()
    #sogo_internet_2list('data/else.txt')
    #gen_corpus('data/S_WithoutError_10001-10350.txt')
    pass
