# Task 9: LangGraph Logical Inference

This task migrates the Task 8 LangChain logical inference engine to 
**LangGraph**, expanding capabilities.

## Implementation

- LangGraph initialized with a small knowledge base (10 facts, 5 rules).
- Rules include `grandparent/2` and `ancestor/2` to infer relationships.
- RAG used to retrieve context from KB (via facts).
- Logical inference outputs both **true/false** for queries and a 
**deduction trace**.

## Tests

- `grandparent(gita, soha)?` → True
- `ancestor(mary, soha)?` → True
- Trace prints each step in the deduction.

