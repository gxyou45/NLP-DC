import os
import pickle as pk


fpath = './correction-master/data/token_freq_pos_jieba.txt'
topath = './correction-master/data/counter_jieba.pkl'

counter = dict()
with open(fpath) as f:
    for line in f: 
        info = line.split()
        counter[info[0]] = int(info[1])
print(len(counter.keys()))
pk.dump(counter, open(topath, 'wb'))
        
