+++
title = "Guaranteed Optimal Compositional Explanations for Neurons"
publication = "arXiv preprint arXiv:2511.20934"
journal = "arXiv preprint arXiv:2511.20934"
year = "2025"
date = "2025-11-25"
abstract = "While neurons are the basic units of deep neural networks, it is still unclear what they learn and if their knowledge is aligned with that of humans. Compositional explanations aim to answer this question by describing the spatial alignment between neuron activations and concepts through logical rules. These logical descriptions are typically computed via a search over all possible concept combinations. Since computing the spatial alignment over the entire state space is computationally infeasible, the literature commonly adopts beam search to restrict the space. However, beam search cannot provide any theoretical guarantees of optimality, and it remains unclear how close current explanations are to the true optimum. In this theoretical paper, we address this gap by introducing the first framework for computing guaranteed optimal compositional explanations. Specifically, we propose: (i) a decomposition that identifies the factors influencing the spatial alignment, (ii) a heuristic to estimate the alignment at any stage of the search, and (iii) the first algorithm that can compute optimal compositional explanations within a feasible time. Using this framework, we analyze the differences between optimal and non-optimal explanations in the most popular settings for compositional explanations, the computer vision domain and Convolutional Neural Networks. In these settings, we demonstrate that 10-40 percent of explanations obtained with beam search are suboptimal when overlapping concepts are involved. Finally, we evaluate a beam-search variant guided by our proposed decomposition and heuristic, showing that it matches or improves runtime over prior methods while offering greater flexibility in hyperparameters and computational resources."
url_dataset = ""
url_pdf = "https://arxiv.org/pdf/2511.20934"
url_project = ""
url_slides = ""
url_video = ""
[[authors]]
  name = "La Rosa, Biagio"
  is_member = true
[[authors]]
  name = "Gilpin, Leilani H"
  is_member = true
+++
