// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

interface IClogMinter{
    function mint_clog(uint amount) external;
    function burn_clog(uint amount) external;
    event Minted(uint clogAmount);
    event Burned(uint clogAmount);
}

interface IClogStaking{
    function stakeTokens(uint _amount) external;
    function unstakeTokens(uint _amount) external;
    event Staking(address owner, uint clogAmount, address sellToken, uint sellTokenAmount);
    event Unstaked(address owner, uint clogAmount, address buyToken, uint buyTokenAmount);
}

interface ISabotTrader{
    struct SabotSwapResult { 
        bool swapExecuted;
        uint amount;
    }
    function swap(address sellToken, uint sellTokenAmount, address buyToken) external returns (SabotSwapResult memory result);
    event SabotSwap(address indexed sellToken, uint sellTokenAmount, address buyToken, uint buyAmount, bool swapExecuted);
}

/// @custom:security-contact admin@sabot.com
contract SabotStaking is Initializable, PausableUpgradeable, AccessControlUpgradeable, UUPSUpgradeable {
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize() initializer public {
        __Pausable_init();
        __AccessControl_init();
        __UUPSUpgradeable_init();

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyRole(UPGRADER_ROLE)
        override
    {}
}
