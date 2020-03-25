import heapq

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)
MOVE_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]



class Node:
    def __init__(self, state=None, parent=None, move=None, depth=None):
        """Node class for searching with A*"""
        self.parent = parent
        self.state = state
        self.move = move
        self.depth = depth

        self.g = 0
        self.h = 0
        self.f = 0

class State:
    """State class to be associated with 1 node"""
    def __init__(self, white_stacks, black_stacks):

        # white_stacks = {(3,2): 1, (3,4): 3}
        self.white_stacks = white_stacks
        self.black_stacks = black_stacks



def get_next_move(init_state, budget=100):

    # make the start node
    start_node = Node(None, init_state)

    # make a list of all the nodes we explore
    explored_nodes = []

    # make the frontier priority queue with only the start node
    frontier = []
    heapq.heappush(frontier, (0, init_state))

    # while there are still nodes in the frontier and we're not over budget, expand more
    while len(frontier) > 0 and len(explored_nodes) <= budget:
        current_node = heapq.heappop(frontier)
        explored_nodes += [current_node]

        # go through the list of applicable move actions and try them
        # go through the squares where we have a stack
        for stack in current_node.state.white_stacks.items():
            # iterate through each possible number of pieces to move from our stack at the current occupied_square
            for n_pieces in range(1, stack[1] + 1):
                # possible moving directions
                for move_direction in MOVE_DIRECTIONS:
                    # number of squares to move n_pieces from current stack, 1 <= n_steps <= stack
                    for n_steps in range(1, n_pieces + 1):
                        # check if moving n_steps in move_direction from current stack is a legal move (i.e. not out of bounds and not landing on an enemy piece)
                        if is_legal_move(current_node.state.black_stacks, stack[0], move_direction, n_steps):
                            # make a child node that is the result of applying this move action to the current_node
                            child_node = apply_action(current_node, stack, n_pieces, move_direction, n_steps)


def is_legal_move(enemy_stack_locations, moving_stack_location, move_direction, n_steps):
    """ check if moving n_steps in move_direction from current stack is a legal move (i.e. not out of bounds and not landing on an enemy piece)"""
    dest_square = calculate_dest_square(moving_stack_location, move_direction, n_steps)
    return bool((dest_square[0] in range(0, 8)) and (dest_square[1] in range(0, 8)) and (dest_square not in enemy_stack_locations))

def calculate_dest_square(moving_stack_location, move_direction, n_steps):
    return (moving_stack_location[0] + n_steps * move_direction[0], moving_stack_location[1] + n_steps * move_direction[1])

def apply_action(base_node, stack, n_pieces, move_direction, n_steps):
    """apply a move action to the given base node by moving n_pieces from stack n_steps in move_direction"""
    dest_square = calculate_dest_square(stack, move_direction, n_steps)

    # make a new node that is a copy of the base_node
    new_node = Node(base_node)

    # adjust new_node fields according to how our move will change them:
    # parent node of the new_node is the base_node
    new_node.parent = base_node
    # new_node depth is parent depth + 1
    new_node.depth = base_node.depth + 1
    # store the move which got us to new_node
    new_node.move = (stack, n_pieces, move_direction, n_steps)

    # execute move on new_node state
    stack_index = base_node.state.stack_locations.index(stack)
    # check if we moved the whole stack, remove square coords from stack_locations in that case
    if base_node.state.stack_quantities[stack_index] == n_pieces:
        base_node.state.stack_quantities.pop(stack_index)
        base_node.state.stack_locations.pop(stack_index)


    return ...

def boom_action(base_node, stack):
    white_pos = base_node.state.white_stacks[0];
    radius_x = [white_pos[0], white_pos[0], white_pos[0]-1, white_pos[0]-1, white_pos[0]-1, white_pos[0]+1, white_pos[0]+1, white_pos[0]+1]
    radius_y = [white_pos[1]-1, white_pos[1]+1, white_pos[1], white_pos[1]-1, white_pos[1]+1, white_pos[1], white_pos[1]-1, white_pos[1]+1]
    radius = zip(radius_x, radius_y)
    for black_stack in base_node.state.black_stacks:
        for r in radius:
            if (black_stack[1] == r):
                pop(black_stack)

