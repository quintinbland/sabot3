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

    event Deployed(string name,address contract_address);
    constructor(
        string memory version,
        address bot_wallet_address,
        address base_token_address,
        address target_token_address,
        int128 base_token_index,
        int128 target_token_index,
        address curve_pool_address
        )
    {


        // --- begin section for upgradable deployment
        // // instantiate logic contract
        // SabotStakingV1 logic_contract = new SabotStakingV1();
        // address logic_contract_address = address(logic_contract);
        // // string memory logic_label = "SabotStakingLogic";
        // // emit Deployed(logic_label,logic_contract_address);

        // // instantiate proxy contract, attaching it to the logix contract
        // bytes memory data = new bytes(0);
        // SabotStakingProxy proxy_contract = new SabotStakingProxy(logic_contract_address,data);
        // address proxy_contract_address = address(proxy_contract);
        // // string memory proxy_label = "SabotStakingProxy";
        // // emit Deployed(proxy_label,proxy_contract_address);

        // // initialize proxy contract
        // SabotStakingV1(proxy_contract_address).initialize(
        //     version,
        //     bot_wallet_address,
        //     base_token_address,
        //     target_token_address,
        //     curve_pool_address,
        //     base_token_index,
        //     target_token_index
        // );
        // --- end section for upgradable deployment

        // --- begin section for static deployment
        SabotStakingV1 logic_contract = new SabotStakingV1(
            version,
            bot_wallet_address,
            base_token_address,
            target_token_address,
            curve_pool_address,
            base_token_index,
            target_token_index
        );
        address proxy_contract_address = address(logic_contract);
        // --- end section for static deployment

        // create utility token instance and set the SabotStaking contract as the Minter for this token
        Clog clog = new Clog(msg.sender, proxy_contract_address);
        address utility_token_address = address(clog);
        emit Deployed(clog.name(),utility_token_address);

        // now that the utility token is available, set the utility token in the staking contract to complete
        // staking contract set up
        SabotStakingV1(proxy_contract_address).setUtilityToken(utility_token_address);

        // finally set sabotstaking admin and upgrader roles to the desginated owner address
        // and revoke these roles for the deployment contract address
        SabotStakingV1(proxy_contract_address).grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        SabotStakingV1(proxy_contract_address).grantRole(UPGRADER_ROLE, msg.sender);
        SabotStakingV1(proxy_contract_address).renounceRole(UPGRADER_ROLE,address(this));
        SabotStakingV1(proxy_contract_address).renounceRole(DEFAULT_ADMIN_ROLE,address(this));

        // indicate sabotstaking contract deployment is completed
        emit Deployed(SabotStakingV1(proxy_contract_address).name(),proxy_contract_address);

    }
}