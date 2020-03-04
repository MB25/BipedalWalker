import numpy as np
'''
This is the agent. It's main purpose is to decay epsilon (so that in the beginning there are more random actions) and is
used to pick a targetFrame, which is the output of the first NN and the input of the second NN
------------------------------------------------------------------------------------------------------------------------
targetFrames =  Array of an array of 6 targetpos each. those are keyframes in a gait cycle. This is what the first NN
                predicts and the 2nd takes as Input.
start_epsilon = beginning value of epsilon. The chance to pick a random action is
                n = random number between 0 and 1
                if  (1-start_epsilon) < = n
                    p = take random action
                else
                    p = let network take a guess
                In the beginning a higher epsilon is used, so it explores more. Updated each cycle wih
                start_epsilon = start_epsilon - (1/1088) until end_epsilon is reached
end_epsilon = The final value of epsilon. Does not decay fully so it still takes some random actions
learning rate = the learning rate is the step size when the algorithm computes gradient descent
'''
class Agent():
    targetFrames = []
    start_epsilon = 0
    end_epsilon = 0
    learning_rate = 0

    def __init__(self):
        self.start_epsilon = 0.9
        self.end_epsilon = 0.05
        self.learning_rate = 0.05
        # order is torso_y, rhip, rknee, rtoes, lhip, lknee, ltoes
        self.targetFrames =    [[0.5236,0.0000,-0.0873,-0.5236,0.0000,0.0000],
                                [0.3491,0.2618,0.1745,-0.5236,0.0873,0.0000],
                                [0.1745,0.3491,0.2618,-0.1745,0.6109,0.3491],
                                [0.1745,0.3491,0.2618,0.0000,0.6981,0.1745],
                                [0.0000,0.0000,0.0000,0.0000,1.0472,0.0000],
                                [-0.5236,0.0436,0.0000,0.5236,0.0000,-0.0873],
                                [-0.5236,0.0873,0.0000,0.3491,0.2618,0.1745],
                                [-0.1745,0.6109,0.3491,0.1745,0.3491,0.2618],
                                [0.0000,0.8727,0.0000,0.0873,0.1745,0.1222],
                                [0.0000,1.0472,0.0000,0.1745,0.3491,0.2618],
                                [0.5236,0.5236,0.0000,0.0000,0.0000,0.0000],
                                [0.4363,0.4363,0.0000,-0.5236,0.0044,0.0000]
                                ]

    # make a prediction and return torque-q-target
    def makePrediction(self, targetsDqn, forcesDqn, state):
        q_targets_positional = targetsDqn.model.predict(state)

        q_targets_positional_index = np.argmax(q_targets_positional[0])
        q_input_torque = self.targetFrames[q_targets_positional_index]
        q_input_torque = np.array(q_input_torque)

        q_input_torque_reshaped = np.reshape(q_input_torque, (1, forcesDqn.n_inputs))

        q_targets_torque = forcesDqn.model.predict(q_input_torque_reshaped)
        q_targets_torque = np.reshape(q_targets_torque[0], (1, forcesDqn.n_outputs))
        q_target_torques_max = np.argmax(q_targets_torque)

        return q_target_torques_max, q_targets_torque, q_targets_positional, q_targets_positional_index

    def trainNetworksOnBatch(self, targetsDqn, forcesDqn, state_targets, state_forces):
        return 98

'''
Base class for the DQN. 2 of these are created 
One for estimating positions (targetFrames from agent) and one to estimate forces needed to reach this positions. 
------------------------------------------------------------------------------------------------------------------------
n_inputs = num of inputs of the network
n_outputs = num of outputs of the network
model = this hosts the NN model 
'''


if __name__ == '__main__':
    agent = Agent()