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
    # return string of square contents from coordinates (x, y)
    # e.g. if a square at (1, 3) is occupied by 3 white pieces, get_square_data(data, 1, 3) returns '3w'
    # return '' if nothing in the given coordinates
    for colour in data:
        for stack in data[colour]:
            if (stack[1], stack[2]) == (x, y):
                # found a stack with those coordinates, return number in stack and the first letter of the colour
                return str(stack[0]) + colour[0]
    # nothing found
    return ''



def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # TODO: find and print winning action sequence
    print_utils.print_board(make_board_dict(data))
    init_state = ai.State()
    current_node = ai.Node()


    while ai.get_next_move()

if __name__ == '__main__':
    main()
