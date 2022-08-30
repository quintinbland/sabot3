// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./usdtToken.sol";
import "./susdToken.sol";
import "./curvePool.sol";

contract DeployTestAssets{
    // The objective of this deployer is to easily deploy the following test assets:
    // USDT token
    //    also set the owner of the USDT Token to be the deployer for easy management
    // SUSD token
    //    also set the owner of the SUSD Token to be the deployer for easy management
    // CurvePool
    // starting USDT balance
    //    set up each of the provided wallet addresses with the specified amount of USDT 
    event Deployed(string name,address contract_address);
    constructor(
        uint256 initialAmount,
        address[] memory wallets_to_initialize
    ) {
        // Create a new instance of the KaseiCoin contract.
        USDT usdt = new USDT(msg.sender,initialAmount, wallets_to_initialize);
        emit Deployed(usdt.name(),address(usdt));
        
        SUSD susd = new SUSD(msg.sender,0, new address[](0));
        emit Deployed(susd.name(),address(susd));
 
        CurvePool pool = new CurvePool();
        emit Deployed(pool.name(),address(pool));
    }
}