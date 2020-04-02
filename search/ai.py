import heapq
import sys
from copy import deepcopy

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, 1)
DOWN = (0, -1)
MOVE_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
MOVE = "MOVE"
BOOM = "BOOM"

# values for the heuristic
LOST_GAME = sys.maxsize
WIN_GAME = -sys.maxsize
#sys.setrecursionlimit(10000)


class Node:
    def __init__(self, state, parent=None, move=None, depth=0, h=0, f=0):
        """Node class for searching with A*"""
        self.parent = parent
        self.state = state
        self.move = move
        self.depth = depth

        # a* value: f(n) = h(n)<-heuristic + g(n)<-depth
        self.h = heuristic(state)
        self.f = h + depth

    def __lt__(self, other):
        return self.f < other.f


class State:
    """State class to be associated with 1 node"""
    def __init__(self, white_stacks, black_stacks):

        # white_stacks = {(3,2): 1, (3,4): 3}
        self.white_stacks = white_stacks
        self.black_stacks = black_stacks

    def __eq__(self, other):
            return bool((self.white_stacks == other.white_stacks) and (self.black_stacks == other.black_stacks))

    def total_white(self):
        return sum(self.white_stacks.values())

    def total_black(self):
        return sum(self.black_stacks.values())


def heuristic(state):
    if State.total_black(state) == 0:
        return WIN_GAME
    if State.total_white(state) == 0:
        return LOST_GAME
    # else, the heuristic is the number of enemy pieces on the board, lower is better
    return State.total_black(state) + manhattan_dist(state)

def manhattan_dist(state):
    sum = 0
    for white in state.white_stacks.items():
        current_sum = 0
        for black in state.black_stacks.items():
            current_sum += calculate_dist(white[0], black[0])
        sum += current_sum/len(state.black_stacks)
    return sum/len(state.white_stacks)

def get_winning_sequence(start_node):

    # make a list of all the nodes we explore
    explored_nodes = []

    # make the frontier priority queue with only the start node
    frontier = []
    heapq.heappush(frontier, (0, start_node))

    winning_node = None

    # each action takes the form: (score, (stack_location, is_boom_action, n_pieces, move_direction, n_steps))
    # score will be the number of enemy pieces left on board, ties broken randomly
    # while there are still nodes in the frontier and we have not found the winning sequence, expand more
    # find the winning node
    while len(frontier) > 0:
        current_node = heapq.heappop(frontier)[1]
        explored_nodes += [current_node]

        # go through the list of applicable BOOM actions and try them
        for stack in current_node.state.white_stacks.items():
            child_node = boom_action(current_node, stack[0])
            # check if we're not adding an already visited state
            if child_node.state not in [e.state for e in explored_nodes]:
                explored_nodes += [child_node]
                heapq.heappush(frontier, (child_node.f, child_node))
            # check if we just won
            if State.total_black(child_node.state) == 0:
                winning_node = child_node
                break
        # break the while loop, because we've already found the winning_node
        if winning_node is not None:
            break
        # go through the list of applicable MOVE actions and try them
        # go through the squares where we have a stack
        for stack in current_node.state.white_stacks.items():
            # iterate through each possible number of pieces to move from our stack at the current occupied_square
            for n_pieces in range(1, stack[1] + 1):
                # possible moving directions
                for move_direction in MOVE_DIRECTIONS:
                    # number of squares to move n_pieces from current stack, 1 <= n_steps <= n_pieces
                    for n_steps in range(1, stack[1] + 1):
                        # check if moving n_steps in move_direction from current stack is a legal move (i.e. not out of bounds and not landing on an enemy piece)
                        if is_legal_move(current_node.state.black_stacks, stack[0], move_direction, n_steps):
                            # make a child node that is the result of applying this move action to the current_node
                            child_node = apply_action(current_node, stack[0], n_pieces, move_direction, n_steps)
                            # make sure we're not duplicating states
                            if child_node.state not in [e.state for e in explored_nodes]:
                                explored_nodes += [child_node]
                                heapq.heappush(frontier, (child_node.f, child_node))

    # we have the winning_node, now we calculate the sequence of moves made to get that node.
    moves_made = []
    curr = winning_node
    while curr.parent is not None:
        moves_made += [curr.move]
        curr = curr.parent
    return list(reversed(moves_made))

def get_next_move(start_node, budget=100):


    # make a list of all the nodes we explore
    explored_nodes = []

    # make the frontier priority queue with only the start node
    frontier = []
    heapq.heappush(frontier, (0, start_node))

    # each action takes the form: (score, (stack_location, is_boom_action, n_pieces, move_direction, n_steps))
    # score will be the number of enemy pieces left on board, ties broken randomly
    best_action = ()

    # while there are still nodes in the frontier and we're not over budget, expand more
    while len(frontier) > 0 and len(explored_nodes) <= budget:
        current_node = heapq.heappop(frontier)[1]
        explored_nodes += [current_node]

        # go through the list of applicable BOOM actions and try them
        # go through the squares where we have a stack
        for stack in current_node.state.white_stacks.items():
            child_node = boom_action(current_node, stack[0])
            if child_node.state not in [e.state for e in explored_nodes]:
                explored_nodes += [child_node]
                heapq.heappush(frontier, (child_node.f, child_node))


        # go through the list of applicable MOVE actions and try them
        # go through the squares where we have a stack
        for stack in current_node.state.white_stacks.items():
            # iterate through each possible number of pieces to move from our stack at the current occupied_square
            for n_pieces in range(1, stack[1] + 1):
                # possible moving directions
                for move_direction in MOVE_DIRECTIONS:
                    # number of squares to move n_pieces from current stack, 1 <= n_steps <= n_pieces
                    for n_steps in range(1, stack[1] + 1):
                        # check if moving n_steps in move_direction from current stack is a legal move (i.e. not out of bounds and not landing on an enemy piece)
                        if is_legal_move(current_node.state.black_stacks.items(), stack[0], move_direction, n_steps):
                            # make a child node that is the result of applying this move action to the current_node
                            child_node = apply_action(current_node, stack[0], n_pieces, move_direction, n_steps)
                            # make sure we're not duplicating states
                            if child_node.state not in [e.state for e in explored_nodes]:
                                explored_nodes += [child_node]
                                heapq.heappush(frontier, (child_node.f, child_node))

