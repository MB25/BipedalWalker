import datetime
import itertools
import json
import numpy as np
import os
import random
import tensorflow as tf
from time import time, ctime
import sys

from myModules import Agent
from myModules import BipedEnv
from myModules import Dqn as Dqn
from myModules import Experience as Exp
from myModules import Replay as Replay

from prettytable import PrettyTable

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import keras
from keras.optimizers import Adam

EPISODES = 50
REPLAYMEMSIZE = 100
BATCHSIZE= 32
JOINTNAMES = ["torso_to_rightleg", "torso_to_leftleg", "r_knee", "l_knee", "r_ankle", "l_ankle"]

'''
I got some help with the main structure for implementation by reading the following blog:
https://deeplizard.com/learn/video/PyQNfsGUnQA

This is the controller. It implements and uses all the other components and implements the generell algorithm
first sets up everything (initiating everything, creating myactions, loading weights..) and then iterates over episodes
each timestep
--------------------------------------------------------------------------------------------------------------
episodes = number of episodes to run
showGui = If set to True, showGui is used 
train = If set to True, trained weights are used 
'''
class ReinforcementWalker2D():

    def __init__(self, episodes=500, showGui=True, train=False):
        self.episodes = episodes
        self.showGui = showGui
        self.train = train
        self.myActions = [[], [],[]]
        self.randCounter = 0
        self.exploitCounter = 0



    def loadActions(self):

        with open("actions.action", "rb") as file:
            try:
                self.myActions = json.loads(file.read())
            except IOError as ioError:
                list = [-100, -60, -20, 20, 60, 100]
                li = itertools.product(list, repeat=6)
                c = 0
                helpArray = [[], [], []]
                print("create instead")
                firstHelp = []
                lenOfList = 0

                for roll in li:
                    firstHelp.append(roll)
                    lenOfList += 1
                helpArray[0].append(firstHelp)
                firstHelp = []
                i = 0
                for i in range(lenOfList):
                    firstHelp.append(random.uniform(-0.001, 0.001))

                helpArray[1].append(firstHelp)
                firstHelp = []
                i = 0
                for i in range(lenOfList):
                    firstHelp.append(random.uniform(-0.15, 0.15))

                helpArray[2].append(firstHelp)
                c = 0
                self.myActions = helpArray



    def setUpEverything(self):
        config = tf.ConfigProto(device_count={'GPU': 1, 'CPU': 1})
        session = tf.Session(config=config)
        keras.backend.set_session(session)
        print("session set")


    def startTraining(self):
        agent = Agent.Agent()

        self.setUpEverything()
        self.loadActions()
        #self.loadActions()
        print("what what ")
        starttime = time()



        prevtime = starttime
        training = self.train  # if this is true, it will run training, if false it will load weights

        lenFrames = len(agent.targetFrames)

        lenOfInput = len(JOINTNAMES)*2 + 2 # only for helper. State is [(pos1, pos2 .., posN), (vel1, vel2, ... velN),
                                            # [0 OR 1], [0 OR 1]]. So length is names * 2 +2

        networkPositions = Dqn.DQN(lenOfInput, len(agent.targetFrames))  # this network is used to calculate the best next state
        netWorkForces = Dqn.DQN(len(agent.targetFrames[0]),len(self.myActions[1][0]))


        print("--------------------------------")
        print("Summary of Networks")
        print(networkPositions.model.summary())
        print(netWorkForces.model.summary())
        print("----------------------------------")

        adam = Adam(lr=agent.learning_rate)
        networkPositions.model.compile(loss='mse', optimizer=adam)
        netWorkForces.model.compile(loss='mse', optimizer=adam)

        if (training == False):
            try:
                networkPositions.model.load_weights("weights/myWeightsPos6weights.we")
                netWorkForces.model.load_weights("weights/myWeightsPos6Forces.we")
                print("loading weights successful")
            except IOError as err:
                print("error; ", IOError)

        print("success creating actions")
        print("count actions ", len(self.myActions[0]))

        replayMemory = Replay.Replay(REPLAYMEMSIZE)

        distances = []
        losses = []
        seconds = []
        totalRewardPerEpisode = []

        c = -1
        for episode in range(self.episodes):
            totalLossPos = 0
            totalLossTorque = 0
            episodeCount = 0
            totalReward = 0

            done = False
            print("gui is shown ", self.showGui)
            envo = BipedEnv.BipedEnv(self.showGui, JOINTNAMES)

            state = envo.resetEnv()
            c += 1
            state = np.array(state)
            state = np.reshape(state, (1, len(state)))  # number of state inputs (6 atm(

            positionalState = state
            positionalState = np.reshape(positionalState, (1, networkPositions.n_inputs))

            # pick action via explore ore exploit
            # 1-epsilon = highest q
            while not done:
                choice = random.random()
                actionIndex = -1


                if ((1 - agent.start_epsilon) <= choice):  # decay epsilon so it explores more in the beginning but less in the end
                    actionIndex = random.randrange(0, len(self.myActions[1][0]))
                    envo.currentTargetTargetFrameIndex = random.randrange(0, len(envo.targetFrames))
                    self.randCounter+=1
                else:
                    state = np.reshape(state, (1, networkPositions.n_inputs))  # 6 = 20
                    actionIndex, _, _, targetFrameIndex = agent.makePrediction(networkPositions, netWorkForces, state)
                    envo.currentTargetTargetFrameIndex = targetFrameIndex
                    self.exploitCounter += 1

                action = [[], [], []]

                action[0] = self.myActions[0][0][actionIndex]
                action[1] = self.myActions[1][0][actionIndex]
                action[2] = self.myActions[2][0][actionIndex]

                state, newState, reward, action, done = envo.step(c, action)
                experience = Exp.Experience(state, action, newState, reward, done)
                replayMemory.addExperience(experience)
                state = newState
                totalReward += reward
                if (replayMemory.n > BATCHSIZE):

                    experiences = replayMemory.getRandomBatch(BATCHSIZE)
                    for experience in experiences:
                        state_t = experience[0]
                        action_t = experience[1]
                        state_t1 = experience[2]
                        reward = experience[3]

                        state_t = np.array(state_t)
                        state_t1 = np.array(state_t1)
                        state_t = np.reshape(state_t, (1, networkPositions.n_inputs,))
                        state_t1 = np.reshape(state_t1, (1, networkPositions.n_inputs,))

                        highestTargetIndexTorque, targetsTorque, targetsPos, targetPosIndex = agent.makePrediction(
                            networkPositions, netWorkForces, state_t)

                        envo.currentTargetTargetFrameIndex = targetPosIndex
                        maxTorquesIndex, maxTorqueQs, maxTargetPosQs, maxTargetPosIndex = agent.makePrediction(networkPositions, netWorkForces, state_t1)

                        rightSidePositions = 0.99 * targetsPos[0][targetPosIndex]
                        rightSideTorques = 0.99 * targetsTorque[0][highestTargetIndexTorque]

                        dist1 = envo.getTorsoY()
                        if (dist1 < 0):
                            abs(reward) * -1

                        targetsPos[0][targetPosIndex] = reward + rightSidePositions
                        targetsTorque[0][self.myActions[0][0].index(action_t[0])] = reward + rightSideTorques

                        totalLossPos += networkPositions.model.train_on_batch(state_t, targetsPos)  # train both atst?

                        frameNow = envo.targetFrames[envo.currentTargetTargetFrameIndex]
                        frameNow = np.array(frameNow)
                        frameNow = np.reshape(frameNow, (1, netWorkForces.n_inputs,))

                        totalLossTorque += netWorkForces.model.train_on_batch(frameNow, targetsTorque)
                        rightSidePositions = 0.99 * maxTargetPosQs[0][maxTargetPosIndex]
                        rightSideTorques = 0.99 * maxTorqueQs[0][maxTorquesIndex]


                        #    print("rew ", reward)
                       #     print("rights ", rightSidePositions)
                       #     print("rights t ", rightSideTorques)
                        maxTargetPosQs[0][maxTargetPosIndex] = reward + rightSidePositions
                        maxTorqueQs[0][self.myActions[0][0].index(action_t[0])] = reward + rightSideTorques
                      #  print("mtposqs ",   maxTargetPosQs[0][maxTargetPosIndex])
                        totalLossPos += networkPositions.model.train_on_batch(state_t1, maxTargetPosQs)  # train both atst?

                        frameNow = envo.targetFrames[envo.currentTargetTargetFrameIndex]

                        frameNow = np.array(frameNow)
                        frameNow = np.reshape(frameNow, (1, netWorkForces.n_inputs,))

                        totalLossTorque += netWorkForces.model.train_on_batch(frameNow, maxTorqueQs)
                        totalReward+=reward

            decrement = 1 / self.episodes
            dif = agent.start_epsilon - decrement

            if (dif > agent.end_epsilon):
                agent.start_epsilon = dif
            else:
                agent.start_epsilon = agent.end_epsilon
            dist = envo.getTorsoY()
            distances.append(dist)
            losses.append(totalLossPos)
            totalRewardPerEpisode.append(totalReward)
            timeDif = time() - prevtime
            prevtime = time()
            seconds.append(timeDif)

            print("episode|distance|loss|total Reward this episode| time[s]")
            print("rand choices ", self.randCounter, " exploits ", self.exploitCounter, " current eps ",
                  agent.start_epsilon)
            t = PrettyTable(['Episode', 'Distance', 'Losses', "reward", "Seconds"])
            t.add_row([episode, round(dist, 4), round(totalLossPos, 4), round(totalReward,4), timeDif])
            starttime = time()
            envo.closeEnv()
            print(t)
            del envo
            episodeCount = 0
            self.exploitCounter = 0
            self.randCounter = 0


        endtime = time()
        print("took ", endtime - starttime, " seconds or ", (endtime - starttime) / 60, " m ", " or ",
              (endtime - starttime) / 60 / 60, " h")

        episodes = []

        t = PrettyTable(['Episode', 'Distance', 'Losses', "TotalReward", "Seconds"])
        for i in range(len(distances)):
            if (i > 0):
                episodes.append(episodes[i - 1] + 1)
            else:
                episodes.append(1)
            t.add_row([episodes[i], distances[i], losses[i], totalRewardPerEpisode[i], seconds[i]])
        t.add_row([100, sum(distances), sum(losses), sum(totalRewardPerEpisode), sum(seconds)])
        print(t)

        timestring = datetime.datetime.now()

        timeStringsub = (str(timestring.day) + "-" + str(timestring.month) + "__" +
                         str(timestring.hour) + "_" + str(timestring.minute) + "_" + str(timestring.second))
        networkPositions.model.save_weights("weights/myWeightsPos6weights.we")
        netWorkForces.model.save_weights("weights/myWeightsPos6Forces.we")
        networkPositions.model.save_weights("weights/timed/myWeightsPos6weights%s.we" % timeStringsub)
        netWorkForces.model.save_weights("weights/timed/myWeightsPos6Forces%s.we" % timeStringsub)



if __name__ == '__main__':
    argsEpisodes = 100
    argsShow = False
    argsTrain = False
    listArgs = sys.argv

    print("num of args ", len(sys.argv))
    if(len(listArgs)==4):
        argsEpisodes = listArgs[1]
        print("setting args ")
        if(listArgs[2]=="True"):
            argsShow = True
        if(listArgs[3]=="True"):
            argsTrain = True
    print(sys.argv)
    walker = ReinforcementWalker2D(int(argsEpisodes), argsShow, argsTrain)
    print("eps ", walker.episodes)
    walker.startTraining()
    print("done")