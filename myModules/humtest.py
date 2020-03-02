import pybullet as p
import pybullet_data
import time
import math



def setupJoints():


    for j in range(p.getNumJoints(botId)):
        p.changeDynamics(botId, j, linearDamping=0, angularDamping=0, lateralFriction=0.8)
        p.setJointMotorControl2(botId, j, p.VELOCITY_CONTROL, force=0)
        info = p.getJointInfo(botId, j)
        state = p.getLinkState(botId, j)
        # print('info ', info)
        jointName = info[1].decode("utf-8")
        jointType = info[2]
        dynInfo = p.getDynamicsInfo(botId, j)

        if "ignore" not in jointName:

            if (jointType==p.JOINT_REVOLUTE):
                print("joiintanme ", jointName, " ", )
                jointIds.append(j)
                paramId = p.addUserDebugParameter(jointName, -2, 2, 0)
                paramIds.append(paramId)



p.connect(p.GUI)
p.setGravity(0,0,-9.7)
p.resetSimulation()
p.setAdditionalSearchPath(pybullet_data.getDataPath())
print(pybullet_data.getDataPath())
p.setRealTimeSimulation(False)
p.setTimeStep(1/240)
planeId = p.loadURDF("plane.urdf")
cubeStartPos = p.getQuaternionFromEuler([0, 0, 0])
cubeStartPos = [0,0,0.75]
cubeStartOrientation = p.getQuaternionFromEuler([1.5, 0,0])
print(pybullet_data.getDataPath())
botId = p.loadURDF("biped/old_biped2d_pybullet.urdf")

print("num ", p.getNumJoints(botId))

jointIds = []
paramIds = []

setupJoints()


while True:

    p.setGravity(0, 0,-9)

    targetFrames = [[0, -0.218, -0.175, 0, 0, 0, 0],  # leftstat, right init
                    [0, 0, 0, 0, 0.436, -1.222, -0.436],  # leftstat, right midswing
                    [-0.3, +0.21, -0.035, -0.035,-0.2, -0.436, 0],  # leftstat, right terminal
                    [0, 0, 0, 0, -0.218, -0.175, 0],  # rightstat, left init
                    [0, 0.436, -1.222, -0.436, 0, 0, 0],  # rightstat, left midswing
                    [0, -0.2, -0.436, 0, +0.21, -0.035, -0.3]  # rightstat, left terminal
                    ]



    while True:
        print("jointids ", jointIds)
        p.setJointMotorControlArray(botId, jointIds, p.POSITION_CONTROL, targetPositions=targetFrames[2])

        p.stepSimulation()

