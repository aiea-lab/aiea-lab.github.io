+++
title = "Abductive Learning"
project_id = "abductive-learning"
draft = false
picture = "projects/trail.png"
short_description = "Reducing LLM hallucinations through neuro-symbolic reasoning and abductive learning for natural-language-to-Prolog translation."
summary = "Reducing LLM hallucinations through neuro-symbolic reasoning and abductive learning for natural-language-to-Prolog translation."
[[participants]]
    name = "Jonathan Morris"
    id = "jonathan_m"
    lead = true
    is_member = true
[[participants]]
    name = "Chanchal Mukeshsingh"
    id = "chanchal"
    is_member = true
[[participants]]
    name = "Sergio Henriquez"
    id = "sergio"
    is_member = true
[[participants]]
    name = "Hugo Lin"
    id = "hugo_l"
    is_member = true
[[participants]]
    name = "Sasidhar Jasty"
    id = "sasidhar"
    is_member = true
[[participants]]
    name = "Chiyan Loo"
    id = "chiyan"
    is_member = true
[[participants]]
    name = "Elson Philip"
    id = "elson"
    is_member = true
[[participants]]
    name = "Sanya Bhatia"
    id = "sanya"
    is_member = true
[[participants]]
    name = "Leilani Gilpin"
    id = "leilani"
    is_member = true
[[participants]]
    name = "Khin (Sabrina) Yone"
    id = "sabrina"
    is_member = true
+++

Our abductive team researches methods of increasing explainability and trustworthiness of Large Language Models (LLM) by reducing the chances of hallucinations. We use a neuro-symbolic approach, where the question and context given to an LLM gets converted to a logic programming language (Prolog) and the answer is deduced by the Prolog interpreter. Currently we are developing a fine tuning method which uses abductive learning to create an LLM that specializes in translating from natural language to Prolog

![Neuro-symbolic reasoning pipeline translating a natural-language question and context into logic, refining it, and using Prolog or Lean to produce an answer with intermediate reasoning and a TRRAIL score.](/img/projects/trail.png)