def calculate_dist(start, destination):
    return (abs(destination[0] - start[0]) + abs(destination[1] - start[1]))


def is_legal_move(enemy_stack_locations, moving_stack_location, move_direction, n_steps):
    """ check if moving n_steps in move_direction from current stack is a legal move (i.e. not out of bounds and not landing on an enemy piece)"""
    dest_square = calculate_dest_square(moving_stack_location, move_direction, n_steps)
    return bool((dest_square[0] in range(0, 8)) and (dest_square[1] in range(0, 8)) and (
            dest_square not in enemy_stack_locations))

def calculate_dest_square(moving_stack_location, move_direction, n_steps):
    return (
        moving_stack_location[0] + n_steps * move_direction[0], moving_stack_location[1] + n_steps * move_direction[1])

def apply_action(base_node, stack, n_pieces, move_direction, n_steps):
    """apply a move action to the given base node by moving n_pieces from stack n_steps in move_direction"""
    dest_square = calculate_dest_square(stack, move_direction, n_steps)

    # make a new node that is a copy of the base_node
    new_node = Node(State(base_node.state.white_stacks.copy(), base_node.state.black_stacks.copy()))

    # adjust new_node fields according to how our move will change them:
    # parent node of the new_node is the base_node
    new_node.parent = base_node
    # new_node depth is parent depth + 1
    new_node.depth = base_node.depth + 1
    # store the move which got us to new_node
    new_node.move = (MOVE, n_pieces, stack, dest_square)

    # execute move on new_node state
    # move the pieces from the stack to a new stack
    new_node.state.white_stacks[stack] -= n_pieces
    if new_node.state.white_stacks[stack] == 0:
        new_node.state.white_stacks.pop(stack)
    if dest_square in new_node.state.white_stacks:
        # there is already a stack in the square we are moving to, just add number of pieces
        new_node.state.white_stacks[dest_square] += n_pieces
    else:
        # we have to make a new key value pair because we made a new stack
        new_node.state.white_stacks[dest_square] = n_pieces

    # update the a* node value
    new_node.h = heuristic(new_node.state)
    new_node.f = new_node.h + new_node.depth

    return new_node

# new boom function needs to be made
def chain_boom(state, stack_to_boom, stacks_to_remove=None):
    # add the stack_to_boom to the stacks_to_remove
    if stacks_to_remove is None:
        stacks_to_remove = set()
    stacks_to_remove.add(stack_to_boom)

    # go through all the adjacent stacks to stack_to_boom
    # add the stack to the stacks to be removed
    # make a boom radius from stack_to_boom
    radius_x = [stack_to_boom[0], stack_to_boom[0], stack_to_boom[0] - 1, stack_to_boom[0] - 1,
                stack_to_boom[0] - 1, stack_to_boom[0] + 1,
                stack_to_boom[0] + 1, stack_to_boom[0] + 1]
    # possible corresponding y coordinates e.g. (2,2): [1, 3, 2, 1, 3, 2, 1, 3]
    radius_y = [stack_to_boom[1] - 1, stack_to_boom[1] + 1, stack_to_boom[1], stack_to_boom[1] - 1,
                stack_to_boom[1] + 1, stack_to_boom[1],
                stack_to_boom[1] - 1, stack_to_boom[1] + 1]
    radius = list(zip(radius_x, radius_y))

    # get a list of all the squares where the boom hit
    all_stacks = list(state.white_stacks.keys()) + list(state.black_stacks.keys())
    stacks_hit = list(set(all_stacks).intersection(radius))

    # add all the stacks_stacks_hit to the stacks_to_remove set, if they havent been added before, boom them
    for st in stacks_hit:
        if st not in stacks_to_remove:
            stacks_to_remove.add(st)
            chain_boom(state, st, stacks_to_remove)

    # remove stacks_to_remove from state and return state
    for st in stacks_to_remove:
        if st in state.white_stacks:
            state.white_stacks.pop(st)
        if st in state.black_stacks:
            state.black_stacks.pop(st)
    return state

# overloaded function for boom actions, return a new node
def boom_action(base_node, stack_to_boom):

    # make a new node that is a copy of the base_node
    new_node = Node(State(base_node.state.white_stacks.copy(), base_node.state.black_stacks.copy()))

    # adjust new_node fields according to how the boom change them:
    # parent node of the new_node is the base_node
    new_node.parent = base_node
    # new_node depth is parent depth + 1
    new_node.depth = base_node.depth + 1
    # store the move which got us to new_node
    new_node.move = (BOOM, stack_to_boom)

    # recursive boom at the new_node.state starting at 'stack', this updates the state
    new_node.state = chain_boom(new_node.state, stack_to_boom)

    # update a* values and return
    new_node.h = heuristic(new_node.state)
    new_node.f = new_node.h + new_node.depth

    return new_node

