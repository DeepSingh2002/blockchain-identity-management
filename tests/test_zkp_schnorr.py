"""Verifies the Schnorr ZKP protocol actually holds: a valid prover is
accepted, and a forged proof (no private key) is rejected."""
import secrets

from ecdsa import SECP256k1, SigningKey

from src.zkp_schnorr import ORDER, G, Proof, Prover, Verifier, run_identification


def test_valid_proof_is_accepted():
    sk = SigningKey.generate(curve=SECP256k1)
    assert run_identification(sk) is True


def test_forged_proof_without_private_key_is_rejected():
    # A forger who does NOT know the private key cannot produce a valid (R, s):
    # they'd have to solve the discrete log problem to do so.
    sk = SigningKey.generate(curve=SECP256k1)
    real_public_key = sk.get_verifying_key().pubkey.point
    verifier = Verifier(public_key=real_public_key)

    # Forger picks arbitrary R and s without knowledge of x.
    forged_s = secrets.randbelow(ORDER - 1) + 1
    forged_R = secrets.randbelow(ORDER - 1) * G

    forged_proof = Proof(R=forged_R, s=forged_s)
    challenge = verifier.challenge()

    assert verifier.verify(forged_proof, challenge) is False


def test_proof_is_not_reusable_nonce():
    sk = SigningKey.generate(curve=SECP256k1)
    prover = Prover(sk)
    prover.commit()
    prover.respond(challenge=5)
    # nonce is cleared after use — calling respond() again without a fresh
    # commit() must fail loudly rather than silently reuse r (which would
    # leak the private key across two challenges).
    try:
        prover.respond(challenge=7)
        assert False, "expected RuntimeError on nonce reuse"
    except RuntimeError:
        pass
