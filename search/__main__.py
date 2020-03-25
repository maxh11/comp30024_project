import sys
import json
import print_utils
import ai

BOARD_SIZE = 8
EMPTY_CELL = ''
WHITE_PIECE = 'w'
BLACK_PIECE = 'b'


def make_board_dict(data):
    # make empty board
    board_dict = {}
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            board_dict[(x, y)] = get_square_data(data, x, y)
    return board_dict


def get_square_data(data, x, y):
    # return string of square contents (e.g. '4b') from coordinates x, y
    # e.g. if a square at (1, 3) is occupied by 3 white pieces, get_square_data(data, 1, 3) returns '3w'
    # return '' if nothing in the given coordinates
    for colour in data:
        for stack in data[colour]:
            if (stack[1], stack[2]) == (x, y):
                # found a stack with those coordinates, return number in stack and the first letter of the colour
                return str(stack[0]) + colour[0]
    # nothing found
    return ''


def make_state_dict(data, colour):
    # input is json data and a colour 'w' or 'b', for white or black
    # return a dict of stack location coordinates as a key with n_pieces as the value
    # a return example is: {(3, 2): 1, (0, 1): 5, (0, 2): 6}
    stacks = {}
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            square = get_square_data(data, x, y)
            if len(square) > 0:  # not an empty square
                if colour in square:
                    # just add the number of pieces in the stack as value
                    stacks[(x, y)] = int(square[:-1])
    return stacks


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print_utils.print_board(make_board_dict(data))

    # make the initial state and the initial node
    init_state = ai.State(make_state_dict(data, WHITE_PIECE), make_state_dict(data, BLACK_PIECE))
    current_node = ai.Node(init_state)

    # run ai and start generating winning moves
    moves_made = []  # keep track of the moves we have made
    current_node = ai.get_next_move(current_node)
    while current_node is not None:
        moves_made.append(current_node.move_made)
        current_node = ai.get_next_move(current_node)

    # print the moves made
    print(moves_made)

if __name__ == '__main__':
    main()
