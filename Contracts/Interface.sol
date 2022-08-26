// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

interface ICounter {
    function count() external view returns (uint);
    function increment() external; 
}

contract Interaction {
    address counterAddr;

    function setCounterAddr(address _counter) public payable {
        counterAddr = _counter;
    }

    function getCount() external view returns (uint) {
        return ICounter(counterAddr).count();
    }
 }