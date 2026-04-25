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

def update_os(choice): #same as above but for player O
    cube_number = choice//27
    slice_number = (choice%27)//9
    row_number = (choice%9)//3
    line_number = choice%3
    os.append([cube_number, slice_number, row_number, line_number])


'''
def add_computer_randomly(xs, os): #simple AI
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
'''
def add_computer_intelligently(xs, os): #smart AI
    available = []
    # Identify all empty spots
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    if not available:
        return #no moves left

    best_move = None
    min_total_distance = float('inf') #start w infinity

    for spot in available: # for empty spots
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

def visualize_board_stacked(xs, os):
    fig = go.Figure()


    SCALE = {0: 0.4, 1: 0.25, 2: 0.12}
    OPACITY = {0: 0.4, 1: 0.7, 2: 1.0}

    def draw_cube(x, y, z, size, color, opacity, name):

        d = size
        fig.add_trace(go.Mesh3d(
            x=[x-d, x-d, x+d, x+d, x-d, x-d, x+d, x+d],
            y=[y-d, y+d, y+d, y-d, y-d, y+d, y+d, y-d],
            z=[z-d, z-d, z-d, z-d, z+d, z+d, z+d, z+d],
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color=color, opacity=opacity, name=name,
            flatshading=True, showlegend=False
        ))

    def draw_sphere(x, y, z, size, color, opacity, name):

        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers',
            marker=dict(
                size=size * 80,
                color=color,
                opacity=opacity,
                symbol='circle'
            ),
            name=name, showlegend=False
        ))

    # Draw moves
    for move in xs: # Player X = Cubes
        w, z, y, x_coord = move
        draw_cube(x_coord, y, z, SCALE[w], 'red', OPACITY[w], f"X (W={w})")

    for move in os: # Player O = Spheres
        w, z, y, x_coord = move
        draw_sphere(x_coord, y, z, SCALE[w], 'blue', OPACITY[w], f"O (W={w})")

    # Draw the Background Ghost Grid
    ghost = [[z, y, x] for z in range(3) for y in range(3) for x in range(3)]
    fig.add_trace(go.Scatter3d(
        x=[c[2] for c in ghost], y=[c[1] for c in ghost], z=[c[0] for c in ghost],
        mode='markers',
        marker=dict(size=2, color='rgba(150,150,150,0.2)'),
        showlegend=False, hoverinfo='none'
    ))

    fig.update_layout(
        title="4D Tic-Tac-Toe: 3D Rendered (W=Size/Opacity)",
        scene=dict(
            xaxis=dict(title='X', range=[-0.5, 2.5]),
            yaxis=dict(title='Y', range=[-0.5, 2.5]),
            zaxis=dict(title='Z', range=[-0.5, 2.5]),
            aspectmode='cube',
            # Adding lighting effects for the 3D meshes
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )
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
    input_type = input("Input as numbers or coordinates? Enter N for Numbers or just press enter for Coordinates: ")
    numerical = input_type.upper() == "N"

    while True:
        #player X turn
        print("\nPlayer X's turn")
        if numerical:
            update_xs(get_numerical_input(player = "X"))
        else:
            xs.append(get_coordinate_input(player = "X"))

        if check_win(xs):
            print("X WON!")
            visualize_board_stacked(xs,os)
            break

        if two_player:
            print("\nPlayer O's turn")
            if numerical:
                update_os(get_numerical_input(player = "O"))
            else:
                os.append(get_coordinate_input(player = "O"))
        else:
            print("\nComputer thinking...")
            add_computer_intelligently(xs,os)


        if check_win(os):
            if two_player:
                print("Player O won!")
            else:
                print("The computer won!")
            visualize_board_stacked(xs,os)
            break

        visualize_board_stacked(xs,os)

if __name__ == "__main__":
    main()




