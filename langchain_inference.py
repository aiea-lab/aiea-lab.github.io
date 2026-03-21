from langchain_core.runnables import RunnableLambda

# ----------------------
# Knowledge Base
# ----------------------
facts = [
    ("parent", "alice", "bob"),
    ("parent", "bob", "charlie"),
    ("parent", "charlie", "dave"),
    ("human", "alice"),
    ("human", "bob"),
    ("human", "charlie"),
]

# ----------------------
# Rules
# ----------------------
def is_grandparent(x, y, trace):
    for f1 in facts:
        if f1[0] == "parent" and f1[1] == x:
            z = f1[2]
            for f2 in facts:
                if f2[0] == "parent" and f2[1] == z and f2[2] == y:
                    trace.append(f"{x} -> {z} -> {y} (grandparent rule)")
                    return True
    return False


def is_mortal(x, trace):
    for f in facts:
        if f == ("human", x):
            trace.append(f"{x} is human -> mortal")
            return True
    return False


# ----------------------
# Inference Function
# ----------------------
def run_query(query: str):
    trace = []

    if query == "grandparent(alice, charlie)":
        result = is_grandparent("alice", "charlie", trace)

    elif query == "mortal(alice)":
        result = is_mortal("alice", trace)

    else:
        result = False

    return {
        "query": query,
        "result": result,
        "trace": trace
    }


# ----------------------
# LangChain Wrapper
# ----------------------
chain = RunnableLambda(run_query)


# ----------------------
# Run test
# ----------------------
if __name__ == "__main__":
    output = chain.invoke("grandparent(alice, charlie)")

    print("Query:", output["query"])
    print("Result:", output["result"])
    print("Trace:")
    for step in output["trace"]:
        print("-", step)
