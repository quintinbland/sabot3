pragma solidity ^0.6.12;
interface IERC20 {
    function totalSupply() external view returns (uint);
    function balanceOf(address account) external view returns (uint);
    function transfer(address recipient, uint amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint);
    function approve(address spender, uint amount) external returns (bool);
    function transferFrom(
        address sender,
        address recipient,
        uint amount
    ) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, uint value);
}
contract SaBot_DAO {
    // call it DefiBank
    string public name = "SaBot DAO";
    // create 3 state variables
    address public usdt;
    address public susd;
    address public clog;
    address[] public stakers;
    mapping(address => uint) public stakingBalance;
    mapping(address => bool) public hasStaked;
    mapping(address => bool) public isStaking;
    // in constructor pass in the address for USDT token and your custom bank token
    // that will be used to pay interest
    constructor() public {
       // CLOG = INPUT-YOUR-TOKEN-ADDRESS-HERE;
       // USDT =
       // SUSD =
    }
    // allow user to stake usdc tokens in contract
    function stakeTokens(uint _amount) public {
        // Trasnfer usdc tokens to contract for staking
        IERC20(USDT).transferFrom(msg.sender, address(this), _amount);
        // REQUIRE USER HAS ENOUGH USDT
        // Update the staking balance in map
        //stakingBalance[msg.sender] = stakingBalance[msg.sender] + _amount;
        //MINT CLOG TOKEN BASED ON VALUE OF WHAT HAS BEEN STAKED
        // Initially on a 1:1 ratio, but then make it relate to the value of user's tokens in relation to total pool amount
        // The bot has a total portfolio value. The clog value is the outstanding supply of tokens divided by total portfolio value. Mint when we stake. Burn when we unstake.
        // if outstanding balance of CLOG is 0, then CLOG price = 1 . If outstanding supply of clog >0 then price of clog = portfolio value/outstanding CLOG supply
        //Outstanding supply | Portfolio Value | CLOG price
        //        0          |         0       |      1.00
        //      20,000       |     20,000USDT  |      1.00
        //      40,000       |     40,000USDT  |      1.00
        //     100,000       |    100,000USDT  |      1.00
        // After 1 year, and profitable trades
        //     100,000       |    300,000USDT  |      3.00
        // Other people enter the pool at this point
        //     150,000       |    450,000USDT  |      3.00
        //Opportunity for governance token that takes 3bps of all profit when unstaking.
        // Add user to stakers array if they haven't staked already
        //if(!hasStaked[msg.sender]) {
          //  stakers.push(msg.sender);
        //}
        // Update staking status to track
        //isStaking[msg.sender] = true;
        //hasStaked[msg.sender] = true;
        //EMIT MINTING EVENT
        //EMIT STAKING EVENT
    }
        // allow user to unstake total balance and withdraw USDC from the contract
     function unstakeTokens(uint _amount) public {
        // REQUIRE USER HAS ENOUGH CLOG
        // Trasnfer usdc tokens to contract for staking
        IERC20(CLOG).transferFrom(msg.sender, address(this), _amount);
        //If outstanding supply of clog >0 then price of clog = portfolio value/outstanding CLOG supply
        //Transfer CLOG price X CLOG amount in USDT to message.sender.  Make sure we have enough USDT to cover staking.
        // If we don't have enough USDT, we error out and tell them what is available to unstake.
        //BURN CLOG TOKEN BASED ON VALUE OF WHAT HAS BEEN STAKED
        // Initially on a 1:1 ratio, but then make it relate to the value of user's tokens in relation to total pool amount
        // The bot has a total portfolio value. The clog value is the outstanding supply of tokens divided by total portfolio value. Mint when we stake. Burn when we unstake.
        // if outstanding balance of CLOG is 0, then CLOG price = 1 . If outstanding supply of clog >0 then price of clog = portfolio value/outstanding CLOG supply
        //Outstanding supply | Portfolio Value | CLOG price
        //        0          |         0       |      1.00
        //      20,000       |     20,000USDT  |      1.00
        //      40,000       |     40,000USDT  |      1.00
        //     100,000       |    100,000USDT  |      1.00
        // After 1 year, and profitable trades
        //     100,000       |    300,000USDT  |      3.00
        // Other people enter the pool at this point
        //     150,000       |    450,000USDT  |      3.00
        //Opportunity for governance token that takes 3bps of all profit when unstaking.
        //EMIT BURN EVENT
        //EMIT UNSTAKING EVENT
    }
}

// helper methons
//function getClogPrice () public
 //   returns (UFixed256x18) {}

// function Need Outstanding supply
// function Get Portfolio Value

// NEXT TOPIC ----------------------------------------
// create struct SabotSwapResult{
//    bool swap_success,
//    uint buy_currency_amount
//}

//SaBot trader section
// function swap(sellToken address, sellToken amount, buyToken address) return (struct SabotSwapResult)
//    a sabot buy event is when sellToken is USDT
//    a sabot sell event is when sellToken is sUSD

//    This function will 
//      * check that there is enough sellToken balance available to do the swap
//      * call curve to execute the swap (is the gas fee to call the curve function(s) covered by the gas fee used to call this function?)
//      *   let's prototype this to determine how gas will be handled
//      * emit a swap even

// helper method
// get_balance(currency_address) // to get balance of USDT and sUSD

