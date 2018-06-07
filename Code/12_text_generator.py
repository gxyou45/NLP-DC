#encoding=utf-8


writeto = open('corpus.txt','w')

# File 1 
with open('S_WithoutError_10001-10350.txt', 'r') as f:
    for line in f:
        print >> writeto, line.split()[2]
        
