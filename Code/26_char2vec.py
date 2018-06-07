#-*- coding: utf-8 -*-
from gensim.models import Word2Vec
import numpy as np

def corpus2list(inpath):
    """Loads corpus from inpath file, returns a list of sentences.
    """
    sentences = list()
    with open(inpath) as f:
        for line in f:
            sentences.append(line)
    return sentences 


def sent2model(sentences):
    """Returns a model trained on a character-level, with the input sentences. 
        Input:
         sentences - a list of strings of characters. 
    """
    def _sent2chars(sentence):
        return [sentence[i:i+3] for i in range(len(sentence)) if i%3==0]
 
    sents = [_sent2chars(s) for s in sentences]
    special_chars = [
      ' ', 
      'OOV', #out of vocab
      '<s>', #word start
      '</s>', #word end
      'EMP' #place holder
      ]
    sents.append(special_chars)
    return Word2Vec(sents, min_count=1)


def char2vec(model, char):
    """Returns the embedded vector of a character, given a trained model. 
    Returns the embedding of 'OOV' (Out Of Vocabulary) if the char is 
    not found in the vocabs.  
    """
    try:
        emb = model[char]
    except:
        print '++Char {} was not found++' % char
        emb = model['OOV']
    return emb


def strlst2npemb(sentencelist,n=8):

    """ List of strings to numpy array of embeddings. 
        Converts texts from inpath to embedded vectors, then save to outpath.
         Inputs: 
         sentencelist : a list of sentences, where each sentence is represented by a string 
         n : the maximum number of characters to be considered in the sentence
             - if len(sentence) is less than n, fillin the space with 'EMP';
             - if len(sentence) is larger than n, cutoff the part of sentence. 
    """
    sentences = corpus2list('data/corpus.txt')
    model = sent2model(sentences)
    embedding = []
    for line in sentencelist:
        emb = np.empty((0,))
        chars = line.strip().split()
        for c in range(n):
            if len(chars) > c:
                if chars[c] in model:
                    e = model[chars[c]]
                else: 
                    e = model['OOV']
            else: 
                e = model['EMP']
            emb = np.concatenate((emb, np.array(e)))
        embedding.append(emb)
    return np.array(embedding) 




if __name__ == '__main__':
    emb = strlst2npemb(['今天天气不错'])
    print emb.shape



