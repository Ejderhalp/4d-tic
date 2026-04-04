
### WELCOME TO 4D TIC TAC TOE ###

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

state = [[[[[0] for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
print(state)

def get_numerical_input():
    choice = int(input("What move do you want to make? There are 81 possible squares that you can move, so answer with a number from 0-80"))
    return choice

def update_state(state, choice):
    cube_number = choice//27 #outputs 0, 1 or 2 (the w coordinate)
    slice_number = (choice%27)//9 #outputs the slice within the cube (the z coordinate)
    row_number = (choice%9)//3 # outputs the row within the slice (the y coordinate)
    line_number = choice%3 # outputs where on the line it is

    coord = []



