// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;


interface ICurvePool {
    function exchange() external;
}

contract Interaction {
    address curvePoolAddr;

    function getCurvePoolAddr(address _poolAddr) public payable returns (address) {
        curvePoolAddr = _poolAddr;
        return curvePoolAddr;
    }

    function getExchange() external payable {
        return ICurvePool(curvePoolAddr).exchange();
    }
}
