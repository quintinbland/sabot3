// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract USDT is ERC20, Ownable {

    constructor(uint256 initialAmount, address[] memory addressesToInitialize) ERC20("sUSD", "SUSD") {
      for (uint8 i=0; i<addressesToInitialize.length; i++) {
            _mint(addressesToInitialize[i],initialAmount);
      }        
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) public onlyOwner {
        _burn(from, amount);
    }
}
