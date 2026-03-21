from langgraph import LangGraph

# Initialize LangGraph engine
lg = LangGraph(model="gpt-4")

# --- Define knowledge base ---
facts = [
    "parent(soha, sia).",
    "parent(pinki, soha).",
    "parent(gita, pinki).",
    "parent(john, soha).",
    "parent(mary, john)."
]

rules = [
    "grandparent(X, Y) :- parent(X, Z), parent(Z, Y).",
    "ancestor(X, Y) :- parent(X, Y).",
    "ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y)."
]

# Load KB into LangGraph
for fact in facts:
    lg.add_fact(fact)
for rule in rules:
    lg.add_rule(rule)

# --- Query function ---
def query_kg(query_str):
    result, trace = lg.infer(query_str)
    return result, trace

# Example usage
if __name__ == "__main__":
    q = "grandparent(gita, soha)?"
    res, trace = query_kg(q)
    print(f"Query: {q}")
    print(f"Result: {res}")
    print("Trace:")
    for step in trace:
        print(" -", step)
