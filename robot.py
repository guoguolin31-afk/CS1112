# robot.py


import math
from shapes import draw_disk
import matplotlib.pyplot as plt
import copy
import numpy as np


class Robot:
    """
    A robot has an ID, a maximum weight it can pick up, a total amount of time
    when it is operating, an initial location, and a list of items it has picked. 
    A robot moves in the cardinal directions only--north, east, south, west (NESW)
    --and moves one unit distance in each time step.

    The Robot class also has a class attribute `color`.

    Class attribute:
    -----------------
    
    color : str; Robot's color. A regular `Robot` is blue

    Instance Attributes:
    ---------------------

    _id_: int; the robot's identifier

    _max_weight: number; maximum weight that the robot can pick up at each pickup

    _total_time: int; the total number of time steps the robot is on (moving, picking)

    _init_loc: list; the initial location of the robot, represented as a list of two
    numbers (the x and y coordinates)

    _items_picked: list; each element of the list is an Item that the robot has 
    picked up. The list is initially empty
    """

    # Class attribute
    color = 'b'


    def __init__(self, id_, max_weight, total_time, init_loc):
        """
        Initializes a `Robot` object

        Parameters:
        ------------

        id_: int; robot's identifier

        max_weight: number; maximum weight that the robot is able to pick up

        total_time: int; total number of time steps the robot can be on, positive

        init_loc: list; a length-2 list of the initial location (x- and y-coord) 
        of the robot
        """
        self._id_ = id_
        self._max_weight = max_weight
        self._total_time = total_time
        self._init_loc = init_loc
        self._items_picked = []
        

    def get_id(self):
        """
        Returns (int) the `_id_` of the robot.
        """
        return self._id_


    def get_items_picked(self):
        """
        Returns a deep copy of `_items_picked`.
        """
        return copy.deepcopy(self._items_picked)


    def total_operation_time(self):
        """
        Returns the total operation time of the robot immediately after 
        completing its most recent Item pick-up. If no item has been picked 
        up, the total operation time is 0.
        """
        if len(self._items_picked) == 0:
            return 0
        last_item = self._items_picked[-1]
        return last_item.picked_window.right
    

    def latest_resting_loc(self):
        """
        Returns the latest resting location of the robot. If no item has been 
        picked up, the robot's latest resting location is just its initial 
        location; otherwise, the robot's latest resting location is where it 
        picked up the most recent item.
        """
        if len(self._items_picked) == 0:
            return self._init_loc
        last_item = self._items_picked[-1]
        return last_item.loc
    

    def draw(self, loc):
        """
        Draw a circle of diameter 1 to represent the robot at a given
        location `loc`. Label the circle at the center with its `_id_`.
        The color of the circle should match the `color` class attribute 
        of the robot.
        
        Assumes figure window is already open.
        
        Parameter:
        -----------
        
        loc: list; a length-2 list representing the location where the robot 
        should be drawn.
        """
        r = 0.5
        draw_disk(loc[0], loc[1], r, self.color)
        plt.text(loc[0], loc[1], str(self._id_), horizontalalignment='center')

    
    def travel_steps(self, curr, dest):
        """
        Returns a valid list of locations that form a path between two locations,
        `curr` and `dest`. Each location in the list corresponds to one time step. 
        The first location in the returned list should be `curr`, the robot's 
        current location; the last location in the list should be `dest`, the 
        robot's destination.  The return type is list; each element inside the
        list is a length 2 list storing an x-coordinate and a y-coordinate.

        While there are multiple ways to construct the path, one simple solution
        is to have the robot first move along the x-direction, then along the
        y-direction. 

        Parameters:
        -----------

        curr: list; a length-2 list storing the robot's current x-y coordinate

        dest: list; a length-2 list storing the robot's destiny x-y coordinate
        
        If `curr` and `dest` refer to the same location, return a length-1 list 
        containing this shared location.
        """
        # Set up the old and new x and y positions
        steps = []
        x1 = curr[0]
        y1 = curr[1]
        x2 = dest[0]
        y2 = dest[1]

        # Move along the x-direction
        delta_x = x2 - x1
        if not np.isclose(delta_x, 0):
            sign = int(delta_x / abs(delta_x))
            for x in range(x1, x2 + sign, sign):
                steps.append([x, y1])
        else:
            steps.append(curr)
        
        # Move along the y-direction
        delta_y = y2 - y1
        if not np.isclose(delta_y, 0):
            sign = int(delta_y / abs(delta_y))
            for y in range(y1 + sign, y2 + sign, sign):
                steps.append([x2, y])
        return steps
    

    def pick(self, item, do_pick=True, num_arms=0):
        """
        Returns True if the robot is able to pick up the item, False otherwise.
        
        If the robot is able to pick up the item, execute the pick-up if `do_pick`
        evaluates to True.
        
        Details are the same as in Project 5.

        Parameters:
        -----------
        
        item: Item; the item to be picked up by the robot

        do_pick: Boolean; indicates if the robot should execute the pick should 
        it be possible. Default is True.

        num_arms: int; the number of arms the robot has. Default is 0.
        """
        # Check if the robot can pick up the item
        robot_capable = item.valid_pickup(self._max_weight, num_arms)
        available_time = self._total_time - self.total_operation_time()
        curr = self.latest_resting_loc()
        dest = item.loc
        steps = self.travel_steps(curr, dest)
        travel_time = len(steps) - 1
        required_time = travel_time + item.duration
        have_time = required_time <= available_time
        item_waiting = item.picked_window is None
        success = robot_capable and have_time and item_waiting

        # Pick up the item if possible and required
        if success and do_pick:
            start_time = self.total_operation_time()
            pick_time = start_time + travel_time
            item.update_pickup_status(pick_time)
            self._items_picked.append(item)

        # Return `success`
        return success
    

    def get_location(self, t):
        """
        Provided method that computes the location of the robot at a queried
        time step t, where t >= 0.

        This method calls the total_operation_time(), latest_resting_loc(), and
        travel_steps() methods that you implemented and assumes correctness in
        these methods. 

        Read but DO NOT modify the code.
        """
        # If t is larger than the total operation time of the robot so far
        if t >= self.total_operation_time():
            return self.latest_resting_loc()
        # Determine which item the robot is handling at the queried time step
        index = 0
        while index < len(self._items_picked) and t > self._items_picked[index].picked_window.right:
            index += 1
        # If the robot is in the middle of picking up an item
        if t >= self._items_picked[index].picked_window.left:
            return self._items_picked[index].loc
        # Otherwise, the robot is in the middle of traveling
        if index == 0:
            curr = self._init_loc
            time_offset = t
        else:
            curr = self._items_picked[index - 1].loc
            time_offset = t - self._items_picked[index - 1].picked_window.right
        dest = self._items_picked[index].loc
        steps = self.travel_steps(curr, dest)
        return steps[time_offset]


