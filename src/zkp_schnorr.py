"""Slide 9-B: Zero-Knowledge Proofs — verify identity without exposing personal data.

A textbook Schnorr identification protocol over SECP256k1. The citizen
(Prover) proves they hold the private key behind their registered DID,
without ever revealing that private key to the verifying service.

Protocol (3 moves):
    1. Commitment — Prover picks random r, sends R = r*G
    2. Challenge  — Verifier sends random challenge c
    3. Response   — Prover sends s = r + c*x  (x = private key)
    Verifier accepts iff s*G == R + c*PublicKey
"""
from __future__ import annotations

from dataclasses import dataclass

from ecdsa import SECP256k1, SigningKey
from ecdsa.ellipticcurve import Point

CURVE = SECP256k1
ORDER = CURVE.order
G = CURVE.generator


@dataclass
class Commitment:
    R: Point


@dataclass
class Proof:
    R: Point
    s: int


class Prover:
    """Holds the private key. Nothing here is ever transmitted except R and s."""

    def __init__(self, signing_key: SigningKey):
        self._x = signing_key.privkey.secret_multiplier  # private scalar, stays local
        self.public_key: Point = signing_key.get_verifying_key().pubkey.point
        self._r: int | None = None

    def commit(self) -> Commitment:
        import secrets
        self._r = secrets.randbelow(ORDER - 1) + 1
        R = self._r * G
        return Commitment(R=R)

    def respond(self, challenge: int) -> Proof:
        if self._r is None:
            raise RuntimeError("commit() must be called before respond()")
        s = (self._r + challenge * self._x) % ORDER
        commitment_R = self._r * G
        self._r = None  # single-use nonce — never reuse
        return Proof(R=commitment_R, s=s)


class Verifier:
    """Never sees the private key or any personal data — only public
    keys, curve points, and integers."""

    def __init__(self, public_key: Point):
        self.public_key = public_key

    def challenge(self) -> int:
        import secrets
        return secrets.randbelow(ORDER - 1) + 1

    def verify(self, proof: Proof, challenge: int) -> bool:
        lhs = proof.s * G
        rhs = proof.R + challenge * self.public_key
        return lhs == rhs


def run_identification(signing_key: SigningKey) -> bool:
    """End-to-end demo of one proof round. Returns True iff the verifier
    accepts — i.e. the prover demonstrably owns the DID's private key
    without that key (or any personal data) ever being sent."""
    prover = Prover(signing_key)
    verifier = Verifier(public_key=prover.public_key)

    commitment = prover.commit()
    c = verifier.challenge()
    proof = prover.respond(c)

    assert proof.R == commitment.R
    return verifier.verify(proof, c)


if __name__ == "__main__":
    from ecdsa import SigningKey as _SK

    sk = _SK.generate(curve=SECP256k1)
    accepted = run_identification(sk)
    print(f"Verifier accepted proof of DID ownership: {accepted}")
