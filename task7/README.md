# Task 7: Backward Chaining FOL Assignment!!

Overview
We will be implementing a Backward Chaining System for First Order Logic (FOL).  
Backward chaining is goal-driven: it starts from a hypothesis and works backward to see which facts/rules support it.

Files

- `backchain.py` – main backward chaining implementation.
- `tests.py` – example tests.
- `README.md` – this tutorial.

## How to Use

1. define rules as (premises, conclusion) tuples in backchain.py  
2. call backchain_to_goal_tree(rules, hypothesis) to generate the goal tree  
3. run tests.py to see sample outputs

## Example

 in python
rules = [
    (['?x is human'], '?x is mortal'),
    ([], 'Socrates is human')
]

goal = 'Socrates is mortal'
tree = backchain_to_goal_tree(rules, goal)
print(tree)
