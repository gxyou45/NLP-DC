# -*- coding: utf-8 -*-
from gensim.corpora import WikiCorpus

if __name__ == '__main__':
	input_file = "../data/zhwiki-latest-pages-articles.xml.bz2" 
	output_file = "data/zhwiki-latest.txt"
	outfile = open(output_file, 'w')

	wiki = WikiCorpus(input_file, lemmatize=False, dictionary={}) 
	for text in wiki.get_texts(): 
		str_line = bytes.join(b' ', text).decode()
		print >> outfile, str_line