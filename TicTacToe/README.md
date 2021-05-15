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
Competent will always win if there is an obvious win and will always block an obvious attempt by its opponent at winning. Meaning, if there are two in-a-row of its own pieces, then it will move to make three in-a-row and win, or if there are two in-a-row of its opponent's pieces then it will move to block it. However, it has no fore-sight, so it can be easily tricked.

### Brute-Force
Brute force using an alpha-beta pruning algorithm tree in order to search through every possible board state. Once it hits a leaf node, it determines if the board state is a win for X, win for O, or a draw and then using the alpha-beta pruning algorithm back propagates that value back to the root.
