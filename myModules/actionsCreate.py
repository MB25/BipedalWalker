import itertools
import random
import json
myActions = [[],[],[]]

list = [-100, -60, -20, 20, 60, 100]
li = itertools.product(list, repeat=6)
print("will try to load actions first")
print("will try to load actions first")

with open("actions.action", "rb") as file:
    myActions = json.load(file)

c = 0
helpArray = [[],[],[]]
print("create instead")
firstHelp = []
lenOfList = 0

for roll in li:
    firstHelp.append(roll)
    lenOfList+=1
print("done with first")

helpArray[0].append(firstHelp)
firstHelp = []
print("helparr size ", len(helpArray))
i = 0
for i in range(lenOfList):
    firstHelp.append(random.uniform(-0.001, 0.001))
print("done with second")
helpArray[1].append(firstHelp)
print("helparr size ", len(helpArray))
firstHelp = []
i=0
for i in range(lenOfList):
    firstHelp.append(random.uniform(-0.15, 0.15))
print("done with third")
helpArray[2].append(firstHelp)
firstHelp = []
print("helparr size ", len(helpArray[0]))
c = 0
myActions = helpArray

print("len ", len(myActions[0][0]))
print("len ", len(myActions[1][0]))
print("len ", len(myActions[2][0]))
#print("myactions ", myActions[0])



for c in range(len(myActions[1][0])):
    print("torque ", myActions[0][0][c])
print("c is ", c)



with open("actionss.action", "w")as file:
    jsdump = json.dumps(myActions)
    # print("jsdumpo")
    file.write(jsdump)

print(len(myActions))