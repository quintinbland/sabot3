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