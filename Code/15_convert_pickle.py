#!/usr/bin/env python3

import pickle

files = []
files.append('./data/xjz.pkl')
files.append('./data/common.pkl')
files.append('./data/sims.pickle')
files.append('./data/simp_simplified.pickle')

with open(files[0], "rb") as f:
        w = pickle.load(f)

pickle.dump(w, open('./data/xjz_py2.pkl',"wb"), protocol=2)
with open(files[1], "rb") as f:
        w = pickle.load(f)

pickle.dump(w, open('./data/common_py2.pkl',"wb"), protocol=2)
with open(files[2], "rb") as f:
        w = pickle.load(f)

pickle.dump(w, open('./data/sims_py2.pickle',"wb"), protocol=2)
with open(files[3], "rb") as f:
        w = pickle.load(f)

pickle.dump(w, open('./data/simp_simplified_py2.pickle',"wb"), protocol=2)