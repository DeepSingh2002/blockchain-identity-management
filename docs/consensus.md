# Consensus mechanism (slide 9-D)

> "Identity transactions are validated using Proof-of-Authority (PoA) or
> Byzantine Fault Tolerance (BFT) to ensure security and efficiency." —
> seminar, slide 9

This layer is deliberately **not reimplemented** in this repo, for an
honest reason: PoA and BFT-style consensus (e.g. IBFT 2.0, QBFT) are
properties of the underlying permissioned chain, not application code you
write on top of it. Reimplementing a consensus engine from scratch would be
its own multi-month systems project, not a smart-contract exercise.

For this identity-management use case, the standard, production path is:

1. Deploy `IdentityRegistry.sol` and `AccessControl.sol` to a **permissioned
   Ethereum-compatible network** running PoA or IBFT/QBFT consensus —
   e.g. **Hyperledger Besu** (supports IBFT 2.0 / QBFT out of the box) or
   **Quorum**, rather than public Ethereum mainnet.
2. A known, vetted set of validators (the "authorities" — e.g. government
   IT department nodes, per the base paper's public-sector setting) run the
   consensus protocol; citizens and services only ever interact with the
   two contracts above via a regular JSON-RPC endpoint.
3. Because validators are known and permissioned rather than open/anonymous,
   the network gets faster finality and lower overhead than proof-of-work —
   which is the efficiency argument the seminar makes for choosing PoA/BFT
   over a public, permissionless chain for a government identity system.

If a from-scratch consensus simulation is wanted for demonstration purposes
(e.g. a toy PoA round-robin leader election over a handful of local nodes),
that's a good next addition — flag it and it can be built as its own
module rather than folded into the contracts above.
