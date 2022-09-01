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
    address public usdt_address;
    address public susd_address;
    address public pool_address;
    event Deployed(string name,address contract_address);
    constructor(
        uint256 initialAmount,
        address[] memory wallets_to_initialize
    ) {
        USDT usdt = new USDT(msg.sender,initialAmount, wallets_to_initialize);
        usdt_address=address(usdt);
        emit Deployed(usdt.name(),address(usdt));
        
        SUSD susd = new SUSD(msg.sender,0, new address[](0));
        susd_address=address(susd);
        emit Deployed(susd.name(),address(susd));


        CurvePool pool = new CurvePool();
        pool_address=address(pool);
        emit Deployed(pool.name(),address(pool));
    }
}
