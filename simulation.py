### 4dtic/simulation.py


### WELCOME TO 4D TIC TAC TOE ###
import random
import numpy as np
from itertools import combinations
import plotly.graph_objects as go
from simulation_lib import get_numerical_input, get_coordinate_input
import math


xs = [] #player moves
os = [] #computer/other players moves
past_choices =[] #past moves



def update_xs(choice):
    cube_number = choice//27 #outputs 0, 1 or 2 (the w coordinate)
    slice_number = (choice%27)//9 #outputs the slice within the cube (the z coordinate)
    row_number = (choice%9)//3 # outputs the row within the slice (the y coordinate)
    line_number = choice%3 # outputs where on the line it is
    xs.append([cube_number, slice_number, row_number, line_number])

def update_os(choice):
    cube_number = choice//27
    slice_number = (choice%27)//9
    row_number = (choice%9)//3
    line_number = choice%3
    os.append([cube_number, slice_number, row_number, line_number])



def add_computer_randomly(xs, os):
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

def add_computer_intelligently(xs, os):
    available = []
    # Identify all empty spots
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if not available:
        return

    best_move = None
    min_total_distance = float('inf')

    for spot in available:
        current_total_dist = 0

        # Calculate sum of Euclidean distances to all human moves
        for player_move in xs:
            # Distance formula in 4D: sqrt((w2-w1)^2 + (z2-z1)^2 + (y2-y1)^2 + (x2-x1)^2)
            dist_sq = sum((spot[i] - player_move[i])**2 for i in range(4))
            current_total_dist += math.sqrt(dist_sq)

        #update best move
        if current_total_dist < min_total_distance:
            min_total_distance = current_total_dist
            best_move = spot

        elif current_total_dist == min_total_distance: #ties
            if random.random() > 0.5: #random 50/50 chance
                best_move = spot

    # Finalize the move
    choice = best_move
    os.append(choice)

    choice_int = (choice[0] * 27) + (choice[1] * 9) + (choice[2] * 3) + choice[3] #converting back to single num
    past_choices.append(choice_int)


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


def visualize_board_stacked(xs, os): #ai assistance was used with this function
    fig = go.Figure()


    size_map = {0: 30, 1: 20, 2: 10}
    opacity_map = {0: 0.6, 1: 0.8, 2: 1.0}

    def add_player_trace(coords, player_name, color, symbol):
        # We need three separate traces per player (one for each W level)
        for w_val in [0, 1, 2]:
            # Filter moves for this specific W value
            filtered_w = [c for c in coords if c[0] == w_val]

            if not filtered_w:
                continue

            # Project coordinates (No W offset here; they stack directly!)
            # Project [w, z, y, x] -> (x_plot, y_plot, z_plot)
            x_plot = [c[3] for c in filtered_w]
            y_plot = [c[2] for c in filtered_w]
            z_plot = [c[1] for c in filtered_w]

            fig.add_trace(go.Scatter3d(
                x=x_plot, y=y_plot, z=z_plot,
                mode='markers',
                # Important: Include W in the legend name
                name=f"{player_name} (W={w_val})",
                marker=dict(
                    size=size_map[w_val],
                    color=color,
                    symbol=symbol,
                    opacity=opacity_map[w_val],
                    # Adding an outline helps define the nested shapes
                    line=dict(width=1, color='white' if player_name=='X' else 'black')
                ),
                # Group legends logically
                legendgroup=player_name
            ))

    # --- 2. ADD MOVES FOR BOTH PLAYERS ---
    if xs:
        # Use simple color coding for visibility
        add_player_trace(xs, 'Player X', 'red', 'square')

    if os:
        add_player_trace(os, 'Player O', 'blue', 'circle')

    # --- 3. ADD THE GHOST GRID (W=0) FOR REFERENCE ---
    # Only need W=0 reference slots for stacking
    ghost_slots = []
    for z in range(3):
        for y in range(3):
            for x in range(3):
                ghost_slots.append([0, z, y, x]) # w fixed at 0

    g_x = [c[3] for c in ghost_slots]
    g_y = [c[2] for c in ghost_slots]
    g_z = [c[1] for c in ghost_slots]

    fig.add_trace(go.Scatter3d(
        x=g_x, y=g_y, z=g_z,
        mode='markers',
        marker=dict(size=4, color='rgba(200, 200, 200, 0.3)'), # Very faint
        showlegend=False,
        hoverinfo='none'
    ))

    # --- 4. LAYOUT AND TITLE ---
    fig.update_layout(
        title="4D Tic-Tac-Toe (W represented by Size/Opacity)",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            xaxis=dict(nticks=3, range=[-0.5, 2.5]),
            yaxis=dict(nticks=3, range=[-0.5, 2.5]),
            zaxis=dict(nticks=3, range=[-0.5, 2.5]),
            aspectmode='cube' # Keep the visualization perfectly square
        ),
        # Stack the legend so W traces are together
        legend=dict(traceorder="grouped")
    )

    fig.show()




def main():
    print("Welcome to 4d Tic Tac Toe. There are 81 possible squares that you can move.")

    while True:
        mode = input("1 or 2 player? Enter 1 for 1p and 2 for 2p").strip()
        if mode in ["1" , "2"]:
            two_player = (mode == "2")
            break
        print("Please enter 1 or 2")

    #choose input type
    input_type = input("Input as numbers or coordinates? Enter N for numbers or just press enter for Coordinates")

    numerical = False
    if input_type.upper() == "N":
        numerical = True

    while True:


        if numerical:
            update_xs(get_numerical_input())
        else:
            xs.append(get_coordinate_input())


        if check_win(xs):
            print("X WON!")
            visualize_board_stacked(xs,os)
            break
        #add_computer_randomly(xs, os)
        add_computer_intelligently(xs, os)
        #print(xs, os) #DEBUG
        if check_win(os):
            print("O WON!")
            visualize_board_stacked(xs,os)
            break
        visualize_board_stacked(xs,os)

if __name__ == "__main__":
    main()




