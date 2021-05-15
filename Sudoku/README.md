# Sudoku

One of the most famous puzzles in the world and a game that I played a lot when I was younger. I created a program that allows users to play Sudoku as well as an engine that will solve any Sudoku puzzle.

In order to play execute `python play.py`. The file is set to having the engine solve what is considered the hardest Sudoku puzzle ever created by default. If you wish to use my program to play Sudoku yourself (although I don't recommend it, there exists apps with much better UI) then comment-out the function `AI()` and uncomment the function `Sudoku()`.

## The Sudoku Solver

I created 3 different Sudoku solvers. Each can solve a more difficult puzzle than the last. I named them `beginner_AI()`, `intermediate_AI()`, and `expert_AI()`

### The Beginner and Intermediate Sudoku Solvers

Simple Sudoku puzzles can be solved by just implementing the following 2 logical priciples (I'm not sure if these are official names, but this is what I have always called them). The beginner AI implement only the first (because that is usually the first method people figure out), and the intermediate AI implements both. Rather than explain them in words I will just show the logical deduction.

* **Unique Candidate**

This principle uses the fact that in Sudoku there are only exists one instance of each number in every row, column, and square.

|     |     |     |     |     |     |     |     |     |     |     |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  0  |  0  |**4**|     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |**4**|  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|**5**|  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |**4**|     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |

The 4's take away all but cell in the bottom left sqaure. Therefore we can conclude the top left cell of the bottom right square is a 4.

|     |     |     |     |     |     |     |     |     |     |     |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  0  |  0  |**4**|     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |**4**|  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|**5**|  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|**4**|  0  |  0  |     |  0  |  0  |**4**|     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |

* **Soul Candidate**

This principle uses the fact that each row, column, and square contrains each of the numbers 1,2,3,4,5,6,7,8,9. This may sound like it is equivalent to the previous principle, but it's not.

|     |     |     |     |     |     |     |     |     |     |     |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  0  |  0  |  0  |     |  0  |  0  |**1**|     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |**6**|     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |**4**|  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |**8**|  0  |     |  0  |  0  |  0  |
|**2**|  0  |**9**|     |  0  |  0  |  0  |     |  0  |  0  |**7**|
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |**3**|     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |

Another way of thinking of this is we are eliminated candidate numbers. Looking at the bottom right cell of the middle square. From it's row we can deduce it can either be a 1, 3, 4, 5, 6, 8, or 9. From its column we can reduce that candidate list to 4, 5, and 8. From its square we can deduce that the cell has to be a 5. This is quite tricky for humans to spot, but it's very simple to code and very powerful.

|     |     |     |     |     |     |     |     |     |     |     |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  0  |  0  |  0  |     |  0  |  0  |**1**|     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |**6**|     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |**4**|  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |**8**|  0  |     |  0  |  0  |  0  |
|**2**|  0  |**9**|     |  0  |  0  |**5**|     |  0  |  0  |**7**|
|     |     |     |     |     |     |     |     |     |     |     |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |**3**|     |  0  |  0  |  0  |
|  0  |  0  |  0  |     |  0  |  0  |  0  |     |  0  |  0  |  0  |
|     |     |     |     |     |     |     |     |     |     |     |


### The Expert Sudoku Solver

With the exception of the principle of the "Naked Pair" (which is relatively simple, but would be a nightmare to code) the advanced techniques of Sudoku get really complex. They mostly revolve around getting a list of candidate moves for each cell and then using complex logical deductions in order to eliminate candidate moves. Instead of trying to code those, I took a different approach.

For lack of a better term, the advanced AI solves the puzzles by contradiction. It implements the intermediate AI until the intermediate AI can't make any more moves. Then it finds cell with the least number of candidate moves (there usually exists one with just 2) and it guesses. We know that one of the candidate moves must be correct. If the guess leads to a contradiction (i.e. a cell that is empty but has zero candidate moves) then that must have been the wrong guess and it tries the next candidate move. If it completes the puzzle with no constradictions, then we found the correct solution.

Formally, this is called a Depth-First Search, but this is a special case because of 2 facts:

1. The solution to Sudoku is unique.
2. We know one of the numbers in out set of candidate solutions must be correct.