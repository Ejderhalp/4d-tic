# 4d-tic
### INSTRUCTIONS ###

In order to play, you must first choose if you want to input a number (0-80) or coordinates (eg. 0 1 2 1)

Then, the player will play their turn. After each of the player's turns, the AI will choose the square that minimizes the distance from
each of the player's previous moves. If there is a tie, the ai will just choose randomly. Note: occupying the same spot but one away in
the 4th dimension is the same as being beside it in the 3rd dimension but the same 4th dimension, since the distance for both would be 1

The game will detect a win when all of a certain player's moves have coordinates that are either 3 of the same or 3 varying by one.

External Support:
- Writing the function to visualise the board
- Finding the move that minimizes the distance to the player's previous moves
