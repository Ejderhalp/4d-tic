
### WELCOME TO 4D TIC TAC TOE ###
import random
import numpy as np
# Current state of the board is recorded as a 4d array
# From outside -> in the order of coordinates in the array
# is w, z, y, x

state = [[[[[],[],[]],[[],[],[]],[[],[],[]]], # first slice of first cube
          [[[],[],[]],[[],[],[]],[[],[],[]]],
          [[[],[],[]],[[],[],[]],[[],[],[]]]], # first cube

          [[[[],[],[]],[[],[],[]],[[],[],[]]],
           [[[],[],[]],[[],[],[]],[[],[],[]]],
           [[[],[],[]],[[],[],[]],[[],[],[]]]], # second cube

           [[[[],[],[]],[[],[],[]],[[],[],[]]],
            [[[],[],[]],[[],[],[]],[[],[],[]]],
            [[[],[],[]],[[],[],[]],[[],[],[]]]]] # third cube

#state = [[[[[0] for i in range(3)] for j in range(3)] for k in range(3)] for l in range(3)]



#print(state)

xs = []
os = []

def get_numerical_input():
    choice = int(input("What move do you want to make? There are 81 possible squares that you can move, so answer with a number from 0-80"))
    return choice

def update_xs(choice):
    cube_number = choice//27 #outputs 0, 1 or 2 (the w coordinate)
    slice_number = (choice%27)//9 #outputs the slice within the cube (the z coordinate)
    row_number = (choice%9)//3 # outputs the row within the slice (the y coordinate)
    line_number = choice%3 # outputs where on the line it is
    xs.append([cube_number, slice_number, row_number, line_number])


def add_computer(xs, os):
    available = []
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if available:
        choice = random.choice(available)
        os.append(choice)

def check_win(player_coords):
    if len(player_coords) < 3:
        return False

    # In a 3x3x3x3 game, we check every combination of 3 points
    # (Note: For performance in larger games, use a different approach)
    from itertools import combinations
    for combo in combinations(player_coords, 3):
        win = True
        for dim in range(4): # Check x, y, z, w
            coords_in_dim = sorted([p[dim] for p in combo])
            # A dimension is valid if all coords are same OR are [0, 1, 2]
            if not (coords_in_dim[0] == coords_in_dim[1] == coords_in_dim[2] or
                    coords_in_dim == [0, 1, 2]):
                win = False
                break
        if win:
            return True
    return False

while True:
    update_xs(get_numerical_input())
    add_computer(os)
    print(xs)
    #print(xs, os)
    x_won = check_win(xs)
    o_won = check_win(os)
    game_over = x_won and o_won
    if game_over:
        break

if x_won:
    print("X WON")
else:
    print("O WON")

