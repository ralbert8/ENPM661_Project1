# IMPORT REQUIRED LIBRARIES #

import copy # Copying States
import random # Randomizing Initial State
import os # File Operations
from collections import deque # Queue for BFS



# COUNT INVERSIONS OF A STATE #
def count_inversions(flat_state):
    inversions = 0

    # Loop Over All Pairs of Numbers
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):

            # Increment Inversions if the Pair is Inverted
            if flat_state[i] and flat_state[j] and flat_state[i] > flat_state[j]:
                inversions += 1
    
    # Return the Number of Inversions
    return inversions



# CHECK SOLVABILITY OF A STATE #
def is_solvable(state):

    # Flatten the State
    flat_state = [num for row in state for num in row]

    # Return True if the Number of Inversions is Even, False if Odd
    return count_inversions(flat_state) % 2 == 0



# SOLVABLE START STATE GENERATION #
def generate_solvable_start():
    while True:
        
        # Create a List of Numbers 0-8
        numbers = list(range(9))

        # Shuffle the Numbers
        random.shuffle(numbers)

        # Reshape List into 3x3 Grid
        state = [numbers[i:i+3] for i in range(0, 9, 3)]

        # Return State if it is Solvable
        if is_solvable(state):
            return state



# FIND BLANK TILE #
def find_blank_tile(state):

    # Loop Over All Tiles
    for i in range(3):
        for j in range(3):

            # Return Index of Blank Tile
            if state[i][j] == 0:
                return i, j
            
    # Return None if Blank Tile is Not Found
    return None



# MOVE BLANK TILE LEFT #
def move_left(state):
    
    # Find Indices of Blank Tile
    i, j = find_blank_tile(state)

    # If Blank Tile is Not on the Left Edge
    if j > 0:

        # Copy the State of the System
        new_state = copy.deepcopy(state)

        # Swap the Blank Tile with the Tile to the Left
        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]

        # Return the New State
        return new_state
    
    # Return None if Blank Tile is on the Left Edge
    return None



# MOVE BLANK TILE RIGHT #
def move_right(state):
    
    # Find Indices of Blank Tile
    i, j = find_blank_tile(state)

    # If Blank Tile is Not on the Right Edge
    if j < 2:

        # Copy the State of the System
        new_state = copy.deepcopy(state)

        # Swap the Blank Tile with the Tile to the Right
        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]

        # Return the New State
        return new_state
    
    # Return None if Blank Tile is on the Right Edge
    return None



# MOVE BLANK TILE UP #
def move_up(state):

    # Find Indices of Blank Tile
    i, j = find_blank_tile(state)

    # If Blank Tile is Not on the Top Edge
    if i > 0:

        # Copy the State of the System
        new_state = copy.deepcopy(state)

        # Swap the Blank Tile with the Tile Above
        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]

        # Return the New State
        return new_state
    
    # Return None if Blank Tile is on the Top Edge
    return None



# MOVE BLANK TILE DOWN #
def move_down(state):

    # Find Indices of Blank Tile
    i, j = find_blank_tile(state)

    # If Blank Tile is Not on the Bottom Edge
    if i < 2:

        # Copy the State of the System
        new_state = copy.deepcopy(state)

        # Swap the Blank Tile with the Tile Below
        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]

        # Return the New State
        return new_state
    
    # Return None if Blank Tile is on the Bottom Edge
    return None



# SOLVE USING BFS #
def bfs_solve(start_state, goal_state):

    # Initialize Queue, Visited Dictionary, and Node Index
    queue = deque()
    visited = {}
    node_index = 0

    # Append Start State to Queue
    queue.append((start_state, node_index, -1))  # (state, index, parent_index)

    # Flatten Start State and Mark as Visited
    visited[tuple(map(tuple, start_state))] = node_index

    # Initialize List to Store Exploration Data
    nodes_info = []
    
    # While Queue is Not Empty
    while queue:

        # Pop the First Element from the Queue
        state, current_index, parent_index = queue.popleft()

        # Append Current State to Exploration Data
        nodes_info.append((current_index, parent_index, state))

        # If Current State is the Goal State
        if state == goal_state:

            # Return Exploration Data
            return nodes_info

        # Loop Over All Possible Moves
        for move in [move_left, move_right, move_up, move_down]:

            # Generate New State
            new_state = move(state)

            # If New State is Valid and Not Visited
            if new_state and tuple(map(tuple, new_state)) not in visited:

                # Increment Node Index
                node_index += 1

                # Mark New State as Visited
                visited[tuple(map(tuple, new_state))] = node_index

                # Append New State to Queue
                queue.append((new_state, node_index, current_index))

    # Return None if No Solution is Found
    return None



# BACKTRACK TO GENERATE PATH #
def generate_path(nodes_info, goal_index):

    # Initialize Path and Index Map
    path = []
    index_map = {node[0]: node for node in nodes_info}

    # While Goal Index is Not -1 (Start State)
    while goal_index != -1:

        # Append State to Path
        path.append(index_map[goal_index][2])

        # Move to Parent Index
        goal_index = index_map[goal_index][1]
    
    # Return Reversed Path
    return path[::-1]



# SAVE RESULTS #
def save_results(nodes_info, solution_path):
    
    # Find Directory of Script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change Directory to Script Directory
    os.chdir(script_dir)

    # Save Nodes
    with open(os.path.join("Nodes.txt"), "w") as f:
        for node in nodes_info:
            f.write(str(node[2]) + "\n")

    # Save Nodes Info
    with open(os.path.join("NodesInfo.txt"), "w") as f:
        for node in nodes_info:
            f.write(f"{node[0]} {node[1]} {node[2]}\n")

    # Save Solution Path
    with open(os.path.join("nodePath.txt"), "w") as f:
        for state in solution_path:
            flat_state = [str(state[i][j]) for j in range(3) for i in range(3)]
            f.write(" ".join(map(str, flat_state)) + "\n")

# EXECUTE BFS SOLVER #
if __name__ == "__main__":

    # Generate Solvable Start State
    start_state = generate_solvable_start()

    # Define Goal State
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # Solve Using BFS
    nodes_info = bfs_solve(start_state, goal_state)

    # If Solution is Found
    if nodes_info:

        # Generate Solution Path
        solution_path = generate_path(nodes_info, len(nodes_info) - 1)

        # Save Results
        save_results(nodes_info, solution_path)

        # Inform User of Success
        print("Solution found.")
    
    # If No Solution is Found
    else:

        # Inform User of Failure
        print("No solution found.")
