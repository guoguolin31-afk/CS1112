# maze.py
"""
Module for solving mazes using recursive backtracking.  Includes 
- Class Maze
- Function run_maze to make an instance and solve it

NumPy and pandas are NOT allowed on Project 6 Part B

Your NetID(s):hl2573
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
# DO NOT USE NumPy, pandas


class Maze:
    """
    Represents a maze that a robot can navigate from a starting position to a 
    goal position.  All moves must remain in the maze grid.

    A maze is represented as a rectangular grid of numbers where:
    - 0 represents an open path
    - 1 represents a wall

    Attributes:
        grid (list of list of int): rectangular grid representing the maze.
        rows (int): Number of rows in the maze.
        cols (int): Number of columns in the maze.
        start (tuple): (row, col) coordinates of the starting position.
        goal (tuple): (row, col) coordinates of the goal position.
        solution_path (list of tuple): List of (row, col) coordinates 
            representing the path from start to goal, empty if no solution.
    """

    def __init__(self, filename):
        """Initialize a Maze by reading from a file.

        The file format is:
        - First line: rows cols start_row start_col goal_row goal_col
        - Following lines: space-separated 0s and 1s representing the maze

        Example file:
        7 11 1 1 5 9
        1 1 1 1 1 1 1 1 1 1 1
        1 0 0 0 1 0 0 0 0 0 1
        1 1 1 0 1 0 1 1 1 0 1
        1 0 1 0 0 0 1 0 0 0 1
        1 0 1 1 1 1 1 0 1 0 1
        1 0 0 0 0 0 0 0 1 0 1
        1 1 1 1 1 1 1 1 1 1 1

        Args:
            filename (str): Path to the maze file.
            
        Initialize the solution_path attribute as an empty list.
        """

        with open(filename, 'r') as f:
            lines = f.readlines()
            
        # TODO: initialize all instance attributes
        # Hint: Use string parsing, e.g., use the methods strip(), split()
        # Remember to convert strings to integers where appropriate
            
            maze_info = lines[0].split()        #parse the first line
            self.rows=int(maze_info[0])
            self.cols=int(maze_info[1])
            self.start=(int(maze_info[2]),int(maze_info[3]))
            self.goal=(int(maze_info[4]),int(maze_info[5]))
            
            self.grid=[]        #parse the remaining line for grid
            for line in lines[1:]:
                grid=line.split()
                lis=[]
                for num in grid:
                    lis.append(int(num))    
                self.grid.append(lis)  
                
            self.solution_path=[]   #initialize solution_path


    def is_valid_move(self, row, col):
        """Check if a position is valid for the robot to move to.

        A position is valid if:
        1. It is within the maze boundaries 
        2. It is an open path, not a wall

        Args:
            row (int): Row coordinate.
            col (int): Column coordinate.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        # TODO: initialize all instance attributes
        
        if row < self.rows and col < self.cols and self.grid[row][col]==0:
            return True
        else: 
            return False
    


    def solve(self, row, col, visited):
        """Recursively solve the maze using backtracking.
        
        Base cases:
        - If current position is invalid or visited, return False
        - If current position is the goal, add it to solution_path and return True

        Recursive case:
        - Mark current position as visited
        - Try moving to the next cell in all 4 directions (up, down, 
          left, right).  For each direction, recursively call solve() on the  
          new position.
        - If any recursive call returns True, add current position to 
          solution_path and return True
        - If no direction works, backtrack by unmarking as visited and return False

        Args:
            row (int): Current row position.
            col (int): Current column position.
            visited (list of list of bool): rectangular grid (same size as the
                attribute `grid`) for tracking visited positions.

        Returns:
            bool: True if a path to the goal exists from this position,
                  False otherwise.
        """
        # TODO: Implement the recursive maze solving algorithm GIVEN ABOVE in
        #       the method docstring
        
        if self.is_valid_move(row,col)==False or visited[row][col]==True:
            return False
        if (row,col) == self.goal:
            self.solution_path.append((row,col))
            return True
        
        visited[row][col]=True
        if self.solve(row-1,col,visited)==True:
            self.solution_path.append((row-1,col))
            return True
        if self.solve(row+1,col,visited)==True:
            self.solution_path.append((row+1,col))
            return True
        if self.solve(row,col-1,visited)==True:
            self.solution_path.append((row,col-1))
            return True
        if self.solve(row,col+1,visited)==True:
            self.solution_path.append((row,col+1))
            return True
        else:
            visited[row][col]=False
            return False
            
    def find_path(self):
        """Find a path from start to goal in the maze.

        Initializes the search and starts the recursive solving process:
            
        - Start by creating a nested list the same size as the `grid` attribute
          to track which positions have been explored.  Call this nested list
          `visited`.  Each element of the inner list should have the value False.
          
        - Call method solve() starting from the start position.

        - After solving, if a path was found, reverse the solution_path because
          the path was built backwards during recursion (from goal back to start).

        Returns:
            bool: True if a path was found, False otherwise.
        """
        # TODO: implement me
        
        #create a nested list the same size as the 'grid' with boola Flse
        visited=[] 
        for i in range(len(self.grid)):
            visited.append([])
            for j in range(len(self.grid[0])):
                visited[i].append(False)
        
        #call solve()
        if self.solve(self.start[0],self.start[1],visited):
            self.solution_path.reverse()
            return True
        else:
            return False



    def draw(self, show_solution=False):
        """Draw the maze using matplotlib.

        This method visualizes the maze with:
        - Black rectangles for walls
        - White rectangles for open paths
        - Green circle for start position
        - Magenta circle for goal position
        - Blue line with markers for solution path (if show_solution=True)

        Args:
            show_solution (bool): Whether to display the solution path. Defaults to False.
        """
        # Create a figure and axis for drawing
        fig, ax = plt.subplots(figsize=(10, 8))

        # Draw each cell of the maze
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    # draw wall as black rectangle
                    rect = patches.Rectangle((col, row), 1, 1,
                                            facecolor='black', edgecolor='gray')
                else:
                    # draw path as white rectangle
                    rect = patches.Rectangle((col, row), 1, 1,
                                            facecolor='white', edgecolor='gray')
                ax.add_patch(rect)

        # Draw start position as green circle
        start_row, start_col = self.start
        start_circle = patches.Circle((start_col + 0.5, start_row + 0.5), 0.3,
                                     facecolor='green', edgecolor='darkgreen', linewidth=2)
        ax.add_patch(start_circle)

        # Draw goal position as magenta circle
        goal_row, goal_col = self.goal
        goal_circle = patches.Circle((goal_col + 0.5, goal_row + 0.5), 0.3,
                                    facecolor='magenta', edgecolor='darkmagenta', linewidth=2)
        ax.add_patch(goal_circle)

        # Draw the solution path if requested and it exists
        if show_solution and len(self.solution_path) > 0:
            # Extract x and y coordinates from solution_path
            # Add 0.5 to center the points in each cell
            x_coords = []
            y_coords = []
            for row, col in self.solution_path:
                x_coords.append(col + 0.5)
                y_coords.append(row + 0.5)

            # Draw the path as a blue line with circular markers
            ax.plot(x_coords, y_coords, color='blue', linewidth=3,
                   marker='o', markersize=8, markerfacecolor='lightblue',
                   markeredgecolor='blue', markeredgewidth=1)

        # Set up the plot appearance
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.set_aspect('equal')
        ax.invert_yaxis()  # Flip y-axis so (0,0) is at top-left
        ax.set_xticks([])
        ax.set_yticks([])

        # Add title
        title = 'Maze'
        if show_solution:
            if len(self.solution_path) > 0:
                title += f' Solution (Path Length: {len(self.solution_path)})'
            else:
                title += ' - No Solution'

        plt.title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()


