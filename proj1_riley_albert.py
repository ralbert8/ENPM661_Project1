import copy
import random
import os
from collections import deque



def count_inversions(flat_state):

    """
    Counts the number of inversions in a flat list.

    Args:
        flat_state (list): A flat list representing the state of the puzzle.

    Returns:
        int: The number of inversions in the list
    """

    inversions = 0

    # Loop over all pairs of numbers
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):

            # Increment inversion count if pair is inverted
            if flat_state[i] and flat_state[j] and flat_state[i] > flat_state[j]:
                inversions += 1
    
    # Return the number of inversions
    return inversions



def is_solvable(state):

    """
    Checks if a given state of the 8-puzzle is solvable.

    Args:
        state(list): A 3x3 list representing the state of the puzzle.

    Returns:
        bool: True if the state is solvable. False otherwise.
    """

    # Flatten the state
    flat_state = [num for row in state for num in row]

    # Return true if the number of inversions is even. False if odd
    return count_inversions(flat_state) % 2 == 0



def generate_solvable_start():

    """
    Generates a random solvable state for the 8-puzzle.

    Returns:
        list: A 3x3 list represnting a solvable state of the puzzle.
    """

    # Loop until a solvable state is generated
    while True:
        
        # Create a list of numbers 0-8
        numbers = list(range(9))

        # Shuffle the numbers
        random.shuffle(numbers)

        # Reshape into a 3x3 grid
        state = [numbers[i:i+3] for i in range(0, 9, 3)]

        # Return state if solvable
        if is_solvable(state):
            return state



def find_blank_tile(state):

    """
    Finds the indices of the blank tile (0) in the state.

    Returns:
        tuple | None: A tuple (i, j) representing the row and column indices of the blank tile. None if the blank tile is not found.
    """

    # Loop Over All Tiles
    for i in range(3):
        for j in range(3):

            # Return index of the blank tile.
            if state[i][j] == 0:
                return i, j
            
    # Return None if the blank tile is not found
    return None



def move_left(state):

    """
    Moves the blank tile (0) to the left if valid.

    Arguments:
        state (list): A 3x3 list representing the current state of the puzzle.

    Returns:
        list | None: A new state with the blank tile moved left. None if the move is invalid.
    """
    
    # Find indices of blank tile
    i, j = find_blank_tile(state)

    # If blank tile is not on the left edge
    if j > 0:

        # Copy the state of the system
        new_state = copy.deepcopy(state)

        # Swap the blank tile with the tile to the left
        new_state[i][j], new_state[i][j-1] = new_state[i][j-1], new_state[i][j]

        # Return the new state
        return new_state
    
    # Return None if blank tile is on the left edge
    return None



def move_right(state):
    
    """
    Moves the blank tile (0) to the right if valid.

    Arguments:
        state (list): A 3x3 list representing the current state of the puzzle.

    Returns:
        list | None: A new state with the blank tile moved right. None if the move is invalid.
    """

    # Find indices of blank tile
    i, j = find_blank_tile(state)

    # If blank tile is not on the right edge
    if j < 2:

        # Copy the state of the system
        new_state = copy.deepcopy(state)

        # Swap the blank tile with the tile to the right
        new_state[i][j], new_state[i][j+1] = new_state[i][j+1], new_state[i][j]

        # Return the new
        return new_state
    
    # Return None if blank tile is on the right edge
    return None



def move_up(state):

    """
    Moves the blank tile (0) up if valid.

    Arguments:
        state (list): A 3x3 list representing the current state of the puzzle.

    Returns:
        list | None: A new state with the blank tile moved up. None if the move is invalid.
    """

    # Find indices of blank tile
    i, j = find_blank_tile(state)

    # If blank tile is not on the top edge
    if i > 0:

        # Copy the state of the system
        new_state = copy.deepcopy(state)

        # Swap blank tile with the tile above
        new_state[i][j], new_state[i-1][j] = new_state[i-1][j], new_state[i][j]

        # Return the new state
        return new_state
    
    # Return none if the blank tile is on the top edge
    return None



