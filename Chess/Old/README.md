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

### Defensive
The philosophy of the AI is to make something that is as hard to attack as possbile. However, it does not have an aggressive bone in it's body. It will not try to checkmate you or attack you, it's objective is to ensure that you cannot attack it and that any exchange it makes is at least even. I also equipt it with the most defensive opening in chess: the Hippopotamus Defense. It's actually quite hard to beat. I played it against Stockfish 8 and the evaluation reads only slightly in Stockfishes favor until well into the middle game.
