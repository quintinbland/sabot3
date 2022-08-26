// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

// @TODO: use errors and revert instead of error messages

interface IClogMinter{
    function mint_clog(address to, uint256 amount) external;
    function burn_clog(address from, uint256 amount) external;
}

interface IClogStaking{
    function stakeTokens(uint256 _amount) external;
    function unstakeTokens(uint256 _amount) external;
    event Staking(address owner, address sellToken, uint256 sellTokenAmount, uint256 clogAmount);
    event Unstaked(address owner, address buyToken, uint256 buyTokenAmount, uint256 clogAmount);
    event Minted(uint256 clogAmount, address owner, uint clogSupply);
    event Burned(uint256 clogAmount, address owner, uint clogSupply);
}

interface ISabotTrader{
    function swap(address sellToken, uint256 sellTokenAmount, address buyToken) external;
    event SabotSwap(address indexed sellToken, uint256 sellTokenAmount, address buyToken, uint256 buyTokenAmount);
}

interface StableSwap {
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
}

contract SabotStakingBase is AccessControlUpgradeable, ISabotTrader, IClogStaking, IClogMinter {

    // for upgradeability - NEVER change the order of these variables
    //    also,             NEVER delete these 
    // Only append new ones in future contracts
    // -- defined in V1.0.0
    bytes32 public constant SABOT_BOT_ROLE = keccak256("SABOT_BOT_ROLE");
    bytes32 public constant CLOG_MINTER_ROLE = keccak256("CLOG_MINTER_ROLE");
    uint public balance;
    address curvePoolAddr;
    mapping(address => int128) poolCoinIndex;
    address stakingToken;
    address clogToken;
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
        int128 i = poolCoinIndex[sellToken];
        int128 j = poolCoinIndex[buyToken];
        uint256 dx = sellTokenAmount;
        uint256 min_dy = 1;
        StableSwap(curvePoolAddr).exchange(i, j, dx, min_dy);
        // ----
        emit SabotSwap(sellToken,sellTokenAmount,buyToken,buyTokenAmount);
    }

    function mint_clog(address to, uint amount) 
    onlyRole(CLOG_MINTER_ROLE)
    public
    {
        //TODO: IMPLEMENT
        uint256 clogSupply = IERC20(clogToken).totalSupply();
        // ----
        emit Minted(amount, to, clogSupply);
    }

    function burn_clog(address from, uint amount)
    onlyRole(CLOG_MINTER_ROLE)
    public
    {
        //TODO: IMPLEMENT
        uint256 clogSupply = IERC20(clogToken).totalSupply();
        // ----
        emit Burned(amount, from, clogSupply);
    }

    function stakeTokens(uint256 _amount) 
    public
    {
        address owner = msg.sender;
        //TODO: IMPLEMENT
        uint256 clogAmount = _amount;
        // ----
        emit Staking(owner,stakingToken,_amount,clogAmount);
    }

    function unstakeTokens(uint256 clogAmount) 
    public
    {
        address owner = msg.sender;
        //TODO: IMPLEMENT
        uint256 buyTokenAmount = clogAmount;
        // ----
        emit Unstaked(owner,stakingToken,buyTokenAmount,clogAmount);
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