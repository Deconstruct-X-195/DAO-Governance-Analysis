# DAO Governance Power Concentration Analysis

An empirical analysis of voting power distribution in Uniswap DAO governance,
examining whether decentralized autonomous organizations achieve genuine 
decentralization in practice.

## Research Question

Do DAOs governed by token-weighted voting achieve decentralized decision-making,
or does governance power concentrate among a small number of addresses —
consistent with Michels' Iron Law of Oligarchy?

## Key Findings

Analyzing 5 recent Uniswap governance proposals via Snapshot API:

| Metric | Value |
|--------|-------|
| Average Gini Coefficient | 0.968 |
| Top 10 addresses control | 99.7% of voting power |
| Average voters per proposal | ~245 addresses |

A Gini coefficient of 0.968 indicates near-complete concentration —
higher than the wealth inequality of any country on Earth.
The top 10 addresses control 99.7% of all voting power,
suggesting that Uniswap DAO governance is effectively controlled
by a small oligarchy despite its decentralized design.

## Data & Methodology

- **Data source**: Snapshot GraphQL API (hub.snapshot.org)
- **Space**: uniswapgovernance.eth
- **Proposals analyzed**: 5 most recent closed proposals
- **Metrics**: Gini coefficient, top-10 address concentration ratio,
  average voting power per participant

## Files

| File | Description |
|------|-------------|
| dao_governance.py | Fetch proposal metadata |
| dao_votes.py | Fetch per-proposal vote records |
| dao_gini.py | Compute Gini coefficient and concentration metrics |
| dao_viz.py | Visualize results |
| uniswap_proposals.csv | Raw proposal data |
| uniswap_votes.csv | Raw vote records |
| dao_gini_analysis.csv | Computed concentration metrics |
| dao_power_concentration.png | Visualization |

## Motivation

This project was inspired by Rabetti (2024)'s work on centralized governance
in decentralized organizations. The findings suggest that rational apathy
among small token holders, combined with capital concentration among early
investors and institutional holders, produces governance structures that
closely resemble traditional centralized organizations.
