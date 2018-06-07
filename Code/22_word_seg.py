from char2vec import * 
from nn import * 
from data_parser import * 



def genData(max_len=8):
    """ Generate data for training models to detect whether a phrase is an
	    internet slang, a popular term (i.e. drama/movie names for now), or
	    else. A half of the number of the total number of internet slangs 
	    and popular terms of other phrases are added to ensure the set is 
	    balanced.

    params: 
        max_len is the maximum acceptable number of characters in a string
    outputs:
	    X is the embedding of the input strings of characters
	    Y is the corresponding labels
    """
    # generates lists of strings
    sogo_internet = sogo_internet_2list('data/sogo_internet_list.txt')
    sogo_drama_movies = sogo_internet_2list('data/sogo_drama_movie_list.txt')
    sogo_else = sogo_internet_2list('data/else_list.txt')

    # numpy array of embeddings -- X
    X_internet = strlst2npemb(sogo_internet,max_len)
    X_drama_movies = strlst2npemb(sogo_drama_movies,max_len)
    c = (X_internet.shape[0] + X_drama_movies.shape[0]) / 2
    X_else = strlst2npemb(sogo_else[:c], max_len)

    # numpy array of labels -- Y 
    # internet [1, 0, 0]; drama_movies [0, 1, 0]
    Y_internet = np.zeros((X_internet.shape[0],3))
    Y_drama_movies = np.zeros((X_drama_movies.shape[0],3))
    Y_else = np.zeros((X_else.shape[0],3))
    Y_internet[:,0] = 1
    Y_drama_movies[:,1] = 1
    Y_else[:,2] = 1

    # concatenation 
    X = np.concatenate((X_else,X_internet,X_drama_movies))
    Y = np.concatenate((Y_else,Y_internet,Y_drama_movies))
    data = np.concatenate((X, Y), axis=1)
    for i in range(5):
        np.random.shuffle(data)

    # split data
    p1 = int(data.shape[0] * 0.6)
    p2 = int(data.shape[0] * 0.9)
    trainX, trainY = data[:p1,:-3], data[:p1,-3:]
    validX, validY = data[p1:p2,:-3], data[p1:p2,-3:]
    testX, testY = data[p2:,:-3], data[p2:,-3:]
    
    print trainX.shape, validX.shape, testX.shape 

    return trainX, trainY, validX, validY, testX, testY



def NN(trainX, trainY, validX, validY):
    model = NeuralNetwork(layers=[200,100], activation='softmax')
    model.fit(trainX, trainY)
    valid_pred = model.predict(validX)
    print "MSE = ", model.mse(validY,valid_pred)
    

if __name__ == '__main__':
    trainX, trainY, validX, validY, testX, testY = genData()
    NN(trainX, trainY, validX, validY)






