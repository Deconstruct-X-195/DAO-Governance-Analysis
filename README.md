We conducted three independent verification layers:

**Layer 1 — ERC20 Token Transfers (1000 records per address):**
- No direct ERC20 transfers found between the 4 addresses
- Split_1 and Split_2 primarily operate LIT and BIO tokens, not $LAB
- Aster_Related shows only 6 ERC20 records, extremely low activity

**Layer 2 — ETH Native Transfers (1000 records per address):**
- No direct ETH transfers found between the 4 addresses
- Gate_Deposit: single transaction of 745 ETH (~$1.6M), institutional scale
- Aster_Related: 1000 incoming, 0 outgoing, max 0.1 ETH — not a market
  maker wallet, likely a contract or crowdfunding address

**Layer 3 — Internal Contract Calls:**
- Split_2 receives large ETH amounts (40–100 ETH per call) from
  0x3B4D794a66304F130a4Db8F2551B0070dFCf5ca7
- This address is identified as **Lighter: ZkLighter** — a ZK-based DEX contract
- Split_2's ETH source is a DEX, NOT Gate_Deposit
- This directly contradicts the Gate→Split_2 link in EnHeng's chain

**Final Conclusion:**
Across all three verification layers, the described fund flow chain
Gate→Split_1→Split_2→Aster cannot be independently verified.

The critical finding: Split_2's primary ETH source is ZkLighter DEX,
not Gate_Deposit. EnHeng's chain either:
1. Relies on data sources beyond public Etherscan API
2. Contains intermediate hop addresses not included in the report
3. May conflate separate market-making operations across different tokens

**Methodological Insight:**
Professional on-chain analysis requires multi-layer verification.
Single-tool or single-layer analysis produces systematically incomplete
results. The honest documentation of these limitations is itself a
contribution — it defines the boundary conditions of public blockchain
forensics.

## Data & Methodology

- **Data source 1**: Snapshot GraphQL API (hub.snapshot.org)
- **Data source 2**: Etherscan API V2
- **DAO Space**: uniswapgovernance.eth
- **Proposals analyzed**: 5 most recent closed proposals
- **Addresses tracked**: 4 addresses from EnHeng's report
- **Transfer types**: ERC20 + ETH native + internal contract calls

## Files

| File | Description |
|------|-------------|
| dao_governance.py | Fetch Uniswap proposal metadata from Snapshot |
| dao_votes.py | Fetch per-proposal vote records |
| dao_gini.py | Compute Gini coefficient and concentration metrics |
| dao_viz.py | Visualize governance concentration results |
| fund_flow.py | Fetch ERC20 token transfers for tracked addresses |
| fund_flow_analysis.py | Analyze cross-address fund flows (ERC20) |
| fund_flow_eth.py | Fetch and analyze ETH native transfers |
| fund_flow_internal.py | Fetch and analyze internal contract calls |
| uniswap_proposals.csv | Raw proposal data |
| uniswap_votes.csv | Raw vote records |
| dao_gini_analysis.csv | Computed concentration metrics |
| fund_flow_raw.csv | Raw ERC20 transfer data |
| fund_flow_eth.csv | Raw ETH native transfer data |
| fund_flow_internal.csv | Raw internal contract call data |
| dao_power_concentration.png | Governance concentration visualization |

## Theoretical Framework

Decentralization exists on a spectrum rather than as a binary state:

- **Bitcoin**: Most decentralized — rules encoded in immutable code,
  founder disappeared, no entity can modify the 21M cap
- **Ethereum**: Hybrid — code rules plus limited human influence
- **Uniswap/DeFi**: Rules modifiable by token holders, empirically
  controlled by ~10 addresses (Gini 0.968)
- **DAOs**: Named decentralized, functionally oligarchic

The deeper the protocol layer, the closer to genuine decentralization.
The higher the application layer, the more centralized in practice.

## Motivation

This project was inspired by Rabetti (2024)'s work on centralized governance
in decentralized organizations, and by on-chain analyst EnHeng's public
market analysis. Both point to the same structural tendency: decentralized
systems consistently produce centralized outcomes through rational apathy,
capital concentration, and information asymmetry.
