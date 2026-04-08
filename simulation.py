
### WELCOME TO 4D TIC TAC TOE ###
import random
import numpy as np
from itertools import combinations
# Current state of the board is recorded as a 4d array
# From outside -> in the order of coordinates in the array
# is w, z, y, x

#print(state)

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
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if available:
        choice = random.choice(available)
        os.append(choice)

def check_win(player_coords):
    if len(player_coords) < 3:
        return False


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

import plotly.graph_objects as go

def visualize_board(xs, os):
    fig = go.Figure()

    def get_plot_coords(coords_list):
        # We project 4D [w, z, y, x] into 3D [X_plot, Y_plot, Z_plot]
        # We use 'w' to offset the X-axis so the cubes sit side-by-side
        x_plot = [c[3] + (c[0] * 4) for c in coords_list]
        y_plot = [c[2] for c in coords_list]
        z_plot = [c[1] for c in coords_list]
        return x_plot, y_plot, z_plot

    # Add X moves
    if xs:
        x_x, x_y, x_z = get_plot_coords(xs)
        fig.add_trace(go.Scatter3d(
            x=x_x, y=x_y, z=x_z,
            mode='markers+text',
            name='Player X',
            marker=dict(size=10, color='red', symbol='x'),
            text=[f"X-{i}" for i in range(len(xs))]
        ))

    # Add O moves
    if os:
        o_x, o_y, o_z = get_plot_coords(os)
        fig.add_trace(go.Scatter3d(
            x=o_x, y=o_y, z=o_z,
            mode='markers',
            name='Player O',
            marker=dict(size=10, color='blue', symbol='circle'),
        ))

    # Add a "grid" of empty slots to help visualization
    all_slots = []
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    all_slots.append([w, z, y, x])

    s_x, s_y, s_z = get_plot_coords(all_slots)
    fig.add_trace(go.Scatter3d(
        x=s_x, y=s_y, z=s_z,
        mode='markers',
        marker=dict(size=2, color='lightgray'),
        showlegend=False,
        hoverinfo='none'
    ))

    fig.update_layout(
        title="4D Tic-Tac-Toe (3D Projection)",
        scene=dict(
            xaxis_title='X (shifted by W)',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        )
    )

    fig.show()

# Example usage (call this in your game loop):
# visualize_board(xs, os)
def main():
    print("There are 81 possible squares that you can move. Please input your guesses as an integer from 0-80")
    while True:
        visualize_board(xs,os)
        update_xs(get_numerical_input())
        if check_win(xs):
            print("X WON!")
            break
        add_computer(xs, os)
        #print(xs, os) #DEBUG
        if check_win(os):
            print("O WON!")
            break

if __name__ == "__main__":
    main()




