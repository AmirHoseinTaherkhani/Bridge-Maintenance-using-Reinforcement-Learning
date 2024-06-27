# Towards Equitable Infrastructure Asset Management

## Scour Maintenance Strategy for Aging Bridge Systems in Flood-prone Zones using Deep Reinforcement Learning

### Overview

This project employs a deep reinforcement learning (DRL) algorithm to optimize the maintenance of bridge systems in flood-prone areas. The goal is to allocate resources efficiently to bridges at risk of scour-induced failure, considering flood degradation, time deterioration, and social vulnerability.

### Key Features

- **Flood Risk Management:** Utilizes Geographic Information System (GIS) data to simulate flood scenarios and assess bridge vulnerabilities.
- **Deep Reinforcement Learning:** Implements a DRL framework to optimize maintenance decisions over a 20-year period.
- **Social Vulnerability Integration:** Incorporates social vulnerability metrics to ensure equitable infrastructure management.
- **Markov Decision Process:** Models bridge conditions and maintenance actions as a Markov Decision Process (MDP).

### Methodology

#### 1. Bridge Condition Modeling
- **Scour Depth Estimation:** Uses the HEC-18 equation to calculate scour depth around bridge piers.
- **Time Deterioration:** Applies a deterioration function to capture the natural aging of bridges.

#### 2. Social Vulnerability Impact Analysis
- **Social Vulnerability Index (SVI):** Developed using 16 social vulnerability factors grouped into four categories: socioeconomic status, household characteristics, racial/ethnic minority status, and housing/transportation.
- **Social Impact Index (SII):** Calculated for each bridge based on proximity to socially vulnerable communities.

#### 3. Economic Cost Assessment
- **Cost of Failure:** Estimates include bridge replacement, detours, and fatalities.
- **Modified Cost of Failure:** Adjusts economic costs based on the Social Impact Index (SII).

#### 4. Deep Reinforcement Learning Framework
- **Environment Modeling:** Uses an MDP to simulate bridge conditions and maintenance decisions.
- **Proximal Policy Optimization (PPO):** Trains the DRL agent to optimize maintenance strategies.


If you use the data or code of this project, please cite the paper below:
