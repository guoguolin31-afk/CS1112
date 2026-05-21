from robot import Robot, FastRobot, LimbedRobot
from item import Item
import math

## Test class Robot
r1 = Robot(1, 4, 20, [4, 4])
step1 = r1.travel_steps([4, 4], [5, 5])
print(len(step1))                                                        # Should be 3
r1.draw([4, 4])                                                          # Draw a blue circle centered at (4, 4)


## Test class FastRobot
# TODO: add test cases

r2 = FastRobot(2,4,20,[0,0],3)              #test fast robot with vertically up angle
step2 = r2.travel_steps([0, 0], [0, 4])     #should be [[0,0],[0,3],[4,4]]
print(f'Fastrobot 1 {step2=}')
r2.draw([0, 0])   #Draw a green circle centered at (0, 0)

r3 = FastRobot(3,4,20,[2,2],math.sqrt(2))   #test fast robot with 45 degrees
step3 = r3.travel_steps([2, 2], [4, 4])     #should be [[2,2], [3, 3], [4, 4]]
print(f'Fastrobot 2 {step3=}')
r3.draw([2, 2])    #Draw a green circle centered at (2, 2)

r6 = FastRobot(6,4,20,[2,1],math.sqrt(3))   #test fast robot with vertically down angle
step6 = r6.travel_steps([2, 1], [2, 0])     #should be [[2,1],[2,0]]
print(f'Fastrobot 3 {step6=}')
r6.draw([2, 1])    #Draw a green circle centered at (2, 1)

r7 = FastRobot(7,4,20,[2,5],math.sqrt(3))   #test fast robot with horizaontal angle
step7 = r7.travel_steps([2, 5], [4, 5])     #should be [[2,5],[number between 2 and 4,5],[4,5]]
print(f'Fastrobot 4 {step7=}')
r7.draw([2, 5])    #Draw a green circle centered at (2, 5)

## Test class LimbedRobot
# TODO: add test cases
r4 = LimbedRobot(4,4,20,[5,4],1,0.5)       #test for limbed robot with 0.5 stepsize
step4 = r4.travel_steps([5, 4], [3, 3])    #should be 6 travel steps
print(f'Limbedrobot 1 {step4=}')
r4.draw([5, 4])   #Draw a magenta circle centered at (5, 4)

r8= LimbedRobot(6, 4,30,[2,9], 2, 0.3,5)   #test for limbed robot with 0.3 stepsize
step8=r8.travel_steps([2,9], [5,8])        #should be 15 travel step
print(f'Limbedrobot 3 {step8=}')
print(f'travel step is {len(step8)}')

r5 = LimbedRobot(5,4,100,[6,5],2,0.9)      #test for limbed robot with 0.5 stepsize
step5 = r5.travel_steps([6, 5], [3, 3])    #should be 8 travel steps
print(f'Limbedrobbot 2 {step5=}')
r5.draw([6, 5])   #Draw a magenta circle centered at (6, 5)

i1= Item(1, 'apple', 3, [1,1], 1, 1)       #test for limbed robot that has 2 arm can pick 
print(f'Libedrobot can pick {r5.pick(i1)=}') #1 arm required item, should be True

i2= Item(2, 'desk', 3, [1,1], 4, 1)       #test for limbed robot that has 2 arm can pick 
print(f'Libedrobot can pick {r5.pick(i2)=}') #4 arm required item, should be False

i3=Item(5, 'cat', 7, [5,8], 2, 2 )
print(f'Libedrobot can pick {r8.pick(i3)=}')