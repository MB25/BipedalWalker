[1mdiff --git a/.idea/workspace.xml b/.idea/workspace.xml[m
[1mindex f41f121..3071adb 100644[m
[1m--- a/.idea/workspace.xml[m
[1m+++ b/.idea/workspace.xml[m
[36m@@ -2,14 +2,10 @@[m
 <project version="4">[m
   <component name="ChangeListManager">[m
     <list default="true" id="0cd860c5-857d-4af4-ab5e-d781eb266397" name="Default Changelist" comment="">[m
[31m-      <change afterPath="$PROJECT_DIR$/weights/backup/backup_4030/myWeightsPos6Forces.we" afterDir="false" />[m
[31m-      <change afterPath="$PROJECT_DIR$/weights/backup/backup_4030/myWeightsPos6weights.we" afterDir="false" />[m
[31m-      <change afterPath="$PROJECT_DIR$/weights/timed/myWeightsPos6Forces4-3__1_52_32.we" afterDir="false" />[m
[31m-      <change afterPath="$PROJECT_DIR$/weights/timed/myWeightsPos6weights4-3__1_52_32.we" afterDir="false" />[m
       <change beforePath="$PROJECT_DIR$/.idea/workspace.xml" beforeDir="false" afterPath="$PROJECT_DIR$/.idea/workspace.xml" afterDir="false" />[m
       <change beforePath="$PROJECT_DIR$/ReinforcementWalker2D.py" beforeDir="false" afterPath="$PROJECT_DIR$/ReinforcementWalker2D.py" afterDir="false" />[m
[31m-      <change beforePath="$PROJECT_DIR$/weights/myWeightsPos6Forces.we" beforeDir="false" />[m
[31m-      <change beforePath="$PROJECT_DIR$/weights/myWeightsPos6weights.we" beforeDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/weights/myWeightsPos6ForcesBackedUp.we" beforeDir="false" afterPath="$PROJECT_DIR$/weights/myWeightsPos6ForcesBackedUp.we" afterDir="false" />[m
[32m+[m[32m      <change beforePath="$PROJECT_DIR$/weights/myWeightsPos6weightsBackedUp.we" beforeDir="false" afterPath="$PROJECT_DIR$/weights/myWeightsPos6weightsBackedUp.we" afterDir="false" />[m
     </list>[m
     <option name="EXCLUDED_CONVERTED_TO_IGNORED" value="true" />[m
     <option name="SHOW_DIALOG" value="false" />[m
[1mdiff --git a/README.md b/README.md[m
[1mindex a0b5eda..970b561 100644[m
[1m--- a/README.md[m
[1m+++ b/README.md[m
[36m@@ -10,5 +10,8 @@[m [mThis is the README File for the REINFORCEMENTWALKER 2D Project.[m
 Option 1 - Run and train yourself [m
 1) If you want to train on your own or simply wish to execute the script yourself, navigate to main project folder with CMD/Terminal [m
 2) type: [m
[31m-	python3 ReinforcementWalker2D.py [m
[32m+[m[32m    python ReinforcementWalker2D.py [Num_Episodes] [ShowGUI] [trainOwnWeights][m
[32m+[m	[32mor, to use standard params (500, False, False)[m[41m [m
[32m+[m	[32mpython ReinforcementWalker2D.py[m[41m [m
[32m+[m[41m	[m
 3) Note: Proper training will take several hours and requires a decent NVIDIA GPU. (1070 and upwards) [m
[1mdiff --git a/ReinforcementWalker2D.py b/ReinforcementWalker2D.py[m
[1mindex ae2a92a..2693588 100644[m
[1m--- a/ReinforcementWalker2D.py[m
[1m+++ b/ReinforcementWalker2D.py[m
[36m@@ -233,9 +233,6 @@[m [mclass ReinforcementWalker2D():[m
                         rightSideTorques = 0.99 * maxTorqueQs[0][maxTorquesIndex][m
 [m
 [m
[31m-                        #    print("rew ", reward)[m
[31m-                       #     print("rights ", rightSidePositions)[m
[31m-                       #     print("rights t ", rightSideTorques)[m
                         maxTargetPosQs[0][maxTargetPosIndex] = reward + rightSidePositions[m
                         maxTorqueQs[0][self.myActions[0][0].index(action_t[0])] = reward + rightSideTorques[m
                       #  print("mtposqs ",   maxTargetPosQs[0][maxTargetPosIndex])[m
[36m@@ -249,9 +246,7 @@[m [mclass ReinforcementWalker2D():[m
                         totalLossTorque += netWorkForces.model.train_on_batch(frameNow, maxTorqueQs)[m
                         totalReward+=reward[m
                         if (distance < 0):[m
[31m-                         #   print("totalR before",totalReward)[m
                             totalReward = abs(totalReward) * -1[m
[31m-                          #  print("total reward after ", totalReward)[m
                         else:[m
                             totalReward = abs(totalReward)[m
             decrement = 1 / self.episodes[m
[1mdiff --git a/weights/myWeightsPos6ForcesBackedUp.we b/weights/myWeightsPos6ForcesBackedUp.we[m
[1mindex d838592..20c29e0 100644[m
Binary files a/weights/myWeightsPos6ForcesBackedUp.we and b/weights/myWeightsPos6ForcesBackedUp.we differ
[1mdiff --git a/weights/myWeightsPos6weightsBackedUp.we b/weights/myWeightsPos6weightsBackedUp.we[m
[1mindex d2dd7ac..1f6bdbb 100644[m
Binary files a/weights/myWeightsPos6weightsBackedUp.we and b/weights/myWeightsPos6weightsBackedUp.we differ
