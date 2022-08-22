// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";


// @TODO: use errors and revert instead of error messages

interface IClogMinter{
    function mint_clog(uint amount) external;
    function burn_clog(uint amount) external;
    event Minted(uint clogAmount);
    event Burned(uint clogAmount);
}

interface IClogStaking{
    function stakeTokens(uint _amount) external;
    function unstakeTokens(uint _amount) external;
    // event Staking(address owner, uint clogAmount, address sellToken, uint sellTokenAmount);
    // event Unstaked(address owner, uint clogAmount, address buyToken, uint buyTokenAmount);
    event Staking(address owner, uint clogAmount);
    event Unstaked(address owner, uint clogAmount);
}

interface ISabotTrader{
    function swap(address sellToken, uint sellTokenAmount, address buyToken) external;
    event SabotSwap(address indexed sellToken, uint sellTokenAmount, address buyToken, uint buyTokenAmount);
}


contract SabotStakingBase is ISabotTrader, IClogStaking, IClogMinter{
    uint public balance;
    constructor() {
    }

    function swap(address sellToken, uint sellTokenAmount, address buyToken)
    public{

        //TODO: IMPLEMENT
        uint buyTokenAmount = 42;
        balance += buyTokenAmount;

        // ----
        emit SabotSwap(sellToken,sellTokenAmount,buyToken,buyTokenAmount);
    }

    function mint_clog(uint amount) public{
        //TODO: IMPLEMENT

        // ----
        emit Minted(amount);
    }

    function burn_clog(uint amount) public{
        //TODO: IMPLEMENT

        // ----
        emit Burned(amount);
    }

    function stakeTokens(uint _amount) public{
        address owner = msg.sender;
        //TODO: IMPLEMENT

        // ----
        emit Staking(owner,_amount);
    }

    function unstakeTokens(uint _amount) public{
        address owner = msg.sender;
        //TODO: IMPLEMENT

        // ----
        emit Unstaked(owner,_amount);
    }

}


contract SabotStakingV1 is Initializable, AccessControlUpgradeable, UUPSUpgradeable, SabotStakingBase{
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize() initializer public {
        __AccessControl_init();
        __UUPSUpgradeable_init();

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyRole(UPGRADER_ROLE)
        override
    {}

}