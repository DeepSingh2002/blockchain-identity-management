// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title IdentityRegistry
/// @notice Slide 9-A/B: on-chain half of DID registration and decentralized
/// identity storage. Stores only a DID string and a public-key hash per
/// citizen — never personal data itself, in line with the seminar's
/// privacy-by-design argument (base paper: Padmanegara & Putri, 2023).
contract IdentityRegistry {
    struct DIDRecord {
        bytes32 publicKeyHash;   // keccak256 of the citizen's public key
        string did;              // e.g. "did:example:<hash>"
        uint256 registeredAt;
        bool revoked;
    }

    mapping(address => DIDRecord) private records;

    event IdentityRegistered(address indexed citizen, string did, uint256 timestamp);
    event IdentityRevoked(address indexed citizen, uint256 timestamp);

    error AlreadyRegistered(address citizen);
    error NotRegistered(address citizen);
    error AlreadyRevoked(address citizen);

    /// @notice Registers a new DID for msg.sender. Called once per citizen.
    function registerIdentity(string calldata did, bytes32 publicKeyHash) external {
        if (records[msg.sender].registeredAt != 0) revert AlreadyRegistered(msg.sender);

        records[msg.sender] = DIDRecord({
            publicKeyHash: publicKeyHash,
            did: did,
            registeredAt: block.timestamp,
            revoked: false
        });

        emit IdentityRegistered(msg.sender, did, block.timestamp);
    }

    /// @notice Revokes a citizen's own identity (e.g. on key compromise).
    function revokeIdentity() external {
        DIDRecord storage record = records[msg.sender];
        if (record.registeredAt == 0) revert NotRegistered(msg.sender);
        if (record.revoked) revert AlreadyRevoked(msg.sender);

        record.revoked = true;
        emit IdentityRevoked(msg.sender, block.timestamp);
    }

    function isValid(address citizen) external view returns (bool) {
        DIDRecord storage record = records[citizen];
        return record.registeredAt != 0 && !record.revoked;
    }

    function getDID(address citizen) external view returns (string memory) {
        if (records[citizen].registeredAt == 0) revert NotRegistered(citizen);
        return records[citizen].did;
    }
}
