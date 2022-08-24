# SabotStaking
SabotStaking is a defi smart contract that will enable participants to safely and securely participate in a collaborative pool. Participants can opt to participate in the Sabot pool by staking USDT tokens using the SabotStaking UI.  Participants will receive CLOGs in exchange for their stake. The SabotStaking smart contract complements the Sabot trading bot.  The Sabot bot will be provide trading direction to the SabotStaking contract. The benefit of implementing the pool through the SabotStaking contract is that the funds can be securely held in a trustless manner.  No central entity or individual is able to unilaterally access the funds of the smart contract or withdraw them.  Furthermore, this structure would enable the pool to scale up and accomodate additional participants.

## Team Members

| Name                 | email                       | 
|----------------------|-----------------------------|
| Quintin Bland        | quintinbland2@gmail.com     |
| Kevin Corstorphine   | kevincorstorphine@gmail.com |
| John Gruenewald      | john.h.gruenewald@gmail.com |
| Martin Smith         | msmith92663@gmail.com       |
| Yanick Wilisky       | yanickw@gmail.com           |

## Project Objectives

* continue with sabot
* develop smart contracts to securely hold the arbitrage tokens
    * design for trustless model
* tokenize participation
* Provide a UI for participants to stake their tokens into the pool
* Enable the Sabot trading bot to communicate trading directions to the staking pool
* Execute exchanges on chain to get best pricing


## Breakdown of Tasks

* CLOG ERC-20 token 
* SabotStaking smart contract
    * mint and burn CLOG based on staking and unstaking
    * staking and unstaking of USDT
    * execute swaps using a Curve Fi Pool exchange method
* Curve Pool test contract
    * implements the exchange mehtod
* Multisig Vault to deploy SabotStaking smart contract
* SabotStaking UI
* SabotStaking smart contract monitoring UI


## Scenario
* Five study group members want to form a collective that leverages the Sabot trading bot for automated arbitrage trading
* Each participant contributes an initial amount of USDT and eth. 
* We don't trust each other - we want a solution that is designed to prevent a nefarious actor from impacting other participants
* Particiaption stake is represented by CLOG tokens
* The Sabot trading bot will make the trading decisions and direct the SabotStaking contract to execute the trades.
* For best pricing, lowest overhead costs, trading will be executed on chain on a Curve Pool.


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
Demo of proof of concept on event listening
Demo of clog token and clog minter
Demo Skeleton of Staking UI
Demo of architecture diagrams