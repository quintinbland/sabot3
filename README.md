# SabotStaking Pool
The SabotStaking Pool is a configurable fit for purpose defi pool aimed at accelerating the implementation of automated cryptocurrency arbitrage trading strategies.
The solution consists of a set of coordinated web3 applications and smart contracts that are designed to 
* secure participant assets
* prevent risk of fraud, rug pulls and other nefarious actions
* minimize transaction costs through on-chain trading
* scale to support the demands of large defi solutions

### Tech
* wizard.openzeppelin.com - An online wizard provided by OpenZeppelin that creates contract skeleton based on advanced feature selections.

## Solution Design
The following scenarios were generated to drive out the critical design aspects and dependencies.

### Scenario - Staking
#### Objective
Allow participant to stake a certain amount of USDT and receive CLOG in return.  This is done through our SabotStaking UI.
#### Prerequisites
* Participant has wallet
* Participant has available USDT to stake
* SabotStaking smart contract is deployed
* UI has SabotStaking contract address and ABI
* SabotStaking smart contract is authorized as the MINTER_ROLE for CLOG
#### Requirements
* Participant connects their wallet by entering wallet address into the address text field
* UI connects the wallet
* Participant enters the amount of USDT they want to stake
* Participant clicks on the stake button to execute the stake
* UI effects a transfer of USDT from the participants wallet to the SabotStaking smart contract
* SabotStaking smart contract mints an amount of CLOG proportional to the amount of USDT that was staked
* SabotStaking smart contract assigns the minted CLOG to the wallet that staked the USDT
* SabotStaking smart contract emits an event that indicates staking occurred
* UI confirms swap has occured by looking at the transaction receipt and confirming that the Staking event exists and indicates the amount of CLOG received from the staking.
#### Verification
* Participant wallet USDT balance is decremented by the amount that was staked
* Participant wallet CLOG balance is increased by an amount proportional to what was staked
* SabotStaking smart contract USDT balance is increased by the amount that was staked.

### Scenario - Arbitrage Trading
#### Objective
The bot is able to send trade orders to the StakingSmart contract and the staking contract executes trade on chain.
#### Prerequisites
* Bot has an eth wallet in order to send transactions to the blockchain
* Bot wallet is funded with sufficient eth to be able to execute swap transactions
* SabotStaking smart contract is deployed
* Bot has SabotStaking contract address and ABI
* Bot wallet was authorized as the SABOT_TRADER role in the SabotStaking smart contract
* Sabot Trading Monitor is listening to events emitted by SabotStaking
* SabotStaking smart contract is set up with the Curve Pool address
* SabotStaking smart contract is set up with the token address to pool index mapping
#### Requirements
* Sabot bot python program makes a call to the swap method of the SabotStaking smart contract
* Sabot smart contract translates from token address to pool index
* SabotStaking smart contract calls Curve Pool exchange function to execute swap
* SabotStaking emits an event that swap has occurred
* Sabot Trading Monitor shows the swap event
#### Verification
* Swap event is observed in the Sabot Trading Monitor

### Scenario - Tokenomics  (Not MVP)
#### Objective 
Demonstrate that the CLOG is effective at
- representing participant ownership stake
- tracking participant porportional value
#### Prerequisites
* SabotStaking smart contract is deployed
* SabotStaking smart contract has a portfolio of USDT tokens (stretch goal to also have sUSD, though not MVP)
* SabotStaking has participants and there is an amount of CLOG tokens in circulation
* SabotStaking has a method to calculate and return token price
* 2 participants with CLOGs
#### Requirements
* Get initial CLOG price
* Artificially increase portfolio value by transferring a quantity of USDT to SabotStaking smart contract
* Get subsequent CLOG price
#### Verification
* Initial CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation
* Each participant share and value is accuretly represented by amount of CLOG tokens each have and price of tokens
* After increase, CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation
* Each participant share is unaffected by increase in price, but increase in value is relfected in CLOG increase in price
 
### Scenario - Deployment
#### Objective
There are dependencies that will need to be configured properly.  To minimize cost, a deployment contract will be used. All on chain configuration will be effected through the deployment contract.  To minimize cost, on-chain configuration will be prioritized over off chain configuration and only one deployment transaction should be needed.  The resulting smart contract ensures asset safety and prevents rug pull or any other adverse action by any nefarious actor.
#### Prerequisites
* CLOG token contract is compiled
* SabotStaking contract is compiled
* Bot wallet address is available
* USDT token address is available
* USDT token index in Curve Pool is available
* sUSD token address is available
* sUSD token index in Curve Pool is available
* Curve Pool smart contract is deployed and pool contract address is available
* Multisig wallet is available  (needs more elaboration)
#### Requirements
* Multisig contract deploys the deployment contract
    * passes in the following:
        * bot wallet address
        * mapping of coin address to pool index
        * curve pool address
* deployment contract deploys the SabotStaking contract and gets its address
    * set the bot address as the SabotStaking TRADER_ROLE in constructor
    * set the Curve Pool address in constructor
    * set coin to pool integr mapping in the constructor
* deployment contract deploys the CLOG token contract and gets its address
    * set the SabotStaking contract address as the CLOG MINTER_ROLE in constructor
#### Verification
* SabotStaking contract is deployed
* Clog token contract is deployed
* bot wallet address has the SABOT_TRADER role
* No other addresses have the SABOT_TRADER role
* SabotStaking smart contract address has the CLOG_MINTER role
* No other addresses have the CLOG_MINTER role
* The other scenarios can be performed as expected

## Solution Assets Inventory
The solution consists of several components which are identified below:

| Asset | Technology | Type | Description |
|-------|------|---------|------------ |
| Staking.py | Streamlit | Solution | The UI users can use to stake USDT to participate in the Sabot pool. |
| event_filter.py | Python | Solution | A simple CLI that monitors transactions in the SabotStaking contract to give visibility to what is happening in the contract. |
| ClogToken.sol | Solidity | Solution | The smart contract that implements the CLOG ERC-20 utility token. |
| SabotStakingProxy.sol | Solidity | Solution | The ERC1697 proxy smart contract that enables UUPS. |
| SabotStakingV1.sol | Solidity | Solution | The SabotStaking implementation (aka logic) smart contract that the proxy contract delegates to. |
| curvePool.sol | Solidity | Mock | A smart contract that implements a mock for a Curve liquidity pool. |
| usdtToken.sol | Solidity | Mock | A smart contract that implements a mock for the base token for the arbitrage strategy. |
| susdToken.sol | Solidity | Mock | A smart contract that implements a mock for the target token for the arbitrage strategy. |
| DeploySabotStaking.sol | Solidity | Deployment | The smart contract that deploys the on-chain portions of the SabotStaking solution. |
| DeployTestAssets.sol | Solidity | Deployment | The smart contract that deploys the on-chain mock contracts needed for testing. |

## Deployment and Testing
Since this solution consists of Web3 applications and and smart contracts, Ganache is used as the test environment in the following section.

### Allocate Wallet Addresses   (John)

*a table that lists how many of the ganache wallets will be used and for what purpose*

### Deploy Test Assets          (John)
If deploying in a test environment, deploy dependencies using **DeployTestAssets.sol**.

*Instructions needed, additionally, video even better*
*list addresses that need to be retrieved and how to do that*

### Deploy SabotStaking         (Yanick)

*Instructions needed, additionally, video even better*
*list addresses that need to be retrieved and how to do that*

### Configure REMIX IDE         (Yanick)
*Instructions on how to configure REMIX IDE for Testing*

### Configure participant wallets   (Yanick)
*Instructions on how to connect participant wallets, e.g. adding USDT sUSD and CLOG tokens, video even better*

### Test Scenarios
#### Participant Staking      (Quintin)
*Instructions / demo on how a participant stakes USDT in order to join the pool and receives CLOG, video even better**

#### Automated arbitrage trading    (John)
*Instructions on how to set up the monitor and / demo showing automated arbitrage trading, video even better**


```
wallet 1: 0xeb170e4FCC7693618857E468CFF622217ec6b577 - deployTestAssets(owns USDT, SUSD, curvePool) deploySabotStakingAssets(admin of Clog and SabotStaking)
wallet 2: 0x8BD0536656a365272cC181A9561C8a8C744b90d7
wallet 3: 0x522Ce41bB0299859e9CF112440AD16875Ab60c26
wallets to initialize: ["0xeb170e4FCC7693618857E468CFF622217ec6b577","0x8BD0536656a365272cC181A9561C8a8C744b90d7","0x522Ce41bB0299859e9CF112440AD16875Ab60c26"]

botWallet: 0x8Ced51Ee27E45B7f862F67BaE3DCc176096B5bE0   (in deployment configured to be SABOT_BOT_ROLE -> swap())
usdt: 0x26fdA07e0e2ca5F407D97b267DD006356e367241
susd: 0x3ad5AD3DEE8f32cFa960373CA7B9Aba5f3B1b12C
curve pool: 0x6eF74B9C422f7148635694a93bBacF0DB3Cd7BC7
clog: 
sabotStaking: 
```

