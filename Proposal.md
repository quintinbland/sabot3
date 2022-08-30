# SabotStaking defi
SabotStaking is a defi smart contract that will enable participants to safely and securely participate in a collaborative pool. Participants can opt to participate in the Sabot pool by staking USDT tokens using the SabotStaking UI.  Participants will receive CLOGs in exchange for their stake. The SabotStaking smart contract complements the Sabot trading bot.  The Sabot bot will be provide trading direction to the SabotStaking contract. The benefit of implementing the pool through the SabotStaking contract is that the funds can be securely held in a trustless manner.  No central entity or individual is able to unilaterally access the funds of the smart contract or withdraw them.  Furthermore, this structure would enable the pool to scale up and accomodate additional participants.

## Team Members
| Name                 | email                       | 
|----------------------|-----------------------------|
| Quintin Bland        | quintinbland2@gmail.com     |
| Kevin Corstorphine   | kevincorstorphine@gmail.com |
| John Gruenewald      | john.h.gruenewald@gmail.com |
| Martin Smith         | msmith92663@gmail.com       |
| Yanick Wilisky       | yanickw@gmail.com           |

## Scenario
* Five study group members want to form a collective that leverages the Sabot trading bot for automated arbitrage trading
* Each participant contributes an initial amount of USDT and eth. 
* We don't trust each other - we want a solution that is designed to prevent a nefarious actor from impacting other participants
* Particiaption stake is represented by CLOG tokens
* The Sabot trading bot will make the trading decisions and direct the SabotStaking contract to execute the trades.
* For best pricing, lowest overhead costs, trading will be executed on chain on a Curve Pool.

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
    * implements the exchange method
* Multisig Vault to deploy SabotStaking smart contract
* SabotStaking UI
* SabotStaking smart contract monitoring UI
