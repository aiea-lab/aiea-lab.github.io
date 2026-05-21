+++
date= "2025-09-27"
description = "Reinforcement Learning in Interpretable Transfer Learning and Falsification"
short_description = "reinforcement learning, falsification, transfer learning"
project_id = ""
picture = "diaa-main-fig.png"
external_link = ""
include_participants_portraits = false
sort_position = 1
title = "Interpretable Transfer Learning"
[[participants]]
    name = "Oliver Chang"
    is_member = true
    id = "oliverchang"
+++

## Interpretable Reinforcement Learning

Transfer learning in deep reinforcement learning (DRL) is becoming an increasingly popular strategy to accelerate learning speed and improve generalizability. Action advising and teacher imitation, in particular, can help a DRL agent  learn a novel task with guidance from a teacher model. In this project, we robustify previous action advising methods by dynamically updating a introspection threshold and benchmarking transfer learning methods from  one task to multiple tasks in increasing difficulty. We employ performance estimation from teacher-guided reinforcement learning to replace the static introspective threshold with a dynamically updating threshold to modulate how much advice should be given to the student. Dynamically Introspective Action Advising (DIAA) aims to make transfer learning transparent while accelerating convergence of the student policy in novel environments.

## Reinforcement Learning for Falsifying Dynnamic Vehicle Controllers

Falsification has been widely used in autonomous vehicles to find safety violations. Cyber-physical systems (CPS) like adaptive cruise control (ACC) have been simulated and tested using sampling-based falsification techniques. However, these techniques are limited global-based falsification methods, applied to a single set of driving scenarios, and do not consider lateral dynamics. In this project, we apply reinforcement learning for counter example discovery. We validate the MOBIL lane change model and ACC in the MetaDrive simulator. We leverage Senic for diverse scenario generation. 
