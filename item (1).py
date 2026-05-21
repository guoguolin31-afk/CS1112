# item.py


from interval import Interval
from shapes import draw_rect
import matplotlib.pyplot as plt

class Item:
    """
    An Item has an id_, a name, a weight, a location, the number of arms 
    required to lift it, the amount of time required to pick it up, and 
    a time window when pick-up is scheduled.
    """


    def __init__(self, id_, name, weight, loc, arm_requirement, duration):
        """
        Initializes an Item object
        
        Parameters:
        -----------
        
        id_: The item's identifier, an int
        
        name: The item's name, a string
        
        weight: The item's weight, a float
        
        loc: Location of the item, a list of length 2 (x coordinate followed
             by a y coordinate)
        
        arm_requirement: Number of arms required to pick up the item, an int
        
        duration: Time units necessary to fully pick up the item, an int
        """
        self.id_ = id_
        self.name = name
        self.weight = weight
        self.loc = loc
        self.arm_requirement = arm_requirement
        self.duration = int(duration)
        self.picked_window = None
        

    def valid_pickup(self, max_load, num_arms):
        """
        Returns True if a robot with a max picking capability of `max_load` 
        and `num_arms` number of arms is able to pick up the item; returns 
        False otherwise.        
        
        Parameters:
        ____________
        
        max_load: (int) the maxium weight that the picking robot can hold
        
        num_arms: (int) the number of arms of the picking robot
        """
        return self.arm_requirement<=num_arms and self.weight<=max_load
        


    def update_pickup_status(self, pickup_time):
        """
        Updates attribute `picked_window` to be an Interval indicating the 
        time window that the item is scheduled to be picked.
        
        The end point of `picked_window` should be `pickup_time` plus the 
        duration required to pick up the item.
            
        Returns None.
        
        Parameter:
        ____________
        
        pickup_time: (int) the time at which the robot reaches the item's 
            location and begins to pick it up
        """
        endpoint=int(pickup_time+self.duration)
        self.picked_window=Interval(pickup_time,endpoint)
        
        return None


    def draw(self, t):
        """
        Draws a red square of side length 1 centered over the item's location 
        at timestep `t` if and only if the item is not yet fully picked up at 
        time `t`.  Label the square at the center with the item's `id_`.
        
        An item is fully picked up at the end of its `picked_window` and so 
        should not be drawn at that time value.
        
        Assumes figure window is already open.
        
        Parameter:
        _____________
        
        t: (int, non-negative) the timestep
        """
        

        #Display the plot
        plt.plot()
        #plot precondition: draw if item has not been picked up yet
        if self.picked_window is None or t < self.picked_window.right:
            #draw
            s=str(self.id_)
            plt.text(self.loc[0],self.loc[1],s)
            lower_leftx=self.loc[0]-0.5
            lower_lefty=self.loc[1]-0.5
            draw_rect(lower_leftx,lower_lefty,1,1,'red')
