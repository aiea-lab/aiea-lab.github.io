+++
title = "VFSI: Validity First Spatial Intelligence for Constraint-Guided Traffic Diffusion"
publication = "arXiv preprint arXiv:2509.23971"
journal = "arXiv preprint arXiv:2509.23971"
year = "2025"
date = "2025-09-28"
abstract = "Modern diffusion models generate realistic traffic simulations but systematically violate physical constraints. In a large-scale evaluation of SceneDiffuser++, a state-of-the-art traffic simulator, we find that 50% of generated trajectories violate basic physical laws - vehicles collide, drive off roads, and spawn inside buildings. This reveals a fundamental limitation: current models treat physical validity as an emergent property rather than an architectural requirement. We propose Validity-First Spatial Intelligence (VFSI), which enforces constraints through energy-based guidance during diffusion sampling, without model retraining. By incorporating collision avoidance and kinematic constraints as energy functions, we guide the denoising process toward physically valid trajectories. Across 200 urban scenarios from the Waymo Open Motion Dataset, VFSI reduces collision rates by 67% (24.6% to 8.1%) and improves overall validity by 87% (50.3% to 94.2%), while simultaneously improving realism metrics (ADE: 1.34m to 1.21m). Our model-agnostic approach demonstrates that explicit constraint enforcement during inference is both necessary and sufficient for physically valid traffic simulation."
url_dataset = ""
url_pdf = "https://arxiv.org/pdf/2509.23971?"
url_project = ""
url_slides = ""
url_video = ""
[[authors]]
  name = "Chauhan, Kargi"
  is_member = false
[[authors]]
  name = "Gilpin, Leilani H"
  is_member = true
+++
