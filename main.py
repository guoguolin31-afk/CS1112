# For dynamic graphics, first use this command in the Spyder Python Console:
#     %matplotlib qt


from robot import Robot
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
        
        ##############################################################
        # TASK 1: Add code below to create a list of Robots and a 
        # list of Items.
        ##############################################################

        robots = []  # list of robots
        items = []   # list of items
        for line in fid:
            # `line` is a string, the next line of text in the file 
            # Split `line` into a list of strings, with comma as separator   
            tokens = line.strip().split(',')
            # TODO: ADD YOUR CODE BELOW FOR TASK 1

            # Read line that starts with R, indicates Robot
            if line[0]=="R":
                #read data and store it
                id_=int(tokens[1])
                max_w=float(tokens[2])
                locx=tokens[3].split('[')
                locy=tokens[4].split(']')
                loc=[float(locx[1]),float(locy[0])]
                #with the stored data, create a robot object and store it to 
                #robot's list
                robot=Robot(id_,max_w,sim_time,loc)
                robots.append(robot)
                
                
            # Read line that starts with I, indicates Item
            if line[0]=="I":
                #read data and store it
                id_=int(tokens[1])
                name=tokens[2]
                weight=float(tokens[3])
                locx_=tokens[4].split('[')
                locy_=tokens[5].split(']')
                loc_=[float(locx_[1]),float(locy_[0])]
                arm_req=int(tokens[6])
                duration=float(tokens[7])
                #with the stored data, create an item object and store it to 
                #item's list
                item=Item(id_,name,weight,loc_,arm_req,duration)
                items.append(item)
                
       
         ##############################################################
         # End of TASK 1
         ##############################################################
       
    # Do a task allocation
    items_remaining = simple_allocation(robots, items)

    #items[2].draw(1)   
    # Animate the simulation
    animate(robots, items, sim_time, room_size)

    # Print descriptive output
    output_results(robots, items_remaining)
    

def simple_allocation(robots, items):
    """
    Given a list of items and a list of robots, allocate item pickups to the robots.

    Algorithm: for each `Item` in `items`, look for the first `Robot` in `robots` 
    that is capable of picking it up. Pick up the `Item` with this first `Robot`.

    Returns: list; a list of remaining `Item`s that did not get picked up.
        
    Parameters:
    -----------

    robots: list; non-empty list of unique `Robot` references

    items: list; non-empty list of unique `Item` references
    """
    ##############################################################
    # TASK 2: Implement this function
    ##############################################################
    #initializing
    lis_remain=[]
    #for each item
    for i in range (len(items)): 
        item=items[i]
        r=0
        #look for the first robot that is capable of picking it up
        while r < len(robots):
             robot=robots[r]
             picked=robot.pick(item, True)
             if picked==True:
                r=len(robots)
             if picked==False:
                r=r+1
        #if no robots can pick it up, append it to list of remain items.
        if picked==False:
             lis_remain.append(item)
             
    # return remained items    
    return lis_remain

 

    ##############################################################
    # End of TASK 2
    ##############################################################


def animate(robots, items, sim_time, room_size):
    """
    Animate the robots and items in space for `sim_time` timesteps.  At each time 
    step, call the `draw` method for each `Item` and for each `Robot`. 

    For drawing a Robot at its correct location at each time step, you will find 
    the get_location() method helpful.

    Parameters
    ----------
    
    robots : list; list of `Robot` references

    items : list; list of `Item` references
    
    sim_time : int; number of timesteps
    
    roomsize : list; length-2 list that represents the dimensions of the room
    """
    plt.close('all')
    plt.figure()
    plt.pause(1)
    for t in range(0, sim_time + 1):
        # Clear axis
        plt.cla()
        plt.axis('equal')
        plt.axis('off')
        # Draw the room
        plt.axis([0, room_size[0] + 1, 0, room_size[1] + 1])
        plt.title(f"Time = {t}")

        ##################################################################
        # TASK 3: Add code for drawing the items and robots at time step t
        ##################################################################
        # TODO: ADD YOUR CODE BELOW
        
        #Draw items
        for i in range(len(items)):
            # Only draw items that still exist (not yet fully picked)
            if items[i].picked_window == None or t < items[i].picked_window.right:
                items[i].draw(t)

        #Draw robots
        for r in range(len(robots)):
            loc = robots[r].get_location(t)
            robots[r].draw(loc)

        ##################################################################
        # End of TASK 3
        ##################################################################
        
        b= 1  # blink time of 1 second for animation
        plt.pause(b)


def output_results(robots, items_remaining):
    """
    Prints the results of task allocation. Show the stats and tasks for each 
    `Robot` in `robots`:
    (1) Print the number of `Item`s picked and the total timesteps taken
    (2) Print out each `Item` picked and the time period taken to navigate to
    the object and pick it.

    Also print out each `Item` that the robots were not able to pick up.

    See the print format in the project description.
    
    Parameters:
    ------------
    
    robots: list; each element is a `Robot` in the simulation

    items_remaining: list; each element is an `Item` that the robots were not
    able to pick up.
    """

    ##############################################################
    # TASK 4: Implement this method
    ##############################################################
    print('------------------------')
    for r in range (len(robots)):
        if len(robots[r].get_items_picked()) == 0:
            print(f'Robot {robots[r]._id_} picked 0 items')
        if len(robots[r].get_items_picked()) != 0:
            timesteps=robots[r].get_items_picked()[-1].picked_window.right
            print(f'Robot {robots[r]._id_} picked {len(robots[r].get_items_picked())} in {timesteps} timesteps')
            for i in range (len(robots[r].get_items_picked())):
                item=robots[r].get_items_picked()[i]
                print(f'  {item.name} (ID {item.id_}): Assigned at time {item.picked_window.left}, picked up at time {item.picked_window.right}')
    print('------------------------')
    if len(items_remaining) !=0:
        print('The robots were not able to pick up:')
        for rem in range(len(items_remaining)):
            item_r=items_remaining[rem]
            print(f'  {item_r.name} (ID {item_r.id_})')
            print('------------------------')

                
    ##############################################################
    # End of TASK 4
    ##############################################################


if __name__ == '__main__':
    run_robots("room1.txt")
    
    