def move_down(state):

    """
    Moves the blank tile (0) down if valid.

    Arguments:
        state (list): A 3x3 list representing the current state of the puzzle.

    Returns:
        list | None: A new state with the blank tile moved down. None if the move is invalid.
    """

    # Find indices of blank tile
    i, j = find_blank_tile(state)

    # If blank tile is not on the bottom edge
    if i < 2:

        # Copy the state of the system
        new_state = copy.deepcopy(state)

        # Swap the blank tile with the tile below
        new_state[i][j], new_state[i+1][j] = new_state[i+1][j], new_state[i][j]

        # Return the new state
        return new_state
    
    # Return none if the blank tile is on the bottom edge
    return None



def bfs_solve(start_state, goal_state):

    """
    Solves the 8-puzzle using the Breadth-First Search (BFS) algorithm.

    Arguments:
        start_state (list): A 3x3 list representing the starting state of the puzzle.
        goal_state (list): A 3x3 list representing the goal state of the puzzle.

    Returns:
        list | None: A list of tuples representing the exploration data. Each tuple contains
        (node_index, parent_index, state). None if no solution is found.
    """

    # Initialize queue, visited dictionary, and node index
    queue = deque()
    visited = {}
    node_index = 0

    # Append start state to queue (state, index, parent index)
    queue.append((start_state, node_index, -1))

    # Flatten start state and mark as visited
    visited[tuple(map(tuple, start_state))] = node_index

    # Initialize list to store exploration data
    nodes_info = []
    
    # While queue is not empty
    while queue:

        # Pop first element from queue
        state, current_index, parent_index = queue.popleft()

        # Append current state to exploration data
        nodes_info.append((current_index, parent_index, state))

        # If current state is the goal state
        if state == goal_state:

            # Return exploration data
            return nodes_info

        # Loop over all possible moves
        for move in [move_left, move_right, move_up, move_down]:

            # Generate new state
            new_state = move(state)

            # If new state is valid and unvisited
            if new_state and tuple(map(tuple, new_state)) not in visited:

                # Increment node index
                node_index += 1

                # Mark new state as visited
                visited[tuple(map(tuple, new_state))] = node_index

                # Append new state to queue
                queue.append((new_state, node_index, current_index))

    # Return none if no solution is found
    return None



def generate_path(nodes_info, goal_index):

    """
    Generates the solution path from the exploration data.

    Arguments:
        nodes_info (list): A list of tuples representing the exploration data.
        goal_index (int): The index of the goal state in the exploration data.

    Returns:
        list: A list of states representing the solution path from start to goal.
    """

    # Initialize path and index map
    path = []
    index_map = {node[0]: node for node in nodes_info}

    # While goal index is not -1 (Start state)
    while goal_index != -1:

        # Append state to path
        path.append(index_map[goal_index][2])

        # Move to parent index
        goal_index = index_map[goal_index][1]
    
    # Return reversed path
    return path[::-1]



def save_results(nodes_info, solution_path):

    """
    Saves the exploration data and solution path to .txt files.

    Arguments:
        nodes_info (list): A list of tuples representing the exploration data.
        solution_path (list): A list of states representing the solution path from start to goal.
    """
    
    # Find directory of script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change working directory to script directory
    os.chdir(script_dir)

    # Save nodes
    with open(os.path.join("Nodes.txt"), "w") as f:
        for node in nodes_info:
            f.write(str(node[2]) + "\n")

    # Save nodes info
    with open(os.path.join("NodesInfo.txt"), "w") as f:
        for node in nodes_info:
            f.write(f"{node[0]} {node[1]} {node[2]}\n")

    # Save solution path
    with open(os.path.join("nodePath.txt"), "w") as f:
        for state in solution_path:
            flat_state = [str(state[i][j]) for j in range(3) for i in range(3)]
            f.write(" ".join(map(str, flat_state)) + "\n")



if __name__ == "__main__":

    # Generate solvable start state
    start_state = generate_solvable_start()

    # Define goal state
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    # Solve using BFS
    nodes_info = bfs_solve(start_state, goal_state)

    # If solution is found
    if nodes_info:

        # Generate solution path
        solution_path = generate_path(nodes_info, len(nodes_info) - 1)

        # Save results
        save_results(nodes_info, solution_path)

        # Inform user of success
        print("Solution found.")
    
    # If no solution is found
    else:

        # Inform user of failure
        print("No solution found.")
