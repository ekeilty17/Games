# Chess
I created a working chess player on the terminal. You can play human vs. human as well as human vs. computer.

## EZ-Chess
I made a simple version of chess. Here are the following things that are different about the rules in my chess player from real chess.

* pawns can only move 1 square at a time, even on their first move
* pawns do not promote if they reach the opposite side
* No en passants
* No castling

## AI's

### Random
It does what the name implies, makes a random move

### Brute Force
I implement a naive alpha-beta pruning search tree. In order to evaluate the state of the board I compare the material counts using the standard chess convention (pawn = 1, knight = 3, bishop = 3, rook = 5, queen = 9) and also take some positional parameters into account such as such as "knight on the rim is dim" and bishops being near own pawns. For more information on how my alpha-beta pruning algorithm can be implemented see [alphabeta_pruning](www.githib.com). Running it at depth 2 is instantaneous, but depth 3 takes a few seconds and depth 4 takes a few minutes especially at the beginning. It's pretty good at end game positions though.

### Defensive
The philosophy of the AI is to make something that is as hard to attack as possible. However, it does not have an aggressive bone in it's body. It will not try to checkmate you or attack you, it's objective is to ensure that you cannot attack it and that any exchange it makes is at least even. I also equipt it with the most defensive opening in chess: the Hippopotamus Defense.

It works by using a hard-coded, sophisticated function that gets a list of candidate moves by considering what pieces are being attacked and what pieces are properly defended. When making exchanges it will always attempt to at least make an even exchange. Once it gets a list of candidate moves, it uses the alpha-beta pruning algorithm to determine which candidate moves are the best.

It's actually quite hard to beat. I played it against Stockfish 8 and the evaluation reads only slightly in Stockfishes favor until well into the middle game.
