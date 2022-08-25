// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./openzeppelin/access/AccessControl.sol";
import "./openzeppelin/proxy/utils/Initializable.sol";
import "./openzeppelin/proxy/utils/UUPSUpgradeable.sol";

// @TODO: use errors and revert instead of error messages

interface IClogMinter{
    function mint_clog(address to, uint amount) external;
    function burn_clog(address from, uint amount) external;
    event Minted(uint clogAmount, address to);
    event Burned(uint clogAmount, address from);
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


contract SabotStakingBase is AccessControl, ISabotTrader, IClogStaking, IClogMinter {

    // for upgradeability - NEVER change the order of these variables
    //    also,             NEVER delete these 
    // Only append new ones in future contracts
    // -- defined in V1.0.0
    bytes32 public constant SABOT_BOT_ROLE = keccak256("SABOT_BOT_ROLE");
    bytes32 public constant CLOG_MINTER_ROLE = keccak256("CLOG_MINTER_ROLE");
    uint public balance;
    // -- end V1.0.0 definitions

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(SABOT_BOT_ROLE, msg.sender);
        _grantRole(CLOG_MINTER_ROLE, msg.sender);
    }

    function swap(address sellToken, uint sellTokenAmount, address buyToken)
    onlyRole(SABOT_BOT_ROLE)
    public
    {

        //TODO: IMPLEMENT
        uint buyTokenAmount = 42;
        balance += buyTokenAmount;

        // ----
        emit SabotSwap(sellToken,sellTokenAmount,buyToken,buyTokenAmount);
    }

    function mint_clog(address to, uint amount) 
    onlyRole(CLOG_MINTER_ROLE)
    public
    {
        //TODO: IMPLEMENT

        // ----
        emit Minted(amount, to);
    }

    function burn_clog(address from, uint amount)
    onlyRole(CLOG_MINTER_ROLE)
    public
    {
        //TODO: IMPLEMENT

        // ----
        emit Burned(amount, from);
    }

    function stakeTokens(uint _amount) 
    public
    {
        address owner = msg.sender;
        //TODO: IMPLEMENT

        // ----
        emit Staking(owner,_amount);
    }

    function unstakeTokens(uint _amount) 
    public
    {
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
        _grantRole(SABOT_BOT_ROLE, msg.sender);
        _grantRole(CLOG_MINTER_ROLE, msg.sender);

    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyRole(UPGRADER_ROLE)
        override
    {}

}