"""
backchain.py
Backward Chaining System for First Order Logic (FOL)
"""

from collections import defaultdict

def unify(x, y, subs={}):
    if subs is None:
        return None
    elif x == y:
        return subs
    elif isinstance(x, str) and x.startswith('?'):
        return unify_var(x, y, subs)
    elif isinstance(y, str) and y.startswith('?'):
        return unify_var(y, x, subs)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for xi, yi in zip(x, y):
            subs = unify(xi, yi, subs)
            if subs is None:
                return None
        return subs
    else:
        return None

def unify_var(var, x, subs):
    if var in subs:
        return unify(subs[var], x, subs)
    elif x in subs:
        return unify(var, subs[x], subs)
    else:
        subs[var] = x
        return subs

def backchain_to_goal_tree(rules, hypothesis, visited=None):
    if visited is None:
        visited = set()

    if hypothesis in visited:
        return hypothesis
    visited.add(hypothesis)

    tree = hypothesis
    for premises, conclusion in rules:
        subs = unify(conclusion, hypothesis, {})
        if subs is not None:
            subgoals = []
            for premise in premises:
                goal = premise
                for var, val in subs.items():
                    goal = goal.replace(var, val)
                subgoal_tree = backchain_to_goal_tree(rules, goal, visited)
                subgoals.append(subgoal_tree)
            tree = {'OR': [tree, {'AND': subgoals}]} if subgoals else tree
    return tree

if __name__ == "__main__":
    rules = [
        (['?x is human'], '?x is mortal'),
        ([], 'Socrates is human')
    ]
    goal = 'Socrates is mortal'
    tree = backchain_to_goal_tree(rules, goal)
    print(tree)
