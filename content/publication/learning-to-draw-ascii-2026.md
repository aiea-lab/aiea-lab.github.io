+++
title = "Learning to Draw ASCII Improves Spatial Reasoning in Language Models"
publication = "arXiv preprint arXiv:2604.14641"
journal = "arXiv preprint arXiv:2604.14641"
year = "2026"
date = "2026-04-16"
abstract = "When faced with complex spatial problems, humans naturally sketch layouts to organize their thinking, and the act of drawing further sharpens their understanding. In this work, we ask whether a similar principle holds for Large Language Models (LLMs): can learning to construct explicit visual layouts from spatial descriptions instill genuine spatial understanding? We introduce Text2Space, a dataset that pairs natural language descriptions with ground-truth ASCII grid layouts and spatial QA pairs, enabling us to separate failures in constructing spatial representations from failures in reasoning over them. We adopt ASCII because it is human-readable, operates entirely within the token space of language models, and encodes spatial relations in a structurally verifiable form. Our evaluation reveals a pronounced \"Read-Write Asymmetry\": LLMs interpret ASCII representations effectively but struggle to produce them from text, and these construction errors propagate to incorrect answers downstream. To address this limitation, we train models on layout construction (TextASCII) and find that it significantly improves spatial reasoning from text alone, even without producing any ASCII at inference time. Combining construction with comprehension training further amplifies these gains. Crucially, these improvements transfer to three external spatial reasoning benchmarks, demonstrating that, much as sketching sharpens human spatial thinking, learning to construct explicit layouts instills spatial understanding that generalizes beyond the training format."
url_dataset = ""
url_pdf = "https://arxiv.org/pdf/2604.14641"
url_project = ""
url_slides = ""
url_video = ""
[[authors]]
  name = "Huang, Shiyuan"
  is_member = true
[[authors]]
  name = "Liu, Li"
  is_member = true
[[authors]]
  name = "He, Jincheng"
  is_member = false
[[authors]]
  name = "Gilpin, Leilani H"
  is_member = true
+++
