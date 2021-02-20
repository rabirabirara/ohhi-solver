
% fd_fliplength(0, []).
% fd_fliplength(N, [_|Xs]) :-
%     fd_fliplength(N0, Xs),
%     N #= N0 + 1.

fliplength(N, T) :- length(T, N).
flipdomain(X, Y, T) :- fd_domain(T, X, Y).

% n_i_times(_, 0, []).
% n_i_times(N, I, [X|Xs]) :-
%     X = N,
%     I_prime is I - 1,
%     n_i_times(N, I_prime, Xs).

    

% transpose/2 and foldl/5, informed by SWI-Prolog's apply.pl and clpfd.pl libraries.
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

% No two rows/columns the same.
% fd_all_different only works on lists of evaluables.
fd_member(X, [H|T]) :- X #= H ; fd_member(X, T).

fd_same_list([], []).
fd_same_list([X|Xs], [Y|Ys]) :- X #= Y, fd_same_list(Xs, Ys).
% Okay, this works with query:
% ?- make2x2(2, [A,B]), fd_same_list(A, B), fd_labeling(A), fd_labeling(B).
% How to make it work for lists of lists?

list_member(Xs, [Hs|Ts]) :- fd_same_list(Xs, Hs) ; list_member(Xs, Ts).

fd_all_different_lists([]).
fd_all_different_lists([Xs|Xss]) :-
    list_member(Xs, Xss), !, fail.
fd_all_different_lists([_|Xss]) :- fd_all_different_lists(Xss).
% Always make the base case the empty list if you can!

% This works!!  Now get fd_all_different_lists to work.
fd_all_same([_]).
fd_all_same([A, B|Xs]) :-
    fd_same_list(A, B),
    fd_all_same([B|Xs]).


% No three of same number contiguously.
% FINALLY GOT IT TO WORK!  A bit off, but it's progress.
% fd_no_threes([_, _]).
% fd_no_threes([A, B, C | T]) :-
%     (A #= B, B #= C) -> !, fail;
%     fd_no_threes([B,C|T]), !.
% fd_no_threes([]).
% fd_no_threes([A, B, C | T]) :-
%     (
%         A #= B,
%         B #= C
%     ) -> !, fail.
% fd_no_threes([_|T]) :- fd_no_threes(T).
% fd_no_threes([A, B, C | _]) :-
%     non_fd_var(A),
%     non_fd_var(B),
%     non_fd_var(C), 
%     A #= B,
%     B #= C,
%     !, fail.
% % fd_no_threes([X, X, X | _]) :- !, fail. 
% fd_no_threes([_ | T]) :- fd_no_threes(T).

fd_and3(X, Y, Z, R) :-
    X #/\ Y,

fd_nodup3(

% Without using cut and fail.  Test.
no_threes([_, _]).
no_threes([A, B, C|T]) :-
    (A \= B
    ;B \= C
    ;A \= C
    ), no_threes([B, C | T]), !.


% Equal count of each number in a row/column.
% Pass a Grid as argument; don't use maplist().
% Include fd_domain(); it crashes without it.
fd_exactly_N(N, [Xs]) :-
    fd_domain(Xs, 1, 2),
    fd_exactly(N, Xs, 1),
    fd_exactly(N, Xs, 2).
fd_exactly_N(N, [Xs|Xss]) :-
    fd_domain(Xs, 1, 2),
    fd_exactly(N, Xs, 1),
    fd_exactly(N, Xs, 2),
    fd_exactly_N(N, Xss).

% ohhi_format([Xs], N) :-
%     length(Xs, N),
%     fd_no_threes(Xs).
%
% ohhi_format([Xs|Xss], N) :-
%     length(Xs, N),
%     fd_no_threes(Xs),
%     ohhi_format(Xss, N).

ohhi_access(Grid, [I|J], Color) :-
    nth(I, Grid, RowI),
    nth(J, RowI, Color).

% Fixed board parts are the only variable constraint.
ohhi_constraint(Grid, c(Color, Square)) :-
    ohhi_access(Grid, Square, Color0),
    Color #= Color0.

% N0 is the half the size of the board.
solve(N0, C, T) :-
    N #= N0 * 2,
    length(T, N),
    maplist(fliplength(N), T),
    fd_exactly_N(N0, T),
    % fd_all_different_lists(T),
    % maplist(fd_no_threes, T),
    transpose(T, TT),
    fd_exactly_N(N0, TT),
    % fd_all_different_lists(TT),
    % maplist(fd_no_threes, TT),
    maplist(ohhi_constraint(T), C),
    maplist(fd_labeling, T).

makeNxN(N0, T) :-
    N #= N0 * 2,
    length(T, N),
    maplist(fliplength(N), T),
    % maplist(fd_no_threes, T),
    fd_exactly_N(N0, T).
    % maplist(flipdomain(1, N), T).
    % fd_all_different_lists(T),
    % maplist(fd_labeling, T).



% fd_no_threes([_, _]).
% fd_no_threes([A, B, C | T]) :-
%     (A #\= B; A #\= C; B #\= C),
%     fd_no_threes([B,C|T]).
% fd_no_threes([A, B, C | T]) :-
%     fd_all_different([A,B,C]),
%     fd_no_threes([B,C|T]).

makelist(N0, T) :-
    N #= N0 * 2,
    length(T, N),
    fd_domain(T, 1, 2),
    fd_exactly(N0, T, 1),
    fd_exactly(N0, T, 2),
    fd_no_threes(T),
    fd_labeling(T).

