
### WELCOME TO 4D TIC TAC TOE ###
import random
import numpy as np
from itertools import combinations
import plotly.graph_objects as go


xs = []
os = []
past_choices =[]
def get_numerical_input():
    while True:
        choice = int(input("What move do you want to make? "))
        if choice in past_choices:
            print("No doubling up guesses!")
        else:
            break
    past_choices.append(choice)
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
                for x in range(3):# checks every possible coordinate and sees if it's occupied
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if available:
        choice = random.choice(available) #chooses a random coordinate
        os.append(choice)

def check_win(player_coords):
    if len(player_coords) < 3:
        return False


    for combo in combinations(player_coords, 3):
        win = True
        for dim in range(4): # Check x, y, z, w
            coords_in_dim = sorted([p[dim] for p in combo])
            # dimension valid if all points in same line or they cover all three lines
            if not (coords_in_dim[0] == coords_in_dim[1] == coords_in_dim[2] or
                    coords_in_dim == [0, 1, 2]):
                win = False
                break
        if win:
            return True
    return False


# Example usage (call this in your game loop):
# visualize_board(xs, os)
def main():
    print("There are 81 possible squares that you can move. Please input your guesses as an integer from 0-80")
    while True:

        update_xs(get_numerical_input())
        if check_win(xs):
            print("X WON!")
            #visualize_board_stacked(xs,os)
            break
        add_computer(xs, os)
        #print(xs, os) #DEBUG
        if check_win(os):
            print("O WON!")
            #visualize_board_stacked(xs,os)
            break
        #visualize_board_stacked(xs,os)

if __name__ == "__main__":
    main()




