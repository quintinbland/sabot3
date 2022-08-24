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
Demo of proof of concept on event listening
Demo Skeleton of Staking UI
Demo of architecture diagrams