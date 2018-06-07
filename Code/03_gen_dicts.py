import json 

def readlines(inpath):
    f = json.loads(inpath)
    print type(f)


if __name__ == '__main__':
    inpath = 'space_boy'
    readlines(inpath)