class FastRobot(Robot):
    """
    A `FastRobot` is a `Robot`. A `FastRobot` can move at most `_speed_multiplier`
    distance in one timestep. A `FastRobot` is green ('g').
    
    Class attribute:
    -----------------
    
    color: str; FastRobot's color. A `FastRobot` is green
        
    Instance attributes:
    ---------------------

    _speed_multiplier: float; the distance that a `FastRobot` is able to move 
    in one time step
    """
    
    # Class attribute
    color = 'g'
    

    def __init__(self, id_, max_weight, total_time, init_loc,
                 speed_multiplier=np.random.uniform(1.0, 7.0)):
        """
        Construct a `FastRobot` with a speed multiplier.
        """
        self._speed_multiplier=speed_multiplier
        super().__init__(id_, max_weight, total_time, init_loc)

        
    def travel_steps(self, curr, dest):
        """
        Returns a valid list of locations that form a path between two locations,
        `curr` and `dest`. As for a regular Robot, each location in the list 
        corresponds to one time step. The first location in the returned list 
        should be `curr`; the last location in the list should be `dest`.

        Importantly, the FastRobot can move `_speed_multiplier` distance in one 
        timestep. Also, it can only move in one direction once it starts moving,
        meaning it can only move in the straight line path from `curr` to `dest`.

        Parameters:
        -----------

        curr: list; a length-2 list storing the robot's current x-y coordinate

        dest: list; a length-2 list storing the robot's destiny x-y coordinate
        
        If `curr` and `dest` refer to the same location, return a length-1 list 
        containing this shared location.

        Example 1: If a `FastRobot` with speed multiplier of 3 is to go from
        [0, 0] to [4, 0], then the list of locations is [[0, 0], [3, 0], [4, 0]]
        Example 2: If a 'FastRobot' with speed multiplier of sqrt(2) is to go from
        [0, 0] to [2, 2], then the list of locations is [[0, 0], [1, 1], [2, 2]]
        Example 3: If a 'FastRobot' with speed multiplier of 6 is to go from
        [0, 0] to [3, 4], then the list of locations is [[0, 0], [3, 4]]
        """
        lis=[curr]                                  #initialization
        k=1
        speed=self._speed_multiplier
        
        if curr[0]==dest[0] and curr[1]==dest[1]:   #angle calculation
            return lis         
        else:
            angle=np.arctan2(dest[1]-curr[1],dest[0]-curr[0])
            
        while k>0:                                  #loop until destination is 
            x=lis[-1][0]                            ##is reached
            y=lis[-1][1]
            x_dis=dest[0]-x
            y_dis=dest[1]-y
            distance=math.sqrt(x_dis**2+y_dis**2)
            if  speed>= distance:              #destination reached
                lis.append(dest)
                return lis
            else:
                x_curr=x+speed*math.cos(angle)
                y_curr=y+speed*math.sin(angle)
                lis.append([x_curr,y_curr])         #update location list
            
class LimbedRobot(Robot):
    """
    A `LimbedRobot` is a `Robot` that has arm capabilities and can lift
    heavier items. A `LimbedRobot` can only move `_slowdown_multiplier`
    distance in one timestep. A `LimbedRobot` is magenta ('m')
    
    Class attribute:
    -----------------
    
    color: str; LimbedRobot's color.  A `LimbedRobot` is magenta
        
    Instance attributes:
    ---------------------

    _num_arms: int; number of arms the `LimbedRobot` has

    _slowdown_multiplier: float; a `LimbedRobot` can move `_slowdown_multiplier` 
    units in one timestep. Assume this is in the range (0, 1)
    """
    
    # Class attribute
    color = 'm'


    def __init__(self, id_, max_weight, total_time, init_loc, num_arms,
                 slowdown_multiplier, max_load_factor=np.random.randint(2, 7)):
        """
        Construct a `LimbedRobot` that has arms, can carry heavier items, but
        moves at a slower speed.

        Parameters:
        ------------

        num_arms: int; corresponds to the `_num_arms` attribute

        slowdown_multiplier: float; corresponds to the `_slowdown_multiplier` 
        attribute

        max_load_factor: int; the value to use to adjust the `_max_weight` of 
        a `LimbedRobot`.  This parameter defaults to a random integer between 2 
        and 7.  The actual `_max_weight` of a `LimbedRobot` is
            max_weight * max_load_factor
        """
        super().__init__(id_, max_weight, total_time, init_loc)
        self._num_arms=num_arms
        self._slowdown_multiplier=slowdown_multiplier
        self._max_weight=max_weight*max_load_factor


    def travel_steps(self, curr, dest):
        """
        Returns a valid list of locations that form a path between two locations,
        `curr` and `dest`. As for a regular Robot, each location in the list 
        corresponds to one time step. The first location in the returned list 
        should be `curr`; the last location in the list should be `dest`.

        A `LimbedRobot` can only move `_slowdown_multiplier` distance in one time
        step and can only move in either the x or the y direction in one step.

        While there are multiple ways to construct the path, one simple solution
        is to have the robot first move along the x-direction, then along the
        y-direction.

        Parameters:
        -----------

        curr: list; a length-2 list storing the robot's current x-y coordinate

        dest: list; a length-2 list storing the robot's destiny x-y coordinate
        
        If `curr` and `dest` refer to the same location, return a length-1 list 
        containing this shared location.
        """
        # Set up the old and new x and y positions
        
        
        lis= [curr]
        x1 = curr[0]
        y1 = curr[1]
        x2 = dest[0]
        y2 = dest[1]
        stepsize=self._slowdown_multiplier
        
        #return if locations are the same
        if x1==x2 and y1==y2:
            return lis
        
        # Move along the x-direction
        delta_x = x2 - x1
        if x2>x1:
            notend=True
            while not np.isclose(delta_x, 0) and notend:
                x1=x1+stepsize
                delta_x = x2 - x1
                if x1>=x2:
                    notend=False
                    lis.append([x2,y1])
                else:
                    lis.append([x1, y1])
        elif x1>x2:
            notend=True
            while not np.isclose(delta_x, 0) and notend:
                x1=x1-stepsize
                delta_x = x2 - x1
                if x2>=x1:
                    notend=False
                    lis.append([x2,y1])
                else:
                    lis.append([x1, y1])
        
        # Move along the y-direction
        delta_y = y2 - y1
        if y2>y1:
            notend=True
            while not np.isclose(delta_y, 0) and notend:
                y1=y1+stepsize
                delta_y = y2 - y1
                if y1>=y2:
                    notend=False
                    lis.append([x2,y2])
                else:
                    lis.append([x2, y1]) 
        elif y1>y2:
            notend=True
            while not np.isclose(delta_y, 0) and notend:
                y1=y1-stepsize
                delta_y = y2 - y1
                if y2>=y1:
                    notend=False
                    lis.append([x2,y2])
                else:
                    lis.append([x2, y1])
                
        return lis
    

    def pick(self, item, do_pick=True):
        """
        Override `Robot`'s pick method.
        
        The only difference is that a `LimbedRobot` has some number of arms.
        """
        return super().pick(item,do_pick,self._num_arms)


