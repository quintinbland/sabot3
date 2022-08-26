// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

contract Counter {
    uint public count;

    function increment() external {
        count += 1;
    }

}