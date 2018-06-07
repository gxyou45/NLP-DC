import numpy as np
import pickle 

from keras.layers import Input, Embedding, LSTM, Dense, merge, Bidirectional
from keras.models import Model
from keras.preprocessing import sequence
from word_seg import genData

#Load pickle files
training_objects = pickle.load(open('bilstmTraining.pickle', 'rb'))
test_objects = pickle.load(open('bilstmTest.pickle', 'rb'))
embed_objects = pickle.load(open('bilstmEmbed.pickle', 'rb'))

trainX, trainY, validX, validY, testX, testY = genData()

def genBiData(X):
    X_reverse = X[:,::-1]
    return np.concatenate((X,X_reverse),axis=1)



#Unpack training objects

train_X = genBiData(trainX)
train_Y = trainY
valid_X = genBiData(validX)
vaild_Y = validY
w2i = training_objects['w2i']
c2i = training_objects['c2i']
task2t2i = training_objects['task2t2i']

#Unpack test objects
test_X = genBiData(testX)
test_Y = testY
org_X = test_objects['org_X']
org_Y = test_objects['org_Y']
test_task_labels = test_objects['test_task_labels']

del trainX
del trainY
del testX
del testY
del validX
del validY

print('X_train shape:', train_X.shape)
print('X_test shape:', test_X.shape)




# Build Keras BiLSTM model

#Placeholder inputs
char_input = Input(shape=(128,64), dtype='float32')
word_input = Input(shape=(128,), dtype='int32')

#Embeddings
embed_layer = Embedding(len(w2i) + 1,
                    64,
                    weights=[embedding_matrix],
                    input_length=128,
                    trainable=False)(word_input)

#Apply LSTM on charachters
char_biLSTM = Bidirectional(LSTM(64))(char_input)

#Concatenate char and word embedings
merge_l1 = merge([embedded, char_biLSTM], mode='concat', concat_axis=0)

#Apply LSTM on concated inputs
biLSTM = Bidirectional(LSTM(64))(merge_l1)

after_dp = Dropout(0.5)(biLSTM)
output = Dense(17, activation='sigmoid')(after_dp)

model = Model([char_input,word_input], output)






