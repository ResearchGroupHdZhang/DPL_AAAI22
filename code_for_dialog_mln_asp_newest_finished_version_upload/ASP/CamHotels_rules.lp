%%% SLOTS
% stars(4;3;2;0).
% area(west;east;north;south;centre).
% haspark(park;nopark).
% kind(guesthouse;hotel).
% pricerange(moderate;expensive;cheap).


is_area(west;east;north;south;centre).



%% Facts about the factors
traffic(X,good) :- is_area(X), not traffic(X,bad).
weather(good) :- not weather(bad).

%% Domain Knowledge

% Topology
pass(west, centre, east).
pass(west, centre, north).
pass(south, centre, east).
pass(south, centre, north).

% Alternative topology
% pass(west, centre, east).
% pass(west, centre, south).
% pass(north, centre, east).
% pass(north, centre, south).
% pass(east, centre, south).

pass(X,Z,Y) :- pass(Y,Z,X), is_area(X;Y;Z).


%% Commonsense Knowledge
update_area(X) :- weather(bad), user_loc(X), is_area(X).
update_hasparking(1) :- weather(bad).

update_area(X) :- traffic(X,bad), user_loc(X), is_area(X), weather(good).

{update_area(X):traffic(X,good)}=1 :- user_loc(Y), traffic(Y,good), weather(good).

:- update_area(X), user_loc(Y), X!=Y, pass(Y,Z,X), traffic(Z,bad).



