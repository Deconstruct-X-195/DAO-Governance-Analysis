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

## Extended Analysis: ETH Native Transfer Tracking

To verify the fund flow chain described in on-chain analyst EnHeng's report,
we extended the analysis to include ETH native transfers across the same 4 addresses.

**Results:**
- No direct ETH transfers found between the 4 addresses (1000+ records per address)
- Combined with ERC20 analysis: the described fund flow chain cannot be verified
  using Etherscan API alone
- Aster_Related address shows anomalous behavior: 1000 incoming transactions,
  0 outgoing, max value 0.1 ETH — inconsistent with a market maker wallet,
  more likely a contract or crowdfunding address
- Gate_Deposit shows institutional-scale activity: single transaction of 745 ETH
  (~$1.6M), consistent with market maker operations

**Conclusion:**
Professional on-chain analysis requires deeper data sources beyond block explorers.
Single-tool analysis has inherent blind spots. Honest documentation of limitations
is itself a contribution to the field.


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
