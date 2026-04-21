### 4dtic/simulation_lib.py

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

def get_coordinate_input():
    while True:
        choice = input("What move do you want to make? (separated by spaces) ").split() #splits users input into a list
        for i in range(4):
            choice[i] = int(choice[i])
        if choice in past_choices:
            print("No doubling up guesses!")
        else:
            break
    past_choices.append(choice)
    return choice
