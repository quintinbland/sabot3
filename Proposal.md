# Sabot
SABot is a machine learning powered automated trading bot that capitalizes on stablecoin instability.

## Team Members

| Name                 | email                       | 
|----------------------|-----------------------------|
| Quintin Bland        | quintinbland2@gmail.com     |
| Kevin Corstorphine   | kevincorstorphine@gmail.com |
| John Gruenewald      | john.h.gruenewald@gmail.com |
| Martin Smith         | msmith92663@gmail.com       |
| Yanick Wilisky       | yanickw@gmail.com           |

## Project Description / Outline

Focus:

* continue with sabot
* develop smart contracts to manage the money
* tokenize the participation
* UI for participants
* API for the bot


#### Options to bridge off chain to on chain

* app - Node(EVM) - chain
* streamlit (WEB3) -> Node(EVM) -> chain
* UI <-> webApp (WEB3 API) -> Node(EVM) -> chain
* App - AirNode(Node) - chain
* App - Infura(Node) - chain

vault vs dao - dao implies governance, vault is like a bank

#### Smart Contract

* design for trustless
* hold the money (pooled)
* receive transactions direction from sabot
* execute trades on chain
* participation token to represent stake in pool
* mint (participants can buy into the collective)

Scenario
* The five of us like sabot, we want to form a collective that leverages sabot for automated arbitrage trading
* In the hypothetical, we invest $20K for a total of $100k
* 5 members, but we don't trust each other
* smart contract hold our funds, represent ownership stake via token
* the wallet that creates the contract is the owner of the contract
* want the smart contract to execute trades automatically without requiring approval for participants

Multi-sig (gnosis wallet)
* update code (proxy)
* change contract settings
    * wallet allowed to send it trade directions

### Contract Properties  (multi role)

* multisig governance wallet (owner)
    * change settings (like libraries)
    * trade direction source (sabot wallet)
    * configure trade pair (USDT - sUSD)
* bot wallet needs to communicate trade direction 
* contract has to have eth to make trades
* contract execute trade automatically 
    * emitting an event representing (mocked)
* sabot bot needs to monitor emitted events
* mint coins
    * crowd sale
       * to fund pool
       * representative ownership stake
    * ERC-20 (ERC-1155)
* is a wallet for USDT and sUSD

* participant UI use case
   * Web3 UI that allows particants to buy in
   * buy into the pool using USDT, get representative token in return
   * get current value of sabot token
   * get history of bot

intentionally out of scope
* selling sabot tokens
* distribution of funds



### Activities

* create a wallet using python web 3 for the bot (John)
* deploy a contract using a multisig wallet (gnossis) (Kevin)
* cron and random trade direction for smart contract and calls smart contract (John)
* Prototype 0X filter for curve (Kevin - Priority B)
* Test contract call curve contract to do a trade, where is curve on the test chain?
    * find Curve / USDT / SUSD on test chain
    * mock curve?
----- smart contract    
* Clog Token
* Smart contract exchange USDT for clog token
    * minting
* Smart contract to execute trades with curve on chain
   * foundation (Martin)
      interface  (Martin)
      library
      static contract address
      (open zeppeling proxy)
------ 
* Streamlit UI (MVP)
    * web3 like experience (using your web3 wallet) - exchange usdt for token (Quintin)
    * Graph of balances ( or other)
    * view filtered contract events - insight of what is happenning on-chain
        * research getting events in 
* Metamask integration - see token balance