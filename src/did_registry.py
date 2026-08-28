"""Slide 9-A: Identity Registration & Verification.

Generates a decentralized digital ID (DID) for a citizen: an EC keypair plus
a DID string derived by hashing the public key. This is the off-chain half
of registration — the DID document (public key + metadata) is what actually
gets written to `IdentityRegistry.sol` on-chain; the private key never
leaves the citizen's device.
"""
from __future__ import annotations

import hashlib
import json
import secrets
from dataclasses import asdict, dataclass

from ecdsa import SECP256k1, SigningKey


@dataclass
class DIDDocument:
    did: str
    public_key_hex: str
    method: str = "did:example:secp256k1"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)


@dataclass
class Identity:
    """Holds both halves; only `document` (no private key) should ever be
    serialized or sent anywhere."""
    private_key: SigningKey
    document: DIDDocument


def generate_identity() -> Identity:
    """Creates a fresh public/private key pair and derives a DID from the
    public key, mirroring 'The system generates a decentralized digital ID
    (DID) secured via cryptographic hashing. A public-private key pair is
    created for authentication.' (seminar, slide 9-A)."""
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    public_key_bytes = vk.to_string()
    public_key_hex = public_key_bytes.hex()

    did_hash = hashlib.sha256(public_key_bytes).hexdigest()
    did = f"did:example:{did_hash}"

    return Identity(private_key=sk, document=DIDDocument(did=did, public_key_hex=public_key_hex))


def random_nonce(n_bytes: int = 32) -> int:
    """Cryptographically secure nonce, used by the Schnorr ZKP protocol."""
    return secrets.randbits(n_bytes * 8)


if __name__ == "__main__":
    identity = generate_identity()
    print("Generated DID document (safe to publish on-chain):")
    print(identity.document.to_json())
