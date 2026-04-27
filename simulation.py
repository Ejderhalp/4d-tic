### WELCOME TO 4D TIC TAC TOE ###

import numpy as np
from itertools import combinations
import plotly.graph_objects as go
import math


xs = [] #player moves
os = [] #computer/other players moves
past_choices =[] #past moves

def get_coordinate_input(player = "X"):
    while True:
        choice = list(input(f"Player {player} what move do you want to make? (input 4 numbers)").strip()) #splits users input into a list
        for i in range(4):
            choice[i] = int(choice[i]) #convert to integer
        if choice in past_choices:
            print("No doubling up guesses!")
        else:
            break
    past_choices.append(choice)
    return choice

def add_computer_intelligently(xs, os):

    #making a list of all empty positions
    available = []
    for w in range(3):
        for z in range(3):
            for y in range(3):
                for x in range(3):
                    if [w, z, y, x] not in xs and [w, z, y, x] not in os:
                        available.append([w, z, y, x])

    # firstly check for a win from the moves that the AI has available right now

    for spot in available:
        test_os = os + [spot]
        if check_win(test_os):
            final_move(spot, os)
            print(f"AI win with {spot}!")
            return

    # if AI can't win in one move, prevent a player win
    for spot in available:
        test_xs = xs + [spot]
        if check_win(test_xs):
            final_move(spot, os)
            print(f"AI Blocked Player at {spot}!")
            return

    # if neither of those things happen, then find the move closest to the player's moves on average
    best_move = None
    min_total_distance = float('inf')

    for spot in available: # checks all available spaces
        current_total_dist = 0
        for player_move in xs: # for each move that's been played,
            dist_sq = sum((spot[i] - player_move[i])**2 for i in range(4)) # find the distance of the possible move from the player's move
            current_total_dist += math.sqrt(dist_sq) #squareroots it to find distance (optional since sqrt is strictly increasing as a function)

        if current_total_dist < min_total_distance:
            min_total_distance = current_total_dist
            best_move = spot #finds the best move

    final_move(best_move, os)

def final_move(choice, os_list): #commits the AI's move into the list of os
    os_list.append(choice)
    past_choices.append(choice)

def check_win(player_coords):
    if len(player_coords) < 3: #no win if less than three moves
        return False


    for combo in combinations(player_coords, 3):
        win = True
        for dim in range(4): # Check x, y, z, w
            coords_in_dim = [p[dim] for p in combo]
            # dimension valid if all points in same line or they cover all three lines
            if not (coords_in_dim[0] == coords_in_dim[1] == coords_in_dim[2] or coords_in_dim == [0,1,2] or coords_in_dim == [2,1,0]):
                win = False
                break
        if win:
            return True
    return False

def visualize_board_stacked(xs, os): # ai assistance used with this function

    fig = go.Figure()

    SCALE = {0: 0.4, 1: 0.25, 2: 0.12} # setting size values for the 4d slices
    OPACITY = {0: 0.4, 1: 0.7, 2: 1.0} # setting opacity for each 4d value

    def draw_cube(x, y, z, size, color, opacity, name):

        d = size
        fig.add_trace(go.Mesh3d(
            x=[x-d, x-d, x+d, x+d, x-d, x-d, x+d, x+d], #defining 8 corners of the cube
            y=[y-d, y+d, y+d, y-d, y-d, y+d, y+d, y-d],
            z=[z-d, z-d, z-d, z-d, z+d, z+d, z+d, z+d],
            i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2], # "instructions" for which vertices to connect
            j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
            k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
            color=color, opacity=opacity, name=name,
            flatshading=True, showlegend=False
        ))

    def draw_sphere(x, y, z, size, color, opacity, name):
        nb_points = 20
        phi = np.linspace(0, 2*np.pi, nb_points)
        theta = np.linspace(0, np.pi, nb_points)
        phi, theta = np.meshgrid(phi, theta)

        X = x + size * np.sin(theta) * np.cos(phi)
        Y = y + size * np.sin(theta) * np.sin(phi)
        Z = z + size * np.cos(theta)

        fig.add_trace(go.Surface(
            x=X, y=Y, z=Z,
            colorscale=[[0, color], [1, color]],
            showscale=False,
            opacity=opacity,
            name=name,
            hoverinfo='name'
        ))

    #draw cubes
    for move in xs:
        w, z, y, x_coord = move
        draw_cube(x_coord, y, z, SCALE[w], 'red', OPACITY[w], f"X (W={w})")

    #draw spheres
    for move in os:
        w, z, y, x_coord = move
        draw_sphere(x_coord, y, z, SCALE[w], 'blue', OPACITY[w], f"O (W={w})")

    #draw the grid
    ghost = [[z, y, x] for z in range(3) for y in range(3) for x in range(3)] #finds every possible coordinate
    fig.add_trace(go.Scatter3d(
        x=[c[2] for c in ghost], y=[c[1] for c in ghost], z=[c[0] for c in ghost],
        mode='markers',
        marker=dict(size=2, color='rgba(150,150,150,0.2)'),
        showlegend=False, hoverinfo='none'
    ))

    fig.update_layout(
        title="4D tic-tac-toe, size represents 4th dimension (coords are [w,z,y,x])",
        scene=dict(
            xaxis=dict(title='X', range=[-0.5, 2.5]),
            yaxis=dict(title='Y', range=[-0.5, 2.5]),
            zaxis=dict(title='Z', range=[-0.5, 2.5]),
            aspectmode='cube',

            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
        )
    )
    fig.show()

def main():
    print("Welcome to 4d Tic Tac Toe!")

    two_player = input("1 or 2 player? Enter 2 for 2p").strip() =="2"

    while True:

        # order of events in this loop:
        # first get player's input and check if they won
        # if no win, get second move (computer/ p2) and check win
        # if no win, repeat until a win occurs
        # only visualise the board once both players have played or someone wins

        print("\nPlayer X's turn")
        xs.append(get_coordinate_input(player = "X"))

        if check_win(xs):
            print("X WON!")
            visualize_board_stacked(xs,os)
            break

        if two_player:
            print("\nPlayer O's turn")
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
