# testscript.py
"""
Demonstration and tests for Project 5 classes
"""


from interval import Interval
from item import Item
from robot import Robot
import matplotlib.pyplot as plt


## Test class Interval
in1 = Interval(3, 9)              # Instantiate an Interval with endpoints 3 and 9
print(in1)
print(in1.left)                   # Should be 3. The attributes are "public," so it 
                                  #   is possible to access the attribute left directly.
in2 = Interval()                  # Instantiate an Interval with default end points
print(in2)
o = in1.overlap(Interval(5, 15))  # o references an Interval with endpoints 5 and 9.
print(o)
print(f"{o.get_width()=}")        # Should be 4, the width of the Interval referenced by o


## Test class Item
#Test 1
print('\nTest 1 for class Item\n---------------------')
#Create an Item with id 1, name"basket", weight 2, located at [3,4], no arm required,
#3 time step for pick up.
i1 = Item(1, 'basket', 2, [3, 4], 0, 3)
print(f"{i1.id_=}")                           # Should be 1
print(f"{i1.loc=}")                           # Should be [3, 4]
print(f'{i1.valid_pickup(4,2)=}')             # Should print true
print(f'{i1.valid_pickup(1,0)=}')             # Should print false
print(f'{i1.update_pickup_status(2)=}')       # Schedule i1 for pickup starting
                                              # at time 2, return None
print(f'{i1.picked_window.left=}')            # Should print 2
print(f'{i1.picked_window.right=}')           # Should print 5 bc start at 2 
                                              # plus duration 3 =5
# The amount of time it takes for a robot to pick up the item should be 
# equal to the item's duration attribute
print(f'{i1.picked_window.get_width()=}')     # Should be 3

# At time 3, the item is not yet fully picked up, so it should be drawn if
# method draw is called. The statements below should give a red rectangle in
# figure window 1, centered at(3,4),with "1"(the id) inside the rectangle.
plt.figure(1); i1.draw(3)
# At time 5, the item is picked up, so it should not be drawn if method draw is
# called. The statements below should show figure window 2 but nothing drawn.
plt.figure(2); i1.draw(5)

#Test 2
print('\nTest 2 for class Item\n---------------------')
i2 = Item(2, 'table', 20, [-9,-6], 4, 5)
print(f"{i2.id_=}")                           # Should be 2
print(f"{i2.loc=}")                           # Should be [-9, -6]
print(f'{i2.valid_pickup(20,4)=}')            # Should print true
print(f'{i2.valid_pickup(4,20)=}')            # Should print false
print(f'{i2.update_pickup_status(6)=}')       # Schedule i2 for pickup starting
                                              # at time 6, return None
print(f'{i2.picked_window.left=}')            # Should print 6
print(f'{i2.picked_window.right=}')           # Should print 11 bc start at 6 
                                              # plus duration 5 =11
# The amount of time it takes for a robot to pick up the item should be 
# equal to the item's duration attribute
print(f'{i2.picked_window.get_width()=}')     # Should be 5

# At time 7, the item is not yet fully picked up, so it should be drawn if
# method draw is called. The statements below should give a red rectangle in
# figure window3, centered at(-9,-6),with "2"(the id) inside the rectangle.
plt.figure(3); i2.draw(7)
# At time 0, the item is picked up, so it should not be drawn if method draw is
# called. The statements below should show figure window 4 but nothing drawn.
plt.figure(4); i2.draw(11)


#Test 3
print('\nTest 3 for class Item\n---------------------')
i3 = Item(3, 'cups', 0.378, [-3.5,4.5], 6, 2)
print(f"{i3.id_=}")                           # Should be 3
print(f"{i3.loc=}")                           # Should be [-3.5 ,4.5]
print(f'{i3.valid_pickup(0.5,7)=}')           # Should print true
print(f'{i3.valid_pickup(0.8,5)=}')           # Should print false
print(f'{i3.update_pickup_status(0)=}')       # Schedule i1 for pickup starting
                                              # at time 0, return None
print(f'{i3.picked_window.left=}')            # Should print 0
print(f'{i3.picked_window.right=}')           # Should print 2 bc start at 0 
                                              # plus duration 2 =2
# The amount of time it takes for a robot to pick up the item should be 
# equal to the item's duration attribute
print(f'{i3.picked_window.get_width()=}')     # Should be 2

# At time 1, the item is not yet fully picked up, so it should be drawn if
# method draw is called. The statements below should give a red rectangle in
# figure window5, centered at(-3.5,4.5),with "3"(the id) inside the rectangle.
plt.figure(5); i3.draw(1)
# At time 11, the item is picked up, so it should not be drawn if method draw is
# called. The statements below should show figure window 6 but nothing drawn.
plt.figure(6); i3.draw(11)


## Test class Robot
# create 3 Item obejct to test Robot class
i1 = Item(1, 'apples', 12, [3, 3], 1, 1)
i2 = Item(4, 'rubber duck', 1, [5, 5], 0, 3)
i3 = Item(6, 'paperclip', 0.1, [9, 1], 0, 3)
i4 = Item(8, 'board', 0.2,[4,4],0,2)


