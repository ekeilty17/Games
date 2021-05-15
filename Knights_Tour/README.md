# Knight's Tour

The knight's tour is a traversal with the knight of an mxn board such that the knight visits every square exactly once. When people say "the knight's tour" they are often referring to the special case of a chess board (8x8), but the problem can easily be generalized to a board of abritrary size. I have created a program that allows users to try to solve the knight's tour puzzle as well as an engine the can solve the knights tour of any sized board in a matter of seconds. 

In order to play execute `python play.py`. The file is set to having the computer solve the knight's tour by default. If you wish to use my program to solve the knight's tour yourself (although I don't recommend it, there exists apps with much better UI) then comment-out the function `Knights_Tour()` and uncomment the function `Human()`.

## Knight's Tour Solver

The code for the solver can be found in `tour.py`. It implements a **Depth-First Search** with the following breaking conditions:

1. If there exists an unvisited square with no possible knight moves
2. If there exsts 2 or more squares with only 1 possible knight move

Moreover, I implemented **Warnsdorf's rule**, which is a heuristic that says to move the knight such that it always proceeds to the square with the fewest onward moves. This heuristic increased the speed of the solver dramatically.

## Closed Knight's Tour

There is also something called the "closed knight's tour", which is a knight's tour such that the starting square is a knight's move away from the ending square. In order words, it's a closed traversal of the board with the knight. My engine can also solve closed knight's tours. It works almost identically to the open knight's tour solver, but with one extra break case:

* If there exists no possible knight moves to the starting square

## Existence

### Background of the Theory

A knight's tour is a special case of a more general problem in graph theory called the Hamiltonian path problem. Likewise, the closed knight's tour is a special case of the Hamiltonian cycle problem. However, unlike the general Hamiltonian problem, the knight's tour can be solved in linear time. Why?

In the specific case of a chess board (8x8) there are 4x10^51 possibly knight traversals. BUT there are 26,534,728,821,064 closed tours (including reversals, reflections, and rotations). And we don't even know how many open tours there are. The reason a random search with some clever heuristics is so fast is because the knight's tour is not unique. There are many, many ways to solve it. The code also scales because as the size of the board increases, so does the number of correct solutions.

### Conditions

**Open Tour:** An open tour exists on any rectangular board where the smallest dimension is greater than or equal to 5.

**Closed Tour:** A closed tour exists on an mxn board unless 1 or more of the following conditions are met (assume m ≤ n):

1. m and n are both odd
2. m = 1, 2, or 4
3. m = 3 and n = 4, 6, or 8

## Future

There is a method for solving the knight's tour called "Divide and conquer algorithms", which can solve the knight's tour in linear time. I may try to implement such an algorithm in the future.

The knight's tour problem also lends itself to a Neural Network Solution. I am very interested in Machine Learning, so I will very likely implement such a solution in the future.
