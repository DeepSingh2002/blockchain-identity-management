// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "./IdentityRegistry.sol";

/// @title SelfSovereignAccessControl
/// @notice Slide 9-C: smart-contract-based identity authentication under
/// self-sovereign identity (SSI) principles — the citizen, not a central
/// authority, decides which services may verify their identity, and can
/// revoke that consent at any time.
contract SelfSovereignAccessControl {
    IdentityRegistry public immutable registry;

    // citizen => service => consent granted
    mapping(address => mapping(address => bool)) private consents;

    event AccessGranted(address indexed citizen, address indexed service, uint256 timestamp);
    event AccessRevoked(address indexed citizen, address indexed service, uint256 timestamp);

    error IdentityNotValid(address citizen);

    constructor(address registryAddress) {
        registry = IdentityRegistry(registryAddress);
    }

    modifier onlyValidIdentity() {
        if (!registry.isValid(msg.sender)) revert IdentityNotValid(msg.sender);
        _;
    }

    /// @notice Citizen grants a specific service (e.g. a bank doing KYC)
    /// permission to verify their identity.
    function grantAccess(address service) external onlyValidIdentity {
        consents[msg.sender][service] = true;
        emit AccessGranted(msg.sender, service, block.timestamp);
    }

    /// @notice Citizen revokes previously granted access — core SSI
    /// guarantee: consent is always reversible by the identity owner.
    function revokeAccess(address service) external onlyValidIdentity {
        consents[msg.sender][service] = false;
        emit AccessRevoked(msg.sender, service, block.timestamp);
    }

    /// @notice A service calls this to check whether it may currently
    /// authenticate a given citizen.
    function hasAccess(address citizen, address service) external view returns (bool) {
        return registry.isValid(citizen) && consents[citizen][service];
    }
}
