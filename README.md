# Warehouse

## Description
This project is a Python-based robot simulation system where robots navigate through a room to pick up items based on their weight capacity, travel time, and pickup requirements.

The simulation uses object-oriented programming principles and visualizes robot movement and item collection using Matplotlib.

## Features
- Robot and item object modeling
- Time-based pickup scheduling
- Robot movement simulation
- Path generation between locations
- Item allocation system
- Animated visualization using Matplotlib
- Room configuration through text files

## Technologies Used
- Python
- Matplotlib
- NumPy

## Project Structure
- `main.py` — Runs the simulation and handles allocation
- `robot.py` — Defines robot behaviors and movement
- `item.py` — Defines item properties and pickup logic
- `interval.py` — Handles time interval operations
- `shapes.py` — Draws shapes for visualization
- `room1.txt` — Simulation input data

## Simulation Overview
The robots move through a 2D room and attempt to pick up items if:
- the item weight is within capacity,
- the robot can reach the item in time,
- and the item has not already been assigned.

The simulation animates robot movement and displays pickup results.

## Concepts Practiced
- Classes and objects
- Data structures
- Simulation design
- File processing
- Visualization and animation
- Problem-solving with Python
