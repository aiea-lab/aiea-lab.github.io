from langgraph_inference import query_kg

tests = [
    "grandparent(gita, soha)?",
    "grandparent(pinki, sia)?",
    "ancestor(gita, soha)?",
    "ancestor(mary, soha)?"
]

for t in tests:
    result, trace = query_kg(t)
    print(f"Test: {t}")
    print(f"Result: {result}")
    print("Trace:")
    for step in trace:
        print(" -", step)
    print("---")
