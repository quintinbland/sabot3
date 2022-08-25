// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

interface StableSwap {
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
}

contract CurvePool is StableSwap {
    event PoolSwap (int128 i, int128 j, uint256 dx, uint256 min_dy);

    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) public override {
        emit PoolSwap (i , j, dx, min_dy);
    }
}





// address constant STABLE_SWAP = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
// address constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
// address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
// address constant USDT = 0xdAC17F958D2ee523a2206206994597C13D831ec7;

// string[3] TOKENS = ["DAI", "USDC", "USDT"];

// mapping(address => string) public token;

// // function getValue(address _addr) public view returns (string[3] memory) {
// //     return (token[_addr]);
// // }

// function swap(uint256 i, uint256 j) public payable returns (string memory) {
//     address token = TOKENS[msg.sender][i];
//     uint256 bal = address(this).balance;

//     StableSwap(STABLE_SWAP).exchange( i, j, bal, 1);
// }

