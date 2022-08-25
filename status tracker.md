### Activities

* create a wallet using python web 3 for the bot (John)
* deploy a contract using a multisig wallet (gnossis) (Kevin)
* cron and random trade direction for smart contract and calls smart contract (John)
    * contract method signature is `swap(sellToken address, sellToken amount, buyToken address) return (struct SabotSwapResult)`
* Prototype 0X filter for curve (Kevin - Priority B) - Cancelled
* Test contract call curve contract to do a trade, where is curve on the test chain?
    * find Curve / USDT / SUSD on test chain (Yanick) - Completed
    * mock curve - 
----- smart contract    
* Clog Token (Quintin)  ERC-20
    * create a IClogMinter
* Smart contract to execute trades with curve on chain
   * minting
   * foundation (Martin)
      interface  (Martin) [DONE]
      library  [DONE]
      static contract address
      (open zeppeling proxy) [IN-PROGESS]
     * struct SabotSwapResult
     * IClogMinter
     * ICLogStaking
     * ISabotTrader
     * Stake (mint) / Unstake (burn)  (John)
     * trade method  (Martin / Yannick)
   * prototype the contract calling another contract (Kevin / Yannick)
       * contract 1 - called by a web3 client   , it has two methods, method 1 and method 2
       * contract 2 - called by contract 1 - method 2
       * Is the gas fee calling contract 1 menthod 1 cheaper than calling contract 1 method 2 (which is the one calling contract 2)?
       * Does it work or is there an out of gas error.
------ 
* Streamlit UI (MVP) Quintin
    * Staking UI - web3 like experience (using your web3 wallet) - exchange usdt for token (Quintin)
    * Monitoring UI - view filtered contract events - insight of what is happenning on-chain POC / Martin
        * research getting events in (Yanick/Martin)
    * TBD - Graph of balances ( or other)
* Metamask integration - see token balance

discussion on multisig wallet
demo of calling contract method
Demo of Curve mock contract
Demo of wallet
Demo of clog token and clog minter
* Demo of proof of concept on event listening
Demo of architecture diagrams
Demo Skeleton of Staking UI

## Solution Components
* CLOG ERC-20 token [DONE]
* Curve Pool Mock contract [DONE]
* POC to mint/burn CLOG [Quintin - In Progress] test and demo
* POC to call Curve Pool Mock Contract [Yanick - In Progress]
* Generate new wallet for bot using Python - [DONE]
* Create test ISabotTrader test contract [John - In Progress]
* POC to call swap method from python program using bot wallet [John - In Progress]
* Create test multisig wallet using Gnossis [DONE]
* Test multisig process [Kevin - in progress]
* Create initial deployment contract [Kevin - in progress]
* Create initial deployment contract [Kevin - in progress]
* POC to deploy initial deployment contract using multisig wallet [Kevin - in progress]
* POC to get events from proxied contract [Martin - in progress]
* Update architecture diagrams [Martin - in progress]
* SabotStaking base contract [Martin - in progress]
* Deployment contract requirements [Martin - in progress]
* Staking UI [Quintin - in progress]
    * needs to call staking method of SabotStaking smart contract
* USDT Token for test - for staking [TBD] 
* Complete python program that emulates bot giving trade direction to smart contract
* Set up scheduler (crontab) and demo automated trading



