import numpy as np

from lstm import LstmParam, LstmNetwork
from word_seg import genData


class ToyLossLayer:
    """
    Computes square loss with first element of hidden layer array.
    """
    @classmethod
    def loss(self, pred, label):
        return (pred[0] - label) ** 2

    @classmethod
    def bottom_diff(self, pred, label):
        diff = np.zeros_like(pred)
        diff[0] = 2 * (pred[0] - label)
        return diff


def genBiData(X):
    X_reverse = X[:,::-1]
    return np.concatenate((X,X_reverse),axis=1)


def bilstm_runn():
    trainX, trainY, validX, validY, testX, testY = genData()
    # learns to repeat simple sequence from random inputs
    np.random.seed(0)

    train_X = genBiData(trainX)
    train_Y = trainY
    valid_X = genBiData(validX)
    vaild_Y = validY
    test_X = genBiData(testX)
    test_Y = testY

    del trainX
    del trainY
    del testX
    del testY
    del validX
    del validY
    
    # parameters for input data dimension and lstm cell count
    mem_cell_ct = 100
    x_dim = 50
    lstm_param = LstmParam(mem_cell_ct, x_dim)
    lstm_net = LstmNetwork(lstm_param)
    y_list = [-0.5, 0.2, 0.1, -0.5]
    input_val_arr = [np.random.random(x_dim) for x in y_list]

    for cur_iter in range(100):
        print("iter", "%2s" % str(cur_iter), end=": ")
        for ind in range(len(y_list)):
            lstm_net.x_list_add(input_val_arr[ind])

        print("y_pred = [" +
              ", ".join(["% 2.5f" % lstm_net.lstm_node_list[ind].state.h[0] for ind in range(len(y_list))]) +
              "]", end=", ")

        loss = lstm_net.y_list_is(y_list, ToyLossLayer)
        print("loss:", "%.3e" % loss)
        lstm_param.apply_diff(lr=0.1)
        lstm_net.x_list_clear()


if __name__ == "__main__":
    #test()

