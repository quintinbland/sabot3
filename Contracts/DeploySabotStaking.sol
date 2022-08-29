// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "./ClogToken.sol";
import "./usdtToken.sol";
import "./SabotStakingV1.sol";
import "./SabotStakingProxy.sol";

contract DeploySabotStakingAssets{
    // The objective of this deployer is to easily deploy the following test assets:
    // Clog token
    // SabotStaking pool contract
    //    - base token address & index - USDT
    //    - target token address & index - sUSD
    //    - utility token address - CLOG
    //    - pool contract address
    //    - bot_wallet_address as SABOT_BOT_ROLE
    //    - owner as admin
    //    - CurvePool address
    bytes32 public constant DEFAULT_ADMIN_ROLE = 0x00;
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    event Deployed(string name,address contract_address);
    constructor(
        address bot_wallet_address,
        address base_token_address,
        address target_token_address,
        int128 base_token_index,
        int128 target_token_index,
        address curve_pool_address
        ).    
    {
        // create utility token instance 
        //set the SabotStaking contract as the Minter for this token
        Clog clog = new Clog();
        emit Deployed(clog.name(),address(clog));

        // in order for conversion algofithm to safely work, base token decimals must be < = utility token decimals
        require(clog.decimals() >= ERC20(base_token_address).decimals(),"Invalid token configuration.  Base token decimals must be less than or equal to utility token decimals.");

        // instantiate logic contract
        SabotStakingV1 logic_contract = new SabotStakingV1();

        // instantiate proxy contract, attaching it to the logix contract
        bytes memory data = new bytes(0);
        SabotStakingProxy proxy_contract = new SabotStakingProxy(address(logic_contract),data);

        // initialize proxy contract
        SabotStakingV1(address(proxy_contract)).initialize(
            bot_wallet_address,
            base_token_address,
            target_token_address,
            address(clog),
            curve_pool_address,
            base_token_index,
            target_token_index
        );
        // 333333333333333333
        // set utility token admin to the desginated owner address
        // set the minter to the sabotstaking contract address
        // and revoke these roles for the deployment contract address
        clog.grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        clog.grantRole(MINTER_ROLE, address(proxy_contract));
        clog.renounceRole(MINTER_ROLE,address(this));
        clog.renounceRole(DEFAULT_ADMIN_ROLE,address(this));

        // finally set sabotstaking admin and upgrader roles to the desginated owner address
        // and revoke these roles for the deployment contract address
        SabotStakingV1(address(proxy_contract)).grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        SabotStakingV1(address(proxy_contract)).grantRole(UPGRADER_ROLE, msg.sender);
        SabotStakingV1(address(proxy_contract)).renounceRole(UPGRADER_ROLE,address(this));
        SabotStakingV1(address(proxy_contract)).renounceRole(DEFAULT_ADMIN_ROLE,address(this));

        // indicate sabotstaking contract deployment is completed
        emit Deployed(SabotStakingV1(address(proxy_contract)).name(),address(proxy_contract));

    }
}