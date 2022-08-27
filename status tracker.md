### Activities
## 8/27
* quick status of tasks
* quick team member updates
* Demos
* Solution Integration
* Testing
* Next steps

## Solution Components
* CLOG ERC-20 token [DONE]
* Curve Pool Mock contract [DONE]
* POC to mint/burn CLOG [Done]
* POC to call Curve Pool Mock Contract [Done]
* Generate new wallet for bot using Python - [DONE]
* Create test ISabotTrader test contract [John - In Progress]
* POC to call swap method from python program using bot wallet [John - In Progress]
* Create test multisig wallet using Gnossis [DONE]
* Create deployment contract [Done]
* POC to get events from proxied contract [Done]
* Update architecture diagrams [Done]
* SabotStaking base contract [Done]
* Deployment contract requirements [Done]
* Staking UI [Quintin - in progress]
    * needs to call staking method of SabotStaking smart contract
* USDT Token for test - for staking [Done] 
* sUSD Token for test - for staking [Done] 
* Complete python program that emulates bot giving trade direction to smart contract [John - In Progress]
* Set up scheduler (crontab) and demo automated trading [Pending]
* Growth simulation [Yanick - TBD] 
   * mint USTD using USDT owner and mint to SabotStaking contract address
* Solidity Discovery - TBD
    * Is the transaction cost higher when a contract calls another contract?
    * prototype the contract calling another contract (Kevin / Yannick)
        * contract 1 - called by a web3 client   , it has two methods, method 1 and method 2
        * contract 2 - called by contract 1 - method 2
        * Is the gas fee calling contract 1 menthod 1 cheaper than calling contract 1 method 2 (which is the one calling contract 2)?
        * Does it work or is there an out of gas error.
    * Is the deployment cost higher when using an upgradable proxy contract than deploying a standard fixed contract?
    * Is the deployment cost higher for deploying an upgradable proxy contract higher when using a deployment contract or when using a Web3 deployment script?
        * any impacts to the transaction costs?
    * Is the transaction cost higher when using a proxy contract method than calling the same contract on a fixed contract?
        * If there is transaction cost savings and if the deployment cost is higher, what is the ROI for the SabotStaking arbitrage strategy?
* Test multisig process [Kevin - Deferred]

## work session items
* Have a non-proxy versionb that is deployable in ganache
* connect using web3

## Next steps
* Create a new Ganache workspace with sufficient bolc gas limit - needed to run demo and test using Ganache
* ERC-20 approval / allowance in context of staking

## Future / Out of MVP Scope 
* Unstaking / burning
* actual trading
* mocking a swap of stablecoins
* demo'ing unstaking after growth of portfolio
* demo'ing future participants after growth of portfolio

