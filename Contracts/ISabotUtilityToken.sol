// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

// Sabot utility tokens are required to provide a mint and burn
// method and authorize the staking contract with the Minter role
// which should be the only role allowed to call these methods 
interface ISabotUtilityToken{
    function mint(address to, uint amount) external;
    function burn(address from, uint amount) external;
}