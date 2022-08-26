// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;


interface StableSwap {
    function exchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external;
}


contract Interaction {
    address curvePoolAddr;
    event Exchange();

    function setCurvePoolAddr(address _poolAddr) public {
        curvePoolAddr = _poolAddr;
    }

    function getExchange(int128 i, int128 j, uint256 dx, uint256 min_dy) external payable {
        StableSwap(curvePoolAddr).exchange(i, j, dx, min_dy);
        emit Exchange();
    }
}
