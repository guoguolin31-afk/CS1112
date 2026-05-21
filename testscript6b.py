# testscript6b.py
"""
Test script for Project 6 Part B
Test Maze initializer and method is_valid_move()

Your NetID(s):hl2573
"""

#from maze_solution import *
from maze import Maze

# Test with maze0: includes up, down, left, right moves, simple solution
print("Using maze0")
m= Maze("maze0.txt")
# Add your code below
print("Test initializer")
assert m.rows==10, f"{m.rows=} but should be 10"
assert m.cols==8, f"{m.cols=} but should be 8"
assert m.start==(1,1), f"{m.start=} but should be 1,1"
assert m.goal==(1,3), f"{m.goal=} but should be (1,3)"
print(f'{m.grid=}')
print("Initializers pass the test")

print("Test is_valid_move")
#up
assert m.is_valid_move(0,1)==False, f"{m.is_valid_move(0,1)=} but should be False"
#down
assert m.is_valid_move(2,1), f"{m.is_valid_move(2,1)=} but should be True"
#left
assert m.is_valid_move(1,0)==False, f"{m.is_valid_move(1,0)=} but should be False"
#right
assert m.is_valid_move(1,2)==False, f"{m.is_valid_move(1,2)=} but should be False"
print("is_valid_move pass the test")






