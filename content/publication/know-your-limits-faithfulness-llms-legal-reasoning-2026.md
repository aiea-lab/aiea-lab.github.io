+++
title = "Know Your Limits: On the Faithfulness of LLMs as Solvers and Autoformalizers in Legal Reasoning"
publication = "arXiv preprint arXiv:2606.16118"
journal = "arXiv preprint arXiv:2606.16118"
year = "2026"
date = "2026-06-15"
abstract = "Large Language Models (LLMs) achieve strong performance on reasoning tasks, but whether this reflects faithful logical inference or heuristic approximation remains unclear. We study this question in legal entailment by comparing three paradigms, including pure LLM classification, LLM-based Formal Reasoning, and solver-based Formal Reasoning using the Z3 SMT solver, on a re-annotated subset of ContractNLI across five LLMs. Our re-annotation reveals a systematic and measurable gap between pragmatic legal interpretation and strict formal entailment, where a substantial proportion of legally sound inferences are not formally grounded without additional unstated assumptions. While introducing formal structure improves accuracy, with LLM-based Formal Reasoning achieving the highest benchmark performance, we show that this gain does not imply faithful reasoning. We identify three recurring failure modes: scope laundering, where LLMs report solver-inconsistent classifications without executing the underlying formal reasoning, producing conclusions that appear logically grounded but are not; implicit constraint blindness, where LLMs overlook logical constraints present in formal representations; and program synthesis failures, where LLMs generate incorrect Z3 code despite structured prompting. Critically, scope laundering persists across all models, raising serious concerns about the faithfulness of LLM-based formal reasoning as a proxy for symbolic execution. These results reveal a fundamental gap between benchmark accuracy and logical faithfulness."
url_dataset = ""
url_pdf = "https://arxiv.org/pdf/2606.16118"
url_project = ""
url_slides = ""
url_video = ""
[[authors]]
  name = "Wang, Olivia Peiyu"
  is_member = true
[[authors]]
  name = "Wong-Toropainen, Sanna"
  is_member = false
[[authors]]
  name = "Amrollahi, Daneshvar"
  is_member = false
[[authors]]
  name = "Bai, Ryan"
  is_member = false
[[authors]]
  name = "Bansal, Tashvi"
  is_member = false
[[authors]]
  name = "Garg, Arush"
  is_member = true
[[authors]]
  name = "Gilpin, Leilani H"
  is_member = true
+++