# TODO: ADD YOUR TESTS BELOW
#Test 1 with 1 items picked
#create a robot id 1, max weight can pick is 20, with total opertaing time 88, 
#located at [4,5]
r1 = Robot(1,20,88,[4,5])
print('\nTest 1 for class Robot\n---------------------')
print(f"{r1._id_=}")                          # Should be 1
print(f"{r1._init_loc=}")                     # Should be [4,5]
print(f'{r1._max_weight=}')                   # Should be 20
print(f'{r1._total_time=}')                   # Should be 88
print(f'{r1.get_id()=}')                      # Should be 1
print(f'{r1.get_items_picked()=}')            # Should be []
print(f'{r1.total_operation_time()=}')        # Should be 0, no item picked yet
print(f'{r1.latest_resting_loc()=}')          # Should be [4,5]
print(f'{r1._items_picked.append(i1)=}')      # update the items picked, return none
print(f'{r1.get_items_picked()=}')            # Should be [i1's address]
print(f'{i1.update_pickup_status(20)=}')      # Lets's say the item is picked up at time=20
print(f'{r1.total_operation_time()=}')        # total time should be 21
print(f'{r1.latest_resting_loc()=}')          # Should be [3,3]
#At resting, the robot is at the last item's position where the robot picked it up
# figure window7, centered at(3,3),with "1"(the id) inside the circle.
plt.figure(7); r1.draw(r1.latest_resting_loc())
      
print(f'{r1.travel_steps([3,3], [3,3])=}')   # Should print 1 loction list nest in a list
                                             # Begins at [3,3] end at [3,3]
print(f'{r1.pick(i1,True,80)=}')             # Should print  False since 
                                             # the item is already set a picked window
                                             # also did not meet arm requirment
print(f'{i1.picked_window.right=}')          # Should be 20+1=21 
                                             # (totaltime+travelstep-1+item duration)
print(f'{r1.get_location(25)=}')             # Should be at item's location

#Test 2 with 2 items picked
#create a robot id 2, max weight can pick is 10, with total opertaing time 6, 
#located at [3,3]
r2 = Robot(2,10,6,[3,3])
print('\nTest 2 for class Robot\n---------------------')
print(f"{r2._id_=}")                          # Should be 2
print(f"{r2._init_loc=}")                     # Should be [3,3]
print(f'{r2._max_weight=}')                   # Should be 10
print(f'{r2._total_time=}')                   # Should be 6
print(f'{r2.get_id()=}')                      # Should be 2
print(f'{r2.get_items_picked()=}')            # Should be []
print(f'{r2.total_operation_time()=}')        # Should be 0, no item picked yet
print(f'{r2.latest_resting_loc()=}')          # Should be [3,3]
print(f'{r2._items_picked.append(i2)=}')      # update the items picked, return none
print(f'{r2._items_picked.append(i3)=}')      # update the items picked, return none
print(f'{r2.get_items_picked()=}')            # Should be [i1 and i2's address]
# update item 1 and 2's status, with robots path time
print(f'pathtime={len(r2.travel_steps([3,3], [5,5]))-1=}')  #should be 4
print(f'pathtime={len(r2.travel_steps([3,3], [9,1]))-1=}')  #should be 8
print(f'{i2.update_pickup_status(4)=}')       #return None, picked item 1 used 4 timestep  
print(f'{i3.update_pickup_status(12)=}')       #return None, picked item 2 used 8 timestep  
print(f'{r2.total_operation_time()=}')        # total time should be 12+3=15
print(f'{r2.latest_resting_loc()=}')          # Should be [9,1]
print(f'{r2.get_location(25)=}')              # Should be at i3's location
#At resting, the robot is at the last item's position where the robot picked it up
# figure window8, centered at(3,3),with "2"(the id) inside the circle.
plt.figure(8); r2.draw(r2.latest_resting_loc())

#Test 3 with directly use pick module without manully update item's picked window
#create a robot id 3, max weight can pick is 40, with total opertaing time 20, 
#located at [1,1]
r3= Robot(3,40,20,[1,1])
print('\nTest 3 for class Robot\n---------------------')
print(f'{r3.latest_resting_loc()=}')          # Should be [1,1]
print(f'pathtime={len(r2.travel_steps(r3._init_loc, i4.loc))-1=}') #Should be 6
print(f'{r3.pick(i4)=}')                      # Should print True since the picked
                                              # condition is satisfied
print(f'{r3.total_operation_time()=}')        # total time should be 6+2=8
print(f'{r3.latest_resting_loc()=}')          # Should be [4,4]
print(f'{r3.get_location(25)=}')              # Should be at i4's location 
#At resting, the robot is at the last item's position where the robot picked it up
# figure window9, centered at(4,4),with "3"(the id) inside the circle.           
plt.figure(9); r3.draw(r3.latest_resting_loc())