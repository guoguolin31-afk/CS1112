# main6a.py
"""
Module for Project 6A Robot Task Allocation
Read data file to instantiate Item and Robot objects.
Perform task allocation.

For dynamic graphics, first use this command in the Spyder Python Console:
     %matplotlib qt
"""

from robot import Robot, FastRobot, LimbedRobot
from item import Item
import numpy as np
import matplotlib.pyplot as plt


def run_robots(data_filename):
    """
    Create an allocation of robots to pickup items given a data file in the
    necessary format.

    Parameter:
    -----------
    
    data_filename: string; the name of the data file.
    """
    with open(data_filename, 'r') as fid:
        # Process the first line of the file
        line = fid.readline()
        sim_info = line.strip().split(',')
        sim_time = int(sim_info[0])
        horiz_dim = float(sim_info[1])
        vert_dim = float(sim_info[2])
        room_size = np.array([horiz_dim, vert_dim])

        # Process the remaining lines of the file
        robots = []  # list of robots
        items = []  # list of items
        for line in fid:
            # split `line` into a list of strings, with comma as separator
            tokens = line.strip().split(',')

            # Parse each object
            if tokens[0][0] == 'I':
                id_ = int(tokens[1])
                name = tokens[2].strip()
                weight = float(tokens[3])
                x_loc = int(tokens[4].strip()[1:])
                y_loc = int(tokens[5].strip()[0:-1])
                loc = [x_loc, y_loc]
                arms_required = int(tokens[6])
                duration = int(tokens[7].strip())
                items.append(Item(id_, name, weight, loc, arms_required, duration))
            elif tokens[0][0] == 'R':
                id_ = int(tokens[1])
                max_weight = float(tokens[2])
                x_loc = int(tokens[3].strip()[1:])
                y_loc = int(tokens[4].strip()[0:-1])
                init_loc = [x_loc, y_loc]
                robots.append(Robot(id_, max_weight, sim_time, init_loc))
            elif tokens[0][0] == 'F':
                id_ = int(tokens[1])
                max_weight = float(tokens[2])
                x_loc = int(tokens[3].strip()[1:])
                y_loc = int(tokens[4].strip()[0:-1])
                init_loc = [x_loc, y_loc]
                speed_multiplier = float(tokens[5])
                robots.append(FastRobot(id_, max_weight, sim_time, init_loc, speed_multiplier))
            elif tokens[0][0] == 'L':
                id_ = int(tokens[1])
                max_weight = float(tokens[2])
                x_loc = int(tokens[3].strip()[1:])
                y_loc = int(tokens[4].strip()[0:-1])
                init_loc = [x_loc, y_loc]
                num_arms = int(tokens[5])
                slowdown_multiplier = float(tokens[6])
                max_load_factor = int(tokens[7])
                robots.append(LimbedRobot(id_, max_weight, sim_time, init_loc, 
                                          num_arms, slowdown_multiplier, max_load_factor))

    # Do a task allocation
    #items_remaining = simple_allocation(robots, items)
    items_remaining = create_allocation(robots, items, sim_time)

    # Animate the simulation
    animate(robots, items, sim_time, room_size)

    # Print descriptive output
    output_results(robots, items_remaining)


def simple_allocation(robots, items):
    """
    Given a list of items and a list of robots, allocate item pickups to the robots.
    For each `Item` in `items`, we look for the first `Robot` in `robots` that is 
    capable of picking it up. Pick up the `Item` with this first `Robot`.

    Returns: list; a list of remaining `Item`s that did not get picked up.
        
    Parameters:
    -----------

    robots: list; non-empty list of unique `Robot` references

    items: list; non-empty list of unique `Item` references
    """
    items_remaining = []
    nRobot = len(robots)
    for item in items:
        is_picked = False
        index = 0
        while is_picked == False and index < nRobot:
            is_picked = robots[index].pick(item)
            index += 1
        if not is_picked:
            items_remaining.append(item)
    return items_remaining

def create_allocation(robots, items, sim_time):
    """
    Given a list of items and a list of robots, allocate item pickups to the robots.

    Algorithm: for each item, loop through the robots to find the robot that minimizes 
    the objective 
    
        0.8 * time_needed + 0.2 * time_ratio

    and make it perform the pick. time_needed is the total time the robot needs to pick 
    an item (getting there and picking it up). time_ratio is time_needed divided by the
    time the robot has left until the simulation ends, before traveling to the item.

    Returns: list; a list of remaining `Item`s that did not get picked up.
    
    Parameters:
    -----------

    robots: list; non-empty list of unique `Robot` references

    items: list; non-empty list of unique `Item` references
    """
    a = 0.8  # weight for the time_needed objective
    b = 0.2  # weight for the time_ratio objective
    items_remaining=[] # list for remaining items
    
    #allocation
    for item in items:
        weights=[]          #list for weights
        work_robot=[]       #list of robot that have weights
        #check if item is pickable and calculate the weight of the robot 
        #and store it for comparsion
        for robot in robots:
            if robot.pick(item,False)==True:
                time_need=len(robot.travel_steps(robot.latest_resting_loc(),item.loc))-1+item.duration
                time_ratio=time_need/(sim_time-robot.total_operation_time())
                weight=a*time_need+b*time_ratio
                weights.append(weight)
                work_robot.append(robot)
        #if item is not pickable, store the item to remaining list
        if len(weights)==0:
            items_remaining.append(item)
        
        #if item is pickable,check for the robot that have the smaller weight
        else:
            best_robot=work_robot[0]
            ibest=weights[0]
            for i in range(len(weights)):
                if weights[i]<ibest:
                    ibest=weights[i]
                    best_robot=work_robot[i]
            #the robot has the smaller weight pick up the item
            best_robot.pick(item)
            
    return items_remaining
                    
def animate(robots, items, sim_time, room_size):
    """
    Animate the robots and items in space for `sim_time` timesteps.  At each time 
    step, call the `draw` method for each `Item` and for each `Robot`. 

    Parameters
    ----------
    
    robots : list; list of `Robot` references

    items : list; list of `Item` references
    
    sim_time : int; number of timesteps
    
    roomsize : list; length-2 list that represents the dimensions of the room
    """
    blinktime= 0.1
    plt.close('all')
    plt.figure()
    plt.pause(1)
    for t in range(0, sim_time + 1):
        plt.cla()
        plt.axis('equal')
        plt.axis('off')
        plt.axis([0, room_size[0] + 1, 0, room_size[1] + 1])
        plt.title(f"Time = {t}")
        for item in items:
            item.draw(t)
        for robot in robots:
            loc = robot.get_location(t)
            robot.draw(loc)
        plt.pause(blinktime)


def output_results(robots, items_remaining):
    """
    Prints the results of task allocation. Show the stats and tasks for each 
    `Robot` in `robots`, and also print out each `Item` that the robots were 
    not able to pick up.
    
    Parameters:
    ------------
    
    robots: list; each element is a `Robot` in the simulation

    items_remaining: list; each element is an `Item` that the robots were not
    able to pick up.
    """
    print("-------------------------------")
    for robot in robots:
        picked = robot.get_items_picked()
        t = robot.total_operation_time()
        print(f"Robot {robot.get_id()} picked {len(picked)} items in {t} timesteps")
        for item in picked:
            print(f"  {item.name} (ID {item.id_}): Assigned at time",
                  f"{item.picked_window.left}, picked up at time {item.picked_window.right}")
    print("-------------------------------")
    print("The robots were not able to pick up:")
    for item in items_remaining:
        print(f"  {item.name} (ID {item.id_})")
    print("-------------------------------")


if __name__ == '__main__':
    run_robots("room2.txt")