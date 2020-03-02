import keras
from keras import backend as K
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam

class DQN():
    n_inputs = 0
    n_outputs = 0
    model = -1


    def __init__(self, n_inputs, n_outputs):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.inputLayer = keras.Input(shape=(n_inputs,), name="inputL")
        self.fl1 = Flatten()
        self.hl1 = Dense(32, activation='relu', name='hl1')(self.inputLayer)

        self.hl2 = Dense(32, activation='relu', name='hl2')(self.hl1)
        self.fl2 = Flatten()
        self.outputLayer = Dense(n_outputs, activation='softmax', name='q_output')(self.hl2)
        self.model = keras.Model(inputs=self.inputLayer, outputs=self.outputLayer)

if __name__ == '__main__':
    dqn = DQN(2,2)