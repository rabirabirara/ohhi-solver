?- use_module(library(clpb)).
?- use_module(library(clpfd)).

fliplength(N, T) :- length(T, N).


%% Binairo/Takuzu/0hh1/whatever.


% No 3 contiguous squares of same color.
no_3_cont([]) :- !.
no_3_cont([_]) :- !.
no_3_cont([_, _]) :- !.
no_3_cont([A, B, C | T]) :-
    sat(+([A + B + C]) * +([~A + ~B + ~C])), no_3_cont([B, C | T]).
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
% sat(card()) is slower than summation. card() averages around 5500 ms, while sum() averages around 4400 ms.
% n0_many(N0, L) :- sat(card([N0], L)).
n0_many(N0, L) :- sum(L, #=, N0).


% Board access.
access(Grid, [I|J], Color) :-
    nth1(I, Grid, RowI),
    element(J, RowI, Color).

% Fixed board parts are the only variable constraint.
cs(T, c(Color, Square)) :- access(T, Square, Color).


% Constraining count before cardinality seems to yield better performance.
% Maybe if I can move the no_duplicates constraints before no_3_cont, I can improve its performance.
solve(N0, C, T) :-
    N is N0 * 2,
    length(T, N),
    maplist(fliplength(N), T),
    append(T, Vs), Vs ins 0..1,
    maplist(cs(T), C),
    maplist(no_3_cont, T),
    maplist(n0_many(N0), T),
    transpose(T, TT),
    maplist(n0_many(N0), TT),
    maplist(no_3_cont, TT), % Solver clicks here. Worth 3500 milliseconds. Must occur before labeling, else loop.  Show board before/after for a show!
    maplist(labeling, T),
    no_dups_labeled(T),
    no_dups_labeled(TT).

show_board([]).
show_board([Xs|Xss]) :-
    write(Xs), nl,
    show_board(Xss).

ohhi(N0, C) :- solve(N0, C, T), show_board(T).

solve_test(N0, C, T, R) :-
    statistics(runtime, [Start|_]),
    solve(N0, C, T),
    statistics(runtime, [End|_]),
    show_board(T),
    R is End - Start.


% So, I tried to use the solver on a 12x12 board, and my fastest 12x12 time is 5:40... I was 75% done with the inputs when I realized I had taken 7 minutes already... crime doesn't pay.
% Welp.  Just got to automate the input too!

/* Easy query copy-pasted for your convenience.  Put the result of constraints.py in between the empty list in solve().
statistics(runtime, [Start|_]), solve(6, [], T), statistics(runtime, [End|_]), R is End - Start, !.
*/
