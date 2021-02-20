# ohhi-solver

#### A simple solver for binary sudoku.

## Instructions

You need to have SWI-Prolog installed on your computer.

Open the `swipl` REPL in a terminal and type in `consult('ohhi.pro')` (or whatever the file path to the solver is) to input.

The API for the solver is very simple:

```prolog
solve(N, C, T).
show_board(T).
```

These are the only predicates you need to call.  To create a solution, you need instanced terms in `N` and `C`.  `N` is half the length of the board - or, how many of each color there are in a row (`N` = 2 produces a 4x4 board).  `C` is a list of constraint predicates (see below).  The resulting grid of numbers is found in `T`.  To show the board after, use `show_board(T).`, as it pretty prints the grid with proper formatting.  (If you look in the code, you can see this is already included in `solve()`.)

An example query:

```prolog
?- solve(3, [...], T).
```

## Producing Constraints

Each constraint predicate is of the form

```prolog
c(Color, Square)
```

...where a `Square` is simply `[i|j]`, and `i` and `j` are the row and column of the square in the grid respectively.  `Color` is either 0 or 1 - in `0hh1`, that's red and blue respectively.

Producing constraints by hand is challenging.  To help yourself out, use the script `make_constraints.py`.  You still need to record information about the locked squares at the start of the puzzle, but the script will format that info for you.

A valid input file to the script is a new-line separated list of squares.  One square takes the following form:

```
I,J,Color
```

So, if  your puzzle has a '0' at square (2, 3), you must put in the following:

```
2,3,0
```

Try not to put any spaces or unnecessary characters.

Once you have your file of constrained squares, pass it in to the script on the command line.  For example:

```
python make_constraints.py tests/marbles.txt
```

It will then print out a comma separated list of constraints.  Paste its output in `C` when you make a query as such:

```prolog
?- solve(4, [HERE: c(Color, Square), c(Color, Square), etc.], T).
```

## Statistics

An 8x8 board can be solved in around a second, while a 12x12 board takes a few seconds (around 6-7).  Realistically, the bottleneck for bringing a puzzle from initial state to completion is not producing the solution with the solver - it's typing in the solution by hand!





