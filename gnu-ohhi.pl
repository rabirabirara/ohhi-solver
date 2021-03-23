

fliplength(N, T) :- length(T, N).

foldl(_, [], [], Result, Result).
foldl(Goal, [H1|T1], [H2|T2], Init, Result) :-
	call(Goal, H1, H2, Init, InitPrime),
	foldl(Goal, T1, T2, InitPrime, Result).
transpose([], []).
transpose([L|Ls], Ts) :-
    foldl(transpose_helper, L, Ts, [L|Ls], _).
transpose_helper(_, HeadsList, Matrix, TailsList) :-
	maplist(heads_tails, Matrix, HeadsList, TailsList).
heads_tails([L|Ls], L, Ls).

%% Binairo/Takuzu/0hh1/whatever.


% No 3 contiguous squares of same color.
no_3_cont([]) :- !.
no_3_cont([_]) :- !.
no_3_cont([_, _]) :- !.
no_3_cont([A, B, C | T]) :-
    (A #\/ B #\/ C) #/\ (#\A #\/ #\B #\/ #\C),
    no_3_cont([B, C | T]).
% Don't use cut fail there. Fails the ENTIRE thing.


% No two rows/columns are same.
list_eq([], []).
list_eq([X|Xs], [Y|Ys]) :- X #= Y, list_eq(Xs, Ys).

list_member(Xs, [Hs|Ts]) :- list_eq(Xs, Hs) ; list_member(Xs, Ts).

% no_dup_lists([]).
% no_dup_lists([Xs|Xss]) :- not(list_member(Xs, Xss)), no_dup_lists(Xss).

% A little faster.  Since we're not using them on CLPB variables anyway.
no_dups_labeled([]).
no_dups_labeled([Xs|Xss]) :-
    list_member(Xs, Xss), !, fail;
    no_dups_labeled(Xss).


% Exactly N0 of each color in a row/column.
n0_many(N0, L) :- fd_cardinality(L, N0).


% Board access.
access(Grid, [I|J], Color) :-
    nth(I, Grid, RowI),
    nth(J, RowI, Color).

% Fixed board parts are the only variable constraint.
cs(T, c(Color, Square)) :- access(T, Square, Color).


solve(N0, C, T) :-
    N is N0 * 2,
    length(T, N),
    maplist(fliplength(N), T),
    maplist(fd_domain_bool, T),
    maplist(cs(T), C),
    maplist(no_3_cont, T),
    maplist(n0_many(N0), T),
    transpose(T, TT),
    maplist(n0_many(N0), TT),
    maplist(no_3_cont, TT), 
    maplist(fd_labeling, T),
    no_dups_labeled(T),
    no_dups_labeled(TT).

show_board([]).
show_board([Xs|Xss]) :-
    write(Xs), nl,
    show_board(Xss).

ohhi(N0, C) :- solve(N0, C, T), show_board(T).

solve_test(N0, C, T, R) :-
    statistics(cpu_time, [Start|_]),
    solve(N0, C, T),
    statistics(cpu_time, [End|_]),
    show_board(T),
    R is End - Start.

solve_spec :- ohhi(6, [c(1, [1|1]),c(1, [1|4]),c(0, [1|7]),c(1, [2|3]),c(0, [2|10]),c(1, [3|3]),c(0, [3|5]),c(1, [3|8]),c(0, [3|10]),c(0, [3|12]),c(1, [4|1]),c(1, [4|2]),c(0, [4|5]),c(1, [5|2]),c(0, [5|6]),c(1, [5|8]),c(1, [5|10]),c(0, [6|6]),c(0, [6|9]),c(0, [7|3]),c(1, [8|10]),c(1, [8|11]),c(0, [9|1]),c(0, [9|2]),c(1, [9|4]),c(0, [9|6]),c(0, [9|9]),c(1, [10|6]),c(1, [10|7]),c(1, [10|12]),c(1, [11|4]),c(0, [11|9]),c(0, [12|3]),c(0, [12|6]),c(0, [12|12])]).

:- initialization(solve_spec).

% So, I tried to use the solver on a 12x12 board, and my fastest 12x12 time is 5:40... I was 75% done with the inputs when I realized I had taken 7 minutes already... crime doesn't pay.
% Welp.  Just got to automate the input too!

/* Easy query copy-pasted for your convenience.  Put the result of constraints.py in between the empty list in solve().
statistics(runtime, [Start|_]), solve(6, [], T), statistics(runtime, [End|_]), R is End - Start, !.
*/
