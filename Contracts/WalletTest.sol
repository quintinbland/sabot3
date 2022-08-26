// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./SabotStakingV1.sol";

contract WalletTest is ISabotTrader{

    uint buyTokenAmount;    
    
    constructor() {
        buyTokenAmount=42;
    }

    function swap(address sellToken, uint sellTokenAmount, address buyToken)
    public
    {
        emit SabotSwap(sellToken,sellTokenAmount,buyToken,buyTokenAmount);
    }
}