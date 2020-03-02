import pybullet as p
import numpy as np
import pybullet_data

GRAVITY = -9.7
timestep = 1 / 240  # fps

showEvery = 100
JOINTNAMES = ["torso_to_rightleg", "torso_to_leftleg", "r_knee", "l_knee", "r_ankle", "l_ankle"]

class BipedEnv():
    numOfActions = -1
    numOfOutputs = numOfActions
    numOfStates = -1
    actions = []
    counter = 0
    jointIds = []
    paramIds = []
    qTable = []
    states = []
    botId = -1
    gravId = -1
    planeId = -1
    e = 0.1
    client = 0
    prevX = 0
    prevY = -1
    prevAction = -1

    targetFrames = [[0.5236,0.0000,-0.0873,-0.5236,0.0000,0.0000],
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


    def __init__(self, showGui = False, jointNames = []):
        self.repeatCounter = 0
        self.prevX = 0
        self.prevY = 0
        self.jointNames = jointNames
        self.jointNames = jointNames
        self.currentTargetTargetFrameIndex = -1
        if (showGui):
            #p.connect(p.GUI)
            p.connect(p.GUI)
            print("gui")
        else:
            p.connect(p.DIRECT)
            print("no gui")
        setupWorld(self)
        self.setupJoints()

    def getTorsoY(self): #2 = torso
        right = p.getLinkState(self.botId, 5)
        left = p.getLinkState(self.botId, 8)
        if (right > left):
            return right[0][1]
        else:
            return left[0][1]

    def getTorsoZ(self): #2 = torso
        return p.getLinkState(self.botId, 2)[0][2]

    def returnLinkStates(self):
        states = []
        for j in range(len(self.jointIds)):
            index = self.jointIds[j]
            linkState = p.getLinkState(self.botId, index)
            states.append(linkState)
        return states

    def returnAllLinkStates(self):
        states = []
        for j in range((p.getNumJoints(self.botId))):
            linkState = p.getLinkState(self.botId, j)
            states.append(linkState)
        return states

    def step(self, counter, action):
        ##print("ac ", action)
        if (action != -1):
            state = self.gatherObservations()
            self.takeActionTorque(action)
            newState = self.gatherObservations()
            reward, done = getReward(self, counter)
            ##print("s ", state, " a_t ", action, " s_t1 ", newState, " reward ", reward)

        # #print('r ', reward)
        return (state, newState, reward, action, done)

    def takeActionTorque(self, torquesAction = []):
        n = 240
        count = 0
        torques = torquesAction[0]
        hipForce = torquesAction[1]
        bodyForce = torquesAction[2]
        subJointIds = self.jointIds

        framesCount = 0
        maxCount = 240/12
        subTorques = []

        c = 0
        for t in torques:
            if(c>=0):
                subTorques.append(t*2.5)
            c+=1

        while (framesCount <=  maxCount):
            currentPos = []
            subtargetFrame = []
            for jointId in subJointIds:
                posState = p.getJointState(self.botId, jointId)[0]
                currentPos.append(round(posState,3))
                #rhip, rknee, rtoes, lhip, lknee, ltoes
                id = -1
                if(jointId == 3): #r hip
                    id = 0
                elif(jointId==4): #rknee
                    id = 1
                elif(jointId==5): #rankle
                    id = 2
                elif(jointId==6): #lhip
                    id = 3
                elif(jointId ==7): #lknee
                    id = 4
                elif(jointId ==8): #lknee
                    id = 5

                subtargetFrame.append(self.targetFrames[self.currentTargetTargetFrameIndex][id])
            p.setGravity(0, 0, GRAVITY)
            p.setJointMotorControlArray(self.botId,subJointIds,  p.TORQUE_CONTROL, forces=subTorques)
            p.setJointMotorControl2(self.botId, 2, p.POSITION_CONTROL, targetPosition=bodyForce)
            p.setJointMotorControl2(self.botId, 0, p.POSITION_CONTROL, targetPosition=hipForce/120)

            p.stepSimulation()

            framesCount += 1

        targetVels = [0]*len(subJointIds)
        p.setJointMotorControlArray(self.botId, subJointIds, p.VELOCITY_CONTROL, targetVelocities = targetVels)





    def closeEnv(self):
        self.paramIds = []

    def setupJoints(self):
        self.paramIds = []
        self.jointIds = []

        for j in range(p.getNumJoints(self.botId)):
            p.changeDynamics(self.botId, j, linearDamping=0.5, angularDamping=0.5,  lateralFriction=1)
            info = p.getJointInfo(self.botId, j)
            jointName = info[1].decode("utf-8")

            print("jointname! ", jointName, " j ", j)
            if(jointName in self.jointNames):
                self.jointIds.append(j)

        print("all joints: ", self.jointIds)

    def resetEnv(self):
        self.repeatCounter = 0
        setupWorld(self)
        return self.gatherObservations()

    def gatherObservations(self):
        state = []
        jointPositions = []
        jointVelocities = []
        feetTouchingFloor = []

        for joint in self.jointIds:
            jointState = p.getJointState(self.botId, joint)
            jointInfo = p.getJointInfo(self.botId, joint)
            min = jointInfo[8]
            max = jointInfo[9]
            dif = max - min
            n_slices = 100
            n_step = dif/n_slices

            jointPos = jointState[0]

            dif = (jointPos - min)
            dif*=100
            dif = round(dif)
            jointVelocity = jointState[1]
            jointPosIndex = dif%n_slices

            jointVelIndex = round(jointVelocity % n_slices)

            jointPositions.append(jointPosIndex)
            jointVelocities.append(jointVelIndex)
        touchFloor = []
        linkInfo = self.returnAllLinkStates()

        leftAnkleIndex  = 7
        rightAnkleIndex = 8

        feetTouchingFloor = detectContactPoints(p.getContactPoints())

        if leftAnkleIndex in feetTouchingFloor:
            touchFloor.append(0)
        else:
            touchFloor.append(1)
        if rightAnkleIndex in feetTouchingFloor:
            touchFloor.append(0)
        else:
            touchFloor.append(1)

        jointPosAndVel = np.concatenate((jointPositions, jointVelocities, touchFloor), axis=0)
        state = jointPosAndVel

        return state


def detectContactPoints(conPoints):
    # #print('contact points ', conPoints)
    # 5 = r ankle
    # 8 = l ankle
    feetTouchingFloor = []
    for contactPoint in conPoints:
        if contactPoint[4] not in feetTouchingFloor:
            feetTouchingFloor.append(contactPoint[4])  # linkIndex

    return feetTouchingFloor

def getReward(self, counter):

    upperBodLink = p.getLinkState(self.botId, 2)[0] #2 = torso
    rightAnkleY = p.getLinkState(self.botId, 5)[0][1] #right
    leftAnkleY = p.getLinkState(self.botId, 8)[0][1]  # left
    height = upperBodLink[2]
    distanceY = 0
    if(rightAnkleY>leftAnkleY):
        distanceY = rightAnkleY
    else:
        distanceY = leftAnkleY
    orientation =  p.getLinkState(self.botId, 2)[5][0]

    reward = distanceY*100 - orientation*100
    done = False
    if (height < 0.65): #fall or at least nearly-fall
        reward -= 100
        done = True
        return reward, done
    else:
        if(counter % 10) == 0:
            diff = abs(self.getTorsoY() - self.prevY)
            if (0 < diff):
                reward += 10 + diff*100
            else:
                reward = -50
                self.repeatCounter+=1
                if(self.repeatCounter>5):
                    done = True
            self.prevY = self.getTorsoY()
        reward + height*5
        return reward, done

    return reward, done


def setupWorld(biped):
    p.resetSimulation()
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    print('data')
    print(pybullet_data.getDataPath())
    p.setRealTimeSimulation(False)
    p.setTimeStep(timestep)
    cubeStartPos = [0, 0, 0]
    cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
    biped.planeId = p.loadURDF("plane.urdf", cubeStartPos, cubeStartOrientation)

    cubeStartPos = [0, 0, -0.25]
    biped.botId = p.loadURDF("biped/biped2d_pybullet.urdf", cubeStartPos, cubeStartOrientation)
    p.setPhysicsEngineParameter(numSolverIterations=10)

    p.changeDynamics(biped.botId, -1, linearDamping=0, angularDamping=0)

    for i in range( p.getNumJoints(biped.botId)):
        p.changeDynamics(biped.botId, i, linearDamping=0, angularDamping=0)
    p.setGravity(0, 0, GRAVITY)



