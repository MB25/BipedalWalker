from collections import deque
import random


class Replay():
    maxSize = 0
    memory = []
    n = 0

    def __init__(self, maxSize):
        self.maxSize = maxSize
        self.memory = deque()
        self.n = 0

    def addExperience(self, experience):
        if(self.n < self.maxSize):
            self.memory.append([experience.s_t, experience.a_t, experience.s_t1, experience.r_t])
            self.n+=1
        else:
            self.memory.popleft()
            self.memory.append([experience.s_t, experience.a_t, experience.s_t1, experience.r_t])

    def returnAllExperiences(self):
        return self.memory


    def getRandomSample(self):
        if(self.n!=0):
            index = random.randrange(0, len(self.memory))
            return self.memory[index]

    def getRandomBatch(self, batchsize):
        if (self.n >= batchsize):
            c = 0
            experiences = []
            for c in range(batchsize):
                index = random.randrange(0, len(self.memory))
                experiences.append(self.memory[index])
            return experiences