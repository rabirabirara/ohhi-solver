?- use_module(library(clpb)).
?- use_module(library(clpfd)).

fliplength(N, T) :- length(T, N).


% Binairo/Takuzu/whatever.

% No 3 contiguous squares of same color.
no_3_cont([]) :- !.
no_3_cont([_]) :- !.
no_3_cont([_, _]) :- !.
no_3_cont([A, B, C | T]) :-
    sat(+([A, B, C]) * +([~A, ~B, ~C])), no_3_cont([B, C | T]).
% Don't use cut fail there. Fails the ENTIRE thing.

% No two rows/columns are same.
list_eq([], []).
list_eq([X|Xs], [Y|Ys]) :- X = Y, list_eq(Xs, Ys).

list_member(Xs, [Hs|Ts]) :- list_eq(Xs, Hs) ; list_member(Xs, Ts).

list_not_member(Xs, [Hs|Ts]) :- dif(Xs, Hs) ; list_not_member(Xs, Ts).

no_dup_lists([]).
no_dup_lists([Xs|Xss]) :- list_not_member(Xs, Xss), no_dup_lists(Xss).
% no_dup_lists([]).
% no_dup_lists([Xs|Xss]) :- not(list_member(Xs, Xss)), no_dup_lists(Xss).
% DON'T USE CUT FAIL.  CUT FAIL IS PROVEN TO NOT WORK
% WITH BOOLEAN CLPB VARIABLES.

% A little faster.  Since we're not using them on CLPB variables anyway.
no_dups_labeled([]).
no_dups_labeled([Xs|Xss]) :-
    list_member(Xs, Xss), !, fail;
    no_dups_labeled(Xss).


% Exactly N0 of each color in a row/column.
n0_many(N0, L) :- sat(card([N0], L)).
% n0_many(N0, L) :- sat_count(L, N0).


% Some squares of the board are fixed.
access(Grid, [I|J], Color) :-
    nth1(I, Grid, RowI),
    element(J, RowI, Color).

% Fixed board parts are the only variable constraint.
cs(T, c(Color, Square)) :- access(T, Square, Color).


solve(N0, C, T) :-
    N is N0 * 2,
    length(T, N),
    maplist(fliplength(N), T),
    maplist(cs(T), C),
    transpose(T, TT),
    maplist(no_3_cont, T),
    maplist(no_3_cont, TT),
    % For some reason... above deterministic, below non??
    maplist(n0_many(N0), T),
    maplist(n0_many(N0), TT),
    % write('0dfl'), nl,
    % no_dup_lists(T),
    % write('1dfl'), nl,
    % no_dup_lists(TT),
    % write('2dfl'), nl,
    maplist(labeling, T),
    % no_dup_lists(T),
    % no_dup_lists(TT).
    no_dups_labeled(T),
    no_dups_labeled(TT),
    show_board(T).

show_board([]).
show_board([Xs|Xss]) :-
    write(Xs), nl,
    show_board(Xss).

% So, I tried to use the solver on a 12x12 board, and my fastest 12x12 time is 5:40... I was 75% done with the inputs when I realized I had taken 7 minutes already... crime doesn't pay.
% Welp.  Just got to automate the input too!

/* Easy query copy-pasted for your convenience.  Put the result of constraints.py in between the empty list in solve().
statistics(runtime, [Start|_]), solve(6, [], T), statistics(runtime, [End|_]), R is End - Start, !.
*/