## Scenario - Staking
### Objective
Allow participant to stake a certain amount of USDT and receive CLOG in return.  This is done through our SabotStaking UI.
### Prerequisites
* Participant has wallet
* Participant has available USDT to stake
* SabotStaking smart contract is deployed
* UI has SabotStaking contract address and ABI
* SabotStaking smart contract is authorized as the MINTER_ROLE for CLOG
### Requirements
* Participant connects their wallet by entering wallet address into the address text field
* UI connects the wallet
* Participant enters the amount of USDT they want to stake
* Participant clicks on the stake button to execute the stake
* UI effects a transfer of USDT from the participants wallet to the SabotStaking smart contract
* SabotStaking smart contract mints an amount of CLOG proportional to the amount of USDT that was staked
* SabotStaking smart contract assigns the minted CLOG to the wallet that staked the USDT
* SabotStaking smart contract emits an event that indicates staking occurred
* UI confirms swap has occured by looking at the transaction receipt and confirming that the Staking event exists and indicates the amount of CLOG received from the staking.
### Verification
* Participant wallet USDT balance is decremented by the amount that was staked
* Participant wallet CLOG balance is increased by an amount proportional to what was staked
* SabotStaking smart contract USDT balance is increased by the amount that was staked.

## Scenario - Arbitrage Trading
### Objective
The bot is able to send trade orders to the StakingSmart contract and the staking contract executes trade on chain.
### Prerequisites
* Bot has an eth wallet in order to send transactions to the blockchain
* Bot wallet is funded with sufficient eth to be able to execute swap transactions
* SabotStaking smart contract is deployed
* Bot has SabotStaking contract address and ABI
* Bot wallet was authorized as the SABOT_TRADER role in the SabotStaking smart contract
* Sabot Trading Monitor is listening to events emitted by SabotStaking
* SabotStaking smart contract is set up with the Curve Pool address
* SabotStaking smart contract is set up with the token address to pool index mapping
### Requirements
* Sabot bot python program makes a call to the swap method of the SabotStaking smart contract
* Sabot smart contract translates from token address to pool index
* SabotStaking smart contract calls Curve Pool exchange function to execute swap
* SabotStaking emits an event that swap has occurred
* Sabot Trading Monitor shows the swap event
### Verification
* Swap event is observed in the Sabot Trading Monitor

## Scenario - Tokenomics  (Not MVP)
### Objective 
Demonstrate that the CLOG is effective at
- representing participant ownership stake
- tracking participant porportional value
### Prerequisites
* SabotStaking smart contract is deployed
* SabotStaking smart contract has a portfolio of USDT tokens (stretch goal to also have sUSD, though not MVP)
* SabotStaking has participants and there is an amount of CLOG tokens in circulation
* SabotStaking has a method to calculate and return token price
* 2 participants with CLOGs
### Requirements
* Get initial CLOG price
* Artificially increase portfolio value by transferring a quantity of USDT to SabotStaking smart contract
* Get subsequent CLOG price
### Verification
* Initial CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation
* Each participant share and value is accuretly represented by amount of CLOG tokens each have and price of tokens
* After increase, CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation
* Each participant share is unaffected by increase in price, but increase in value is relfected in CLOG increase in price
 
## Scenario - Deployment
### Objective
There are dependencies that will need to be configured properly.  To minimize cost, a deployment contract will be used. All on chain configuration will be effected through the deployment contract.  To minimize cost, on-chain configuration will be prioritized over off chain configuration and only one deployment transaction should be needed.  The resulting smart contract ensures asset safety and prevents rug pull or any other adverse action by any nefarious actor.
### Prerequisites
* CLOG token contract is compiled
* SabotStaking contract is compiled
* Bot wallet address is available
* USDT token address is available
* USDT token index in Curve Pool is available
* sUSD token address is available
* sUSD token index in Curve Pool is available
* Curve Pool smart contract is deployed and pool contract address is available
* Multisig wallet is available  (needs more elaboration)
### Requirements
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
### Verification
* SabotStaking contract is deployed
* Clog token contract is deployed
* bot wallet address has the SABOT_TRADER role
* No other addresses have the SABOT_TRADER role
* SabotStaking smart contract address has the CLOG_MINTER role
* No other addresses have the CLOG_MINTER role
* The other scenarios can be performed as expected

## Future / Out of MVP Scope 
* Unstaking / burning
* actual trading
* mocking a swap of stablecoins
* demo'ing unstaking after growth of portfolio
* demo'ing future participants after growth of portfolio

