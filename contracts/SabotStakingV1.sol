// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

// import "@openzeppelin/contracts-upgradeable/access/AccessControlUpgradeable.sol";
// import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
// import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


// This interface is created so that we can call the exchange method of the Curve pool
interface StableSwap {
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
}

// move to separate file.  All Sabot utility tokens must implement this
interface ISabotUtilityToken{
    function mint(address to, uint amount) external;
    function burn(address from, uint amount) external;
}
// @ TODO update clog class diagram

interface IClogStaking{
    function stakeTokens(uint256 _amount, address token) external;
    function unstakeTokens(uint256 _amount, address token) external;
    function getPortfolioValue() external view returns(uint);

    event Staked(address owner, address sellToken, uint256 sellTokenAmount, address utilityToken, uint256 utilityTokenAmount);
    event Unstaked(address owner, address buyToken, uint256 buyTokenAmount, address utilityToken, uint256 utilityTokenAmount);
    event Minted(address owner, address utilityToken, uint256 utilityTokenAmount);
    event Burned(address owner, address utilityToken, uint256 utilityTokenAmount);
}

interface ISabotTrader{
    function swap(address sellToken, uint256 sellTokenAmount, address buyToken) external;
    event Swapped(address indexed sellToken, uint256 sellTokenAmount, address buyToken);
}


//contract SabotStakingBase is AccessControlUpgradeable, ISabotTrader, IClogStaking {

contract SabotStakingBase is AccessControl, ISabotTrader, IClogStaking {

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
    mapping(address => int128) poolTokenIndex;

    // -- end V1.0.0 definitions

    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(SABOT_BOT_ROLE, msg.sender);
    }

    function swap(address sellToken, uint sellTokenAmount, address buyToken)
    onlyRole(SABOT_BOT_ROLE)
    public
    {
        int128 i = poolTokenIndex[sellToken];
        int128 j = poolTokenIndex[buyToken];
        uint256 dx = sellTokenAmount;
        uint256 min_dy = 1;

        StableSwap(curvePoolAddr).exchange(i, j, dx, min_dy);
        emit Swapped(sellToken,sellTokenAmount,buyToken);
    }

    function mint_clog(address to, uint amount) 
    internal
    {
        ISabotUtilityToken(utilityToken).mint(to, amount);
        emit Minted(to, utilityToken, amount);
    }

    function burn_clog(address from, uint amount)
    internal
    {
        ISabotUtilityToken(utilityToken).burn(from, amount);
        emit Burned(from, utilityToken, amount);
    }

    function stakeTokens(uint256 _amount, address token) 
    public
    {
        require(token == baseToken,string.concat("only ", ERC20(baseToken).name(), " tokens can be staked"));
        // add requires
        ERC20(baseToken).transferFrom(msg.sender,address(this),_amount);
        uint256 utilityTokenAmount = convertBaseTokenToUtilityToken(_amount);
        mint_clog(msg.sender,utilityTokenAmount);
        emit Staked(msg.sender,token,_amount,utilityToken, utilityTokenAmount);
    }

    function unstakeTokens(uint256 _amount, address token) 
    public
    {
        require(token == baseToken,string.concat("only ", ERC20(baseToken).name(), " tokens can be unstaked"));
        // add a require that calculates how much USDT can be unstaked based on clog price
        ERC20(baseToken).transfer(msg.sender,_amount);
        uint256 utilityTokenAmount = convertBaseTokenToUtilityToken(_amount);
        // require enough utility tokens to unstake
        burn_clog(msg.sender,utilityTokenAmount);
        // ----
        emit Unstaked(msg.sender,token,_amount, utilityToken, utilityTokenAmount);
    }

    function convertBaseTokenToUtilityToken(uint baseTokenAmount) internal pure returns(uint){
        // TODO define conversion rate process and use safemath and ensure everything is properly casted
        uint rate = 1;
        return baseTokenAmount * rate;
    }

    function setUtilityToken(address token) public onlyRole(DEFAULT_ADMIN_ROLE){
        utilityToken=token;
        _makeName();
    }

    function _makeName() internal{
        string memory label="Sabot v";
        string memory delim1=" : ";
        string memory delim2=" ==> ";
        string memory delim3=" | ";
        name = append(label,version,delim1,
                ERC20(baseToken).name(),delim2,ERC20(targetToken).name(),
                delim3,ERC20(utilityToken).name());
    }

    function append(
        string memory a, string memory b, string memory c, string memory d,
        string memory e, string memory f, string memory g, string memory h) internal pure returns (string memory) {

        return string(abi.encodePacked(a, b, c, d, e, f, g, h));
    }   

    function getPortfolioValue() public view returns(uint) {
        // TODO: get on chain ethbased pricing for each token and back calculate true normalized value of each
        //       and sum for portfolio value

        // Simplification for class project:  portolio value is roughly the sum of the balances of each stable coin since
        // these are stable coins pegged to 1 USD
        uint baseTokenAmount = ERC20(baseToken).balanceOf(address(this));
        uint targetTokenAmount = ERC20(targetToken).balanceOf(address(this));
        // With the simplification
        //TODO refactor using safemath
        return baseTokenAmount + targetTokenAmount;
    }
}

// temporary non upgrable version
contract SabotStakingV1 is AccessControl, SabotStakingBase{
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor(
        string memory _version, address botWalletAddress, 
        address _baseToken, address _targetToken,
        address _curvePoolAddr, int128 baseTokenIndex, int128 targetTokenIndex) {
        // _disableInitializers();
        version = _version;
        baseToken=_baseToken;
        targetToken=_targetToken;
        curvePoolAddr = _curvePoolAddr;

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(UPGRADER_ROLE, msg.sender);
        _grantRole(SABOT_BOT_ROLE, botWalletAddress);

        poolTokenIndex[baseToken]=baseTokenIndex;
        poolTokenIndex[targetToken]=targetTokenIndex;   
    }

}

// contract SabotStakingV1 is Initializable, AccessControlUpgradeable, UUPSUpgradeable, SabotStakingBase{
//     bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

//     /// @custom:oz-upgrades-unsafe-allow constructor
//     constructor() {
//         _disableInitializers();
//     }

//     function initialize(
//         string memory _version, address botWalletAddress, 
//         address _baseToken, address _targetToken,
//         address _curvePoolAddr, int128 baseTokenIndex, int128 targetTokenIndex) initializer public {
//             version = _version;
//             baseToken=_baseToken;
//             targetToken=_targetToken;
//             curvePoolAddr = _curvePoolAddr;

//             __AccessControl_init();
//             __UUPSUpgradeable_init();

//             _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
//             _grantRole(UPGRADER_ROLE, msg.sender);
//             _grantRole(SABOT_BOT_ROLE, botWalletAddress);

//             poolTokenIndex[baseToken]=baseTokenIndex;
//             poolTokenIndex[targetToken]=targetTokenIndex;   

//     }

//     function _authorizeUpgrade(address newImplementation)
//         internal
//         onlyRole(UPGRADER_ROLE)
//         override
//     {}

// }