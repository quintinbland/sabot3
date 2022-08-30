// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./ISabotUtilityToken.sol";

// This interface is created so that we can call the exchange method of the Curve pool
// i is the index in the pool of the token we are exchanging in (sellToken)
// j is the index in the pool of the tolen we are exchanging for (buyToken)
// dx is the amount of i we are exchanging
// min_dy is the minimum. amount of j we require or the exchange will be reverted.
interface StableSwap {
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
    function setExchangeRate(uint256 exchangeRate) external;
}

// This interfact defines the staking related functions 
// that the staking contract must implement 
// and staking related events
interface IClogStaking{
    function stakeTokens(uint256 _amount, address token) external;
    function unstakeTokens(uint256 _amount, address token) external;

    event Staked(
        address indexed sellToken, address indexed utilityToken, address indexed owner, 
        uint256 sellTokenAmount, uint256 utilityTokenAmount, uint256 utilityTokenTotalSupply, 
        uint256 balanceOfBaseToken, uint256 balanceOfTargetToken);
    event Unstaked(
        address indexed buyToken, address indexed utilityToken, address indexed owner, 
        uint256 buyTokenAmount, uint256 utilityTokenAmount, uint256 utilityTokenTotalSupply, 
        uint256 balanceOfBaseToken, uint256 balanceOfTargetToken);
    event Minted(address owner, address utilityToken, uint256 utilityTokenAmount);
    event Burned(address owner, address utilityToken, uint256 utilityTokenAmount);
}

// This interfact defines the sabot trader related function
// that the staking contract must implement 
// this function must be restricted such that only the 
// SABOT_BOT_ROLE is allowed to call this method
// as well as the related event
// In addition, we are our own oracle, on every trade decision, set exchangeRate
interface ISabotTrader{
    // use swap when making a trade
    function swap(address sellToken, uint256 sellTokenAmount, address buyToken, uint256 exchangeRate) external;
    // use setExchangeRate when not making a trade
    function setExchangeRate(uint256 exchangeRate) external;
    event Swapped(
        address indexed sellToken, address indexed buyToken, address indexed utilityToken, 
        uint256 sellTokenAmount, uint256 utilityTokenTotalSupply, uint256 balanceOfBaseToken, uint256 balanceOfTargetToken);
    event ExchangeRate(
        address indexed sellToken, address indexed utilityToken, uint256 exchangeRate);
}

