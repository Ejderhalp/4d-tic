### 4dtic/simulation_lib.py

past_choices =[]

def get_numerical_input(player = "X"):
    while True:
        choice = int(input(f"Player {player} what move do you want to make? (0-80)"))
        if choice in past_choices:
            print("No doubling up guesses!")
        else:
            break
    past_choices.append(choice)
    return choice

def get_coordinate_input(player = "X"):
    while True:
        choice = input(f"Player {player} what move do you want to make? (seperated by spaces)").split() #splits users input into a list
        for i in range(4):
            choice[i] = int(choice[i])
        if choice in past_choices:
            print("No doubling up guesses!")
        else:
            break
    past_choices.append(choice)
    return choice
