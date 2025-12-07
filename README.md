# From "Onion Not Found" to Guard Discovery - Validation and Countermeasures Study

This repository contains an extension of the PETS'22 paper "From Onion Not Found to Guard Discovery" by Oldenburg, Acar, and Diaz. Our work validates the persistence of the guard discovery vulnerability in 2025 and evaluates countermeasure effectiveness.

Original paper: https://www.esat.kuleuven.be/cosic/publications/article-3392.pdf
Original repository: https://github.com/numbleroot/from-onion-not-found-to-guard-discovery

## Our Contributions

This fork contains two major validation studies:

1. 2020 Study: Replication of original experiments with updated Tor network data from September 2020
2. 2025 Study: Temporal validation demonstrating the vulnerability remains effective despite network growth

3. Countermeasure Evaluation: Analysis of token bucket rate limiting and Vanguards-lite defense mechanisms

Attack overview available in original paper.


## Key Findings

Network Growth 2020-2025:
- Total relays increased from 6451 to 9186 (+42.4%)
- HSDir nodes increased from 3905 to 5007 (+28.2%)

Attack Persistence:
- Median attack time increased by only 0.2 seconds despite network growth
- Success rate remains 85-100% across all configurations
- Vulnerability is structural and cannot be mitigated by network growth alone

Countermeasure Analysis:
- Token bucket rate limiting (60 tokens/min) increases attack time by 23-32 seconds
- Original paper proposal (6 tokens/min, 10 initial tokens) creates severe DoS vulnerability: legitimate users exhausted tokens in 5-10 seconds
- Realistic configuration (60 tokens/min, 5 initial tokens) balances security and usability
- Vanguards-lite provides additional protection when L2 guards are not compromised
- Combined countermeasures offer strongest defense but require careful parameter tuning

## Repository Structure

Original paper sections (3_cell-pattern through 6_countermeasures) contain baseline experiments.

Our validation studies:
- 5_evaluation/study-2020: Replication with September 2020 network data
- 5_evaluation/study-2025: Temporal validation with November 2025 network data
- 6_countermeasures/study-2020: Countermeasure evaluation with 2020 parameters
- 6_countermeasures/study-2025: Updated countermeasure analysis with realistic configurations

See README.md files in each study directory for detailed documentation.

## Setup

This fork requires Python 3 with Jupyter, numpy, pandas, seaborn, matplotlib, and stem libraries. Simulation scripts use the same dependencies as the original repository.


## Our Data Sets

Validation Study Data (2020):
- 5_evaluation/2_data_attack-time: Attack simulation results with September 2020 network (6451 relays)
- 6_countermeasures/1_data_token-bucket: Token bucket countermeasure evaluation

Validation Study Data (2025):
- 5_evaluation/study-2025/data: November 2025 consensus and relay CSV (9186 relays)
- 5_evaluation/study-2025/results: Attack simulation results demonstrating persistence
- 6_countermeasures/study-2025/data: Countermeasure evaluation with realistic parameters

Original Paper Data:
- OSF repository (64.5 GB): https://osf.io/t9x4b/
- Additional datasets in 4_attack-tuning subdirectories


## Reproducing Our Studies

2020 Validation Study:
1. See 5_evaluation/study-2020/README.md for attack simulation replication
2. See 6_countermeasures/study-2020/README.md for countermeasure evaluation

2025 Validation Study:
1. Download November 2025 consensus or use provided data in 5_evaluation/study-2025/data
2. Run attack simulations following 5_evaluation/study-2025/README.md
3. Evaluate countermeasures following 6_countermeasures/study-2025/README.md
4. Compare results with 2020 data using provided comparison scripts

Analysis Notebooks:
- 5_evaluation/study-2025/1_analysis_noise-lookup-rate_2025.ipynb
- 5_evaluation/study-2025/2_analysis_attack-time_2025.ipynb
- 6_countermeasures/study-2025/1_analysis_token-bucket_2025.ipynb
- 6_countermeasures/study-2025/4_analysis_realistic-refill_2025.ipynb

Original Paper Reproduction:
- 3_cell-pattern: Cell pattern analysis
- 4_attack-tuning: Attack optimization
- 5_evaluation: Original evaluation
- 6_countermeasures: Original countermeasure analysis


## Methodology

Our studies use the original attack simulation framework with updated network parameters:
- attack_simulation.py modified to use current relay consensus data
- attack_simulation_refill_on.py extended to evaluate token bucket and Vanguards-lite countermeasures
- 100 simulation runs per configuration for statistical significance
- Network data collected from official Tor consensus archives

Key modifications:
- Updated N_HSDIRS parameter to reflect network growth
- Implemented token bucket rate limiting (60 tokens/min realistic configuration)
- Added Vanguards-lite L2 guard rotation simulation
- Maintained original methodology for result comparability

## Conclusions

The guard discovery vulnerability identified in the original paper remains highly effective in 2025 despite significant network growth. Token bucket rate limiting provides meaningful protection but can be bypassed with patient attackers. 

Critical discovery: The original paper's token bucket configuration (6 tokens/min, 10 initial tokens) creates a severe DoS vulnerability. Legitimate onion service clients exhaust their token allowance in 5-10 seconds during normal browsing, effectively blocking access. Our analysis demonstrates that realistic configurations require significantly higher refill rates (60 tokens/min) to maintain usability while still providing meaningful attack mitigation.

Vanguards-lite offers additional defense when adversarial control of L2 guards is limited. The fundamental issue is structural in Tor's HSDir lookup protocol and requires protocol-level countermeasures rather than relying on network growth.

## References

Original paper:
```
@article{OldenburgAcarDiaz_GuardDiscovery,
    title   = {{From "Onion Not Found" to Guard Discovery}},
    author  = {Lennart Oldenburg and Gunes Acar and Claudia Diaz},
    journal = {Proceedings on Privacy Enhancing Technologies},
    number  = {1},
    volume  = {2022},
    year    = {2022},
    doi     = {doi:10.2478/popets-2022-0026},
    url     = {https://doi.org/10.2478/popets-2022-0026},
    pages   = {522--543}
}
```

This validation study: Academic project validating and extending the original work, 2025.
