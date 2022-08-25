// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

// deployment wallet == multi_sig wallet

interface IClogMinter{
    function mint_clog(address to, uint amount) external;
    function burn_clog(address from, uint amount) external;
    event Minted(uint clogAmount, address to);
    event Burned(uint clogAmount, address from);
}

interface IClog {
function mint(address to, uint256 amount) external;
function burn(address from, uint256 amount) external;
}


contract ClogMinter is IClogMinter {
    address _ClogToken;
    constructor(address ClogToken) {
        _ClogToken = ClogToken;
    }

    function mint_clog(address to, uint256 amount) public {
        IClog(_ClogToken).mint(to, amount);
        emit Minted(amount, to);
    }

    function burn_clog(address from, uint256 amount) public {
        IClog(_ClogToken).burn(from, amount);
        emit Burned(amount, from);
    }
}