### SETUP ###

Libraries needed:
numpy, itertools, plotly, math, dash

Ideally play in the vs code web based ide as that's how we tested the files

simulation_backup.py is the version without the dash library
simulation.py is the version augmented to include the dash library

### README ###

Welcome to 4d tic tac toe. I (Alp) came up with the idea for this game after hearing my friend mention that he had devised
a way to play 3d tic tac toe on a sheet of paper during a random physics class in high school, by using circles and squares
of different sizes that fit within each other. I figured it would be the same concept to extend that to 4d but never had the
chance to code it until now. Valentina very kindly let our group project be based on this idea, and we had lots of fun coding it

### INSTRUCTIONS ###

In order to play, you must first choose if you want to play one player or two players.
Next, you will put your move as 4 numbers between 0 and 2 inclusive (eg. 1021)

### 1 PLAYER MODE ###

After each of the player's turns, the AI will:
- First check if it can win
- Then check if it can prevent a win
- Then play a move that minimizes the distance to the player's moves

### 2 PLAYER MODE ###

In 2 player mode, the game continues until one player wins

### WINNING ###

The game will detect a win when all of a certain player's moves have coordinates that are either 3 of the same or 3 that change by one.

### EXTERNAL SUPPORT USED ###

- GenAI assistance was used in writing the function that finds the best move for the AI.
- GenAI assistance was also used in writing the visualise board function, alongside the documentation, to help us understand a new library (plotly)
- GenAI assistance for Dash - combining the input and visualization