def run_maze(filename):
    """Instantiates a Maze, solves it, displays result.

    This is a helper function that demonstrates the complete workflow:
    1. Instantiate a Maze object (load maze data from file)
    2. Display the unsolved maze
    3. Solve the maze
    4. Display the solution (if found)

    Args:
        filename (str): Path to the maze file.
    """

    # Load the maze
    maze = Maze(filename)

    # Display maze information
    print(f"Maze dimensions: {maze.rows} x {maze.cols}")
    print(f"Start position: {maze.start}")
    print(f"Goal position: {maze.goal}")

    # Check if start and goal are valid
    if maze.grid[maze.start[0]][maze.start[1]] == 1:
        print("WARNING: Start position is a wall!")
    if maze.grid[maze.goal[0]][maze.goal[1]] == 1:
        print("WARNING: Goal position is a wall!")

    print("\nDisplaying maze...")
    maze.draw(show_solution=False)

    # Solve the maze
    print("Solving maze...")
    found = maze.find_path()

    # Display results
    if found:
        print(f"Solution found! Path length: {len(maze.solution_path)}")
        print(f"First 5 steps: {maze.solution_path[:5]}")
        print(f"Last 5 steps: {maze.solution_path[-5:]}")
        print("Displaying solution...")
        maze.draw(show_solution=True)
    else:
        print("No solution exists for this maze.")


### Script code
if __name__ == '__main__':
    print("Load and solve mazes!")

    # TODO: Call   run_maze(maze_filename)   to load and solve some mazes 
    print('\nMaze 0---------------')
    run_maze("maze0.txt")
    print('\nMaze 1---------------')
    run_maze("maze1.txt")
    print('\nMaze 2---------------')
    run_maze("maze2.txt")
    print('\nMaze 3---------------')
    run_maze("maze3.txt")