contract SabotStakingBase is AccessControlUpgradeable, ISabotTrader, IClogStaking {
    // for upgradeability - NEVER change the order of these variables
    //    also,             NEVER delete these 
    // Only append new ones in future contracts
    // -- defined in V1.0.0
    bytes32 public constant SABOT_BOT_ROLE = keccak256("SABOT_BOT_ROLE");
    string public name;
    string public version;
    address public utilityToken;
    address public baseToken;
    address public targetToken;
    address public curvePoolAddr;
    uint256 public exchangeRate;
    mapping(address => int128) poolTokenIndex;

    // -- end V1.0.0 definitions

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(SABOT_BOT_ROLE, msg.sender);
    }

    // This method functions as an oracle and sends exchange rate on chain to our contract
    function setExchangeRate(uint256 _exchangeRate)
    onlyRole(SABOT_BOT_ROLE)
    public
    {
        exchangeRate=_exchangeRate;
        emit ExchangeRate(baseToken, utilityToken, exchangeRate);
    }

    // This method functions as an oracle and sends exchange rate on chain to our contract
    // in addition to communicating swap instruction
    function swap(address sellToken, uint sellTokenAmount, address buyToken, uint256 _exchangeRate)
    onlyRole(SABOT_BOT_ROLE)
    public
    {
        // delegte to setExchangeRate
        setExchangeRate(_exchangeRate);
        // then process swap instruction

        // retrieve the pool indexes for each token
        int128 i = poolTokenIndex[sellToken];
        int128 j = poolTokenIndex[buyToken];

        // execute swap using desingated liquidity pool
        StableSwap(curvePoolAddr).exchange(i, j, sellTokenAmount, 1);

        emit Swapped(
            sellToken, buyToken, utilityToken, sellTokenAmount,
            ERC20(utilityToken).totalSupply(),ERC20(baseToken).balanceOf(address(this)),
            ERC20(targetToken).balanceOf(address(this))
        );
    }

    function mint_clog(address to, uint amount) 
    internal
    {
        // this contract is permitted to mint the utility token
        ISabotUtilityToken(utilityToken).mint(to, amount);
        emit Minted(to, utilityToken, amount);
    }

    function burn_clog(address from, uint amount)
    internal
    {
        // this contract is permitted to burn the utility token
        ISabotUtilityToken(utilityToken).burn(from, amount);
        emit Burned(from, utilityToken, amount);
    }

    function stakeTokens(uint256 baseTokenAmount, address token) 
    public
    {
        // This interface allows participants to stake base tokens in exchange for
        // utility tokens
        require(token == baseToken,append3("only ", ERC20(baseToken).name(), " tokens can be staked"));
        ERC20(baseToken).transferFrom(msg.sender,address(this), baseTokenAmount);
        uint256 utilityTokenAmount = convertBaseTokenToUtilityToken(baseTokenAmount);
        mint_clog(msg.sender,utilityTokenAmount);

        emit Staked(
            token, utilityToken, msg.sender, baseTokenAmount, utilityTokenAmount,
            ERC20(utilityToken).totalSupply(),ERC20(baseToken).balanceOf(address(this)),
            ERC20(targetToken).balanceOf(address(this)));
    }

    function unstakeTokens(uint256 utilityTokenAmount, address token) 
    public
    {
        // This interface allows participant to unstake utility tokens in exchange 
        // for base tokens
        require(token == utilityToken,append3("only ", ERC20(utilityToken).name(), " tokens can be unstaked"));
        uint256 buyTokenAmount = convertUtilityTokenToBaseToken(utilityTokenAmount);
        ERC20(baseToken).transfer(msg.sender,buyTokenAmount);
        burn_clog(msg.sender, utilityTokenAmount);

        emit Unstaked(
            baseToken, utilityToken, msg.sender, buyTokenAmount, utilityTokenAmount,
            ERC20(utilityToken).totalSupply(),ERC20(baseToken).balanceOf(address(this)),
            ERC20(targetToken).balanceOf(address(this)));
    }

    function convertBaseTokenToUtilityToken(uint256 baseTokenAmount) internal view returns(uint256){
        // the exchangeRate rate represents how many utility tokens expressed in utility token decimals
        // can be purchased for the nominal representation of the base token.
        // 
        // the nominal reresentation of the base token is 1*10**(token decimal)
        // for USDT, which has a decimal of 6, the exchange rate
        //           represents how many utility tokens expressed in the utility token decimal scale
        //           one receives when giving 1000000 (equivalently i USDT)
        // for eth, which has a decimal of 18, the exchange rate
        //           represents how many utility tokens expressed in the utility token decimal scale
        //           one receives when giving 1000000000000000000 (equivalently i eth)
        // Examples:
        // if the base token decimal is 6
        // if the utility token decimal is 12
        // if the decimal conversation rate is 1.25, meaning that one would receive 1.25 utility tokens for 1 base token
        // the exchange rate will be int(1.25 * 10**(base token decimal) * 10**(utility token decimal - base token decimal))
        //                           int(1.25 * 10 **(base token decimal + utility token decimal - base token decimal))
        //                           int(1.25  * 19 **(utility token decimal))
        //                  exchangeRate=1250000000000
        // 
        // The setup is constrained to require that utility tokens decimals >= base token decimals
        // 
        // step 1 - divide exchange rate by base token decimals: e.g. 1.25 * 10^12 / 10^6 , this keeps as much of the precision as possible
        // step 2 - multiply result from step 1 by base token amount: e.g.  1.25 * 10^6 * 42 * 10^6
        // 
        // The order of the math operations is to increase precision while reducing risk of overflow
        uint256 utilityTokenAmount = 
            SafeMath.mul(
                SafeMath.div(exchangeRate,10**ERC20(baseToken).decimals()),
                baseTokenAmount);
        return utilityTokenAmount;
    }

    function convertUtilityTokenToBaseToken(uint256 utilityTokenAmount) internal view returns(uint){
        // the exchangeRate is explained above
        // the nominal reresentation of the base token is 1*10**(token decimal)
        // 
        // The setup is constrained to require that utility tokens decimals >= base token decimals
        // 
        // step 1 - multiply base token decimals by utilityTokenAmount : e.g. 10^6 * 42 * 10^12, this keeps as much of the precision as possible
        // step 2 - multiply result from step 1 by base token amount: e.g.  42 * 10^18 / 1.25 * 10^12
        // 
        // 
        // The order of the math operations is to increase precision while reducing risk of overflow
        uint256 baseTokenAmount = 
            SafeMath.div(
                SafeMath.mul(10**ERC20(baseToken).decimals(),utilityTokenAmount),
                exchangeRate);
        return baseTokenAmount;
    }

    function _makeName() internal{
        string memory label="Sabot v";
        string memory delim1=" : ";
        string memory delim2=" ==> ";
        string memory delim3=" | ";
        name = append8(label,version,delim1,
                ERC20(baseToken).name(),delim2,ERC20(targetToken).name(),
                delim3,ERC20(utilityToken).name());
    }

    function append8(
        string memory a, string memory b, string memory c, string memory d,
        string memory e, string memory f, string memory g, string memory h) internal pure returns (string memory) {

        return string(abi.encodePacked(a, b, c, d, e, f, g, h));
    }   

    function append3(
        string memory a, string memory b, string memory c) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b, c));
    }   

}

contract SabotStakingV1 is Initializable, AccessControlUpgradeable, UUPSUpgradeable, SabotStakingBase{
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        version = '0.1.0';
        _disableInitializers();
    }

    function initialize(
        address botWalletAddress, 
        address _baseToken, address _targetToken, address _utilityToken,
        address _curvePoolAddr, int128 baseTokenIndex, int128 targetTokenIndex) initializer public {
        baseToken=_baseToken;
        targetToken=_targetToken;
        utilityToken=_utilityToken;
        curvePoolAddr = _curvePoolAddr;
        _makeName();

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
        _grantRole(SABOT_BOT_ROLE, botWalletAddress);

        poolTokenIndex[baseToken]=baseTokenIndex;
        poolTokenIndex[targetToken]=targetTokenIndex;   

        exchangeRate=10**ERC20(_utilityToken).decimals();  //initial exchange rate is 1 base token nominal value for 1 utility token nominal value
    }

    function _authorizeUpgrade(address newImplementation)
        internal
        onlyRole(UPGRADER_ROLE)
        override
    {}

}

