# ohhi-solver

#### A simple solver for binary sudoku.

![ezgif-4-dfe5d7eaeb](https://github.com/rabirabirara/ohhi-solver/assets/59306451/c423f847-c5f5-4fa4-a0eb-77e075e1ba03)

## Instructions

You need to have GNU-Prolog and gplc installed on your computer. (If you want to use SWI-Prolog or Picat, install those too.)

If you want to use the auto-solver script, you also need Python and pip (for the script's dependencies - e.g. OpenCV, numpy, PyAutoGUI).

### Python: automatic solve

Just open the website like in the above video, open the script, then press play. You need GNU-Prolog and a compiler for it.

The script looks for the history icon which appears when play begins.

You can change what theme the solver looks for, but only the first two themes are supported. The others are either redundant or cluttered or not viable.

#### Compiling an executable

GNU-Prolog has a compiler called `gplc`. Compile the gprolog-targeting script like this:

```
gplc gnu-ohhi.pl
```

Simple as that. It should produce an executable. I reccommend passing in the arguments `-o build/<executable-name>`.

The executable takes two arguments on the command line: a number (N/2 for an NxN board) and a string (valid prolog syntax produced by gen_constraints.py).

### Prolog

#### REPL

Open the `gprolog` or `swipl` REPL in a terminal and type in `consult('ohhi.pro')` (or whatever the file path to the solver is) to input.

The (usage) API for the solver is very simple:

```prolog
ohhi(N, C).
```

These are the only predicates you need to call.  To create a solution, you need instanced terms in `N` and `C`.  `N` is half the length of the board - or, how many of each color there are in a row (`N` = 2 produces a 4x4 board).  `C` is a list of constraint predicates (see below).  

An example query:

```prolog
?- ohhi(3, [...]).
```

If you want more control, or to use the solution grid, there are other functions available:

```prolog
solve(N, C, T).
show_board(T).
```

The solution grid is stored in `T` when you use `solve/3`. You can then pretty print it with `show_board/1`.

## Producing Constraints

Each constraint predicate is of the form

```prolog
c(Color, Square)
```

...where a `Square` is simply `[i|j]`, and `i` and `j` are the row and column of the square in the grid respectively.  `Color` is either 0 or 1 - in `0hh1`, that's red and blue respectively.

Producing constraints by hand is challenging.  To help yourself out, use the script `make_constraints.py`.  You still need to record information about the locked squares at the start of the puzzle, but the script will format that info for you.

A valid input file to the script is a new-line separated list of squares, similar to a CSV file.  One square takes the following form:

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

## Using the Picat script

Picat is a multi-paradigm language; you can think of it as Prolog for general purpose programming.  It includes
imperative/functional features and is absolutely excellent as a logic/constraint/planning solver.  You'll notice that
the Picat program is much more concise and expressive.

Picat programs can only be run with the Picat interpreter.  To give a test case to the script, you have to enter
in the board yourself, by editing the `board/1` function.  Install the Picat language system, and then run the
script with `picat picat-ohhi.pi`.  You can do that, or run the Picat REPL and include the script with `cl(picat-ohhi)`.


## Statistics

The `gprolog` implementation should solve a 12x12 board in a dozen milliseconds, while the `swipl` implementation
takes several times as much time - around three seconds for a 12x12 board.

I am unsure as to why this is.  But one thing is for sure - all of the program execution time is sucked up by the one line
mapping `no_3_cont` to the transposeed grid.  I suspect it isn't actually the inferiority of the SWI implementation,
but just a bug.

The Picat solution doesn't have time measurements in the milliseconds, but we can use the GNU `time` utility to time
all the solutions anyway - this makes more sense as `gprolog` can be compiled into an executable, while Picat files cannot.
Picat takes a little less time than `gprolog`, but still takes time in the order of several milliseconds.

Realistically, the bottleneck for bringing a puzzle from initial state to completion is not 
producing the solution with the solver - it's typing in the solution by hand!

## Resources

I wanted to improve the performance of the solver.  In my research I stumbled upon a slew of papers regarding the binary puzzle.  
While I didn't learn anything I didn't already know - the solver's bottlenecks are not in my theoretical implementation of the constraints - I was enthused
to read fancy research papers about the problem.  Probably the most succinct description of the problem is here:

- Putranto Utomo and Ruud Pellikaan. Binary Puzzle as a SAT Problem; accessed February 20, 2021. https://www.win.tue.nl/~ruudp/paper/82.pdf



