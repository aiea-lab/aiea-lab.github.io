parent(homer, bart).
parent(homer, lisa).
parent(marge, bart).
parent(marge, lisa).
parent(abraham, homer).
parent(mona, homer).
parent(marge, herb).

male(homer).
male(bart).
male(abraham).
male(herb).

female(marge).
female(lisa).
female(mona).

father(X,Y) :- parent(X,Y), male(X).
mother(X,Y) :- parent(X,Y), female(X).
grandparent(X,Y) :- parent(X,Z), parent(Z,Y).