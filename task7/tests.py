"""
tests.py
Simple tests for backward chaining
"""

from backchain import backchain_to_goal_tree

rules = [
    (['?x is human'], '?x is mortal'),
    ([], 'Socrates is human'),
    ([], 'Plato is human'),
]

def test_socrates():
    goal = 'Socrates is mortal'
    tree = backchain_to_goal_tree(rules, goal)
    print("Socrates test:", tree)

def test_plato():
    goal = 'Plato is mortal'
    tree = backchain_to_goal_tree(rules, goal)
    print("Plato test:", tree)

def test_nonexistent():
    goal = 'Aristotle is mortal'
    tree = backchain_to_goal_tree(rules, goal)
    print("Aristotle test:", tree)

if __name__ == "__main__":
    test_socrates()
    test_plato()
    test_nonexistent()
