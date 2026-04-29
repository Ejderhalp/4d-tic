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





plan for video:
Explain 4D tic tac toe the vision (what are the inputs, outputs, and logical components of your algorithm).

Explain a few key sections of your code in detail. These should be critical pieces of your algorithm or things that you found particularly difficult or interesting to implement. If you are working in a group, every group member should explain a key section (we recommend ~1 minute per person).

Highlight the new thing(s) you learned along the way. We are looking to see that you applied at least one concept, tool, or skill beyond what we did in class.

Play the game a few times with some edge cases. Tell them why those edge cases work

If the scope of your project has changed since your FP Status video, discuss those changes and the rationale behind them. Your project needs to have accomplished what you committed to in your last video, or have made course corrections for good reasons. Running out of time is not likely to be a good reason.

Suggest what the next steps would be if you were to keep improving this project.
