# blockchain-identity-management# Blockchain-Powered Identity Management (DID + ZKP + Smart Contracts)

**Technical Seminar (21IS81) — Dayananda Sagar College of Engineering, Dept. of Information Science & Engineering, AY 2024-25**
Presented by: Deep Singh (1DS21IS031)
Guide: Dr. Yogesh B S, Assistant Professor, ISE Dept.
Seminar Coordinators: Dr. Vaidehi M, Dr. Bhavani K

## Base paper

A. Padmanegara and R. N. Putri, *"Blockchain and The Public Sector: Blockchain-Based Identity Management Systems For Public Services and The Impact on Privacy and Security Risks,"* 2023 International Conference on Digital Business and Technology Management (ICONDBTM), Jakarta, Indonesia, 2022, pp. 1–6. DOI: [10.1109/ICONDBTM59210.2023.10326737](https://doi.org/10.1109/ICONDBTM59210.2023.10326737)

## What this is

A working reconstruction of the four-part architecture described in the seminar (slide 9), built as real, runnable code rather than a slide diagram:

| Architecture component (seminar) | This repo |
|---|---|
| A. Identity Registration & Verification — decentralized digital ID (DID), public/private key pair | `src/did_registry.py` |
| B. Decentralized Identity Storage — permissioned storage, Zero-Knowledge Proofs so identity is verified without exposing personal data | `src/zkp_schnorr.py` |
| C. Smart Contracts for Identity Authentication — self-sovereign identity (SSI): users control who can access their data | `contracts/IdentityRegistry.sol`, `contracts/AccessControl.sol` |
| D. Consensus Mechanism — Proof-of-Authority / BFT-style validator set | `docs/consensus.md` (design write-up; PoA/BFT consensus is normally provided by the underlying chain — e.g. a Hyperledger Besu / Quorum PoA network — rather than re-implemented here) |

## Why Zero-Knowledge Proofs, concretely

The seminar's core privacy claim is "verify identity without exposing personal data." `src/zkp_schnorr.py` implements the **Schnorr identification protocol** — a well-known, textbook zero-knowledge proof: a citizen (prover) convinces a verifier they know the private key behind their registered DID, in three moves (commitment → challenge → response), without the private key or any personal data ever crossing the wire. It's the standard, honest way to demonstrate a ZKP concept in a student project rather than hand-waving it.

## Repo layout

```
blockchain-identity-management/
├── contracts/
│   ├── IdentityRegistry.sol   # on-chain DID registry (register / revoke / look up)
│   └── AccessControl.sol      # SSI-style consent: identity owner grants/revokes per-service access
├── src/
│   ├── did_registry.py        # DID + keypair generation (off-chain helper / client)
│   └── zkp_schnorr.py         # Schnorr ZKP: prove key ownership without revealing it
├── tests/
│   └── test_zkp_schnorr.py    # verifies the protocol actually holds (accepts valid, rejects forged)
├── docs/
│   └── consensus.md           # PoA/BFT design notes (slide 9-D)
└── requirements.txt
```

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest tests/
```

The Solidity contracts compile against Solidity ^0.8.20 (OpenZeppelin `Ownable`/`AccessControl` patterns). Use Remix, Hardhat, or Foundry to deploy to a testnet or local PoA network.

## Status

This is a from-scratch build based on the seminar's own architecture and base paper — not code copied from elsewhere. The ZKP and DID modules are real and tested (see `tests/`); the consensus layer is documented rather than reimplemented, since PoA/BFT consensus is a property of the chain you deploy to, not application code.
