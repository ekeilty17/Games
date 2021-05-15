# Tic Tac Toe
I have created a terminal tic tac toe game. This can be played human vs. human and it can be played human vs. computer as I have programmed a few AI's

## How to Play
simply run `python play.py`

## Other Settings
By default you will play as X's against the Brute-Force AI. I have commented out every other permutation of the game settings. You may play those simply by uncommenting them.


## AI's
### Random
Random does what the name implies. Outputs a random legal move.

### Competent
Competent will always win if there is an obvious win and will always block an obvious attempt by its oppenent at winning. Meaning, if there are two in-a-row of its own pieces, then it will move to make three in-a-row and win, or if there are two in-a-row of its opponent's pieces then it will move to block it. However, it has no fore-sight, so it can be easily tricked.

### Brute-Force
Brute force using a general tree in order to search through every possible board state and uses a heuristic function to determine which move is the best to play. As of right now my heuristic function is very simple. It starts at the end of the tree (since tic tac toe is small you can easily search through all possible states) analyzes that end-state of the board and then uses max-min back propogation in order to give the root it's final heuristic.

### Something to Note
If you play against the brute force AI you may think it's broken. It actually does works as designed. What you will notice is that the brute force AI's first move is always in the top left corner. This is because tic tac toe is objectively a draw with best play. You can always draw if you play in a corner. So all corner squares (and the center square if available) are coming back with a hueristic of 0 and the max() and min() functions just return the first instance, which is the index 0, i.e. the top left corner. Since by the nature of a max-min back propogation, the AI does not try to trick you and therefore if you play competently you should never lose.

