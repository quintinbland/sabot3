# SabotStaking Pool
The `SabotStaking Pool` is a configurable fit for purpose defi pool aimed at accelerating the implementation of automated cryptocurrency arbitrage trading strategies.
The solution consists of a set of coordinated web3 applications and smart contracts that are designed to.
* secure participant assets.
* prevent risk of fraud, rug pulls and other nefarious actions.
* minimize transaction costs through on-chain trading.
* scale to support the demands of large defi solutions.

### **Tech**
* wizard.openzeppelin.com - An online wizard provided by OpenZeppelin that creates contract skeleton based on advanced feature selections.

---

## Solution Design
The following scenarios were generated to drive out the critical design aspects and dependencies.

### SCENARIO - Staking

#### **Objective**
Allow participant to stake a certain amount of `USDT` and receive `CLOG` in return.  This is done through our SabotStaking UI.

#### **Prerequisites**
* Participant has wallet.
* Participant has available `USDT` to stake.
* SabotStaking smart contract is deployed.
* UI has SabotStaking contract address and ABI.
* SabotStaking smart contract is authorized as the `MINTER_ROLE` for `CLOG`.

#### **Requirements**
* Participant connects their wallet by entering wallet address into the address text field.
* UI connects the wallet.
* Participant enters the amount of `USDT` they want to stake.
* Participant clicks on the stake button to execute the stake.
* UI effects a transfer of `USDT` from the participants wallet to the SabotStaking smart contract.
* SabotStaking smart contract mints an amount of `CLOG` proportional to the amount of `USDT` that was staked.
* SabotStaking smart contract assigns the minted `CLOG` to the wallet that staked the `USDT`.
* SabotStaking smart contract emits an event that indicates staking occurred.
* UI confirms swap has occured by looking at the transaction receipt and confirming that the Staking event exists and indicates the amount of `CLOG` received from the staking.

#### **Verification**
* Participant wallet `USDT` balance is decremented by the amount that was staked.
* Participant wallet `CLOG` balance is increased by an amount proportional to what was staked.
* SabotStaking smart contract `USDT` balance is increased by the amount that was staked.

---

### SCENARIO - Arbitrage Trading

#### **Objective**
The bot is able to send trade orders to the StakingSmart contract and the staking contract executes trade on chain.

#### **Prerequisites**
* Bot has an eth wallet in order to send transactions to the blockchain.
* Bot wallet is funded with sufficient eth to be able to execute swap transactions.
* SabotStaking smart contract is deployed.
* Bot has SabotStaking contract address and ABI.
* Bot wallet was authorized as the `SABOT_TRADER` role in the SabotStaking smart contract.
* Sabot Trading Monitor is listening to events emitted by SabotStaking.
* SabotStaking smart contract is set up with the Curve Pool address.
* SabotStaking smart contract is set up with the token address to pool index mapping.

#### **Requirements**
* Sabot bot python program makes a call to the swap method of the SabotStaking smart contract.
* Sabot smart contract translates from token address to pool index.
* SabotStaking smart contract calls `Curve Pool exchange` function to execute swap.
* SabotStaking emits an event that swap has occurred.
* Sabot Trading Monitor shows the swap event.

#### **Verification**
* Swap event is observed in the Sabot Trading Monitor.

---

### SCENARIO - Tokenomics  (Not MVP)

#### **Objective** 
Demonstrate that the CLOG is effective at:
- representing participant ownership stake.
- tracking participant porportional value.
#### **Prerequisites**
* SabotStaking smart contract is deployed.
* SabotStaking smart contract has a portfolio of USDT tokens (stretch goal to also have sUSD, though not MVP).
* SabotStaking has participants and there is an amount of CLOG tokens in circulation.
* SabotStaking has a method to calculate and return token price.
* 2 participants with `CLOGs`.
#### **Requirements**
* Get initial `CLOG` price.
* Artificially increase portfolio value by transferring a quantity of USDT to SabotStaking smart contract.
* Get subsequent `CLOG` price.
#### **Verification**
* Initial CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation.
* Each participant share and value is accuretly represented by amount of CLOG tokens each have and price of tokens.
* After increase, CLOG price accurately reflects SabotStaking portfolio value / CLOG tokens in circulation.
* Each participant share is unaffected by increase in price, but increase in value is relfected in CLOG increase in price.
 
---

### SCENARIO - Deployment

#### **Objective**
There are dependencies that will need to be configured properly.  To minimize cost, a deployment contract will be used. All on chain configuration will be effected through the deployment contract.  To minimize cost, on-chain configuration will be prioritized over off chain configuration and only one deployment transaction should be needed.  The resulting smart contract ensures asset safety and prevents rug pull or any other adverse action by any nefarious actor.

#### **Prerequisites**
* `CLOG` token contract is compiled.
* `SabotStaking` contract is compiled.
* `Bot wallet` address is available.
* `USDT token` address is available.
* `USDT token index` in `Curve Pool` is available.
* `sUSD token` address is available.
* `sUSD token index` in `Curve Pool` is available.
* `Curve Pool` smart contract is deployed and pool contract address is available.
* `Multisig wallet` is available  (needs more elaboration).

#### **Requirements**
* Multisig contract deploys the deployment contract.
    * passes in the following:
        * bot wallet address.
        * mapping of coin address to pool index.
        * curve pool address.

* deployment contract deploys the SabotStaking contract and gets its address.
    * set the bot address as the SabotStaking `TRADER_ROLE` in constructor.
    * set the Curve Pool address in constructor.
    * set coin to pool integr mapping in the constructor.

* deployment contract deploys the `CLOG` token contract and gets its address.
    * set the SabotStaking contract address as the `CLOG MINTER_ROLE` in constructor.

#### **Verification**
* SabotStaking contract is deployed.
* Clog token contract is deployed.
* bot wallet address has the `SABOT_TRADER` role.
* No other addresses have the `SABOT_TRADER` role.
* SabotStaking smart contract address has the `CLOG_MINTER` role.
* No other addresses have the `CLOG_MINTER` role.
* The other scenarios can be performed as expected.

---

## SOLUTION ASSETS INVENTORY
The solution consists of several components which are identified below:

| Asset | Technology | Type | Description |
|-------|------|---------|------------ |
| Staking.py | Streamlit | Solution | The UI users can use to stake `USDT` to participate in the Sabot pool. |
| event_filter.py | Python | Solution | A simple CLI that monitors transactions in the SabotStaking contract to give visibility to what is happening in the contract. |
| ClogToken.sol | Solidity | Solution | The smart contract that implements the CLOG ERC-20 utility token. |
| SabotStakingProxy.sol | Solidity | Solution | The ERC1697 proxy smart contract that enables UUPS. |
| SabotStakingV1.sol | Solidity | Solution | The SabotStaking implementation (aka logic) smart contract that the proxy contract delegates to. |
| curvePool.sol | Solidity | Mock | A smart contract that implements a mock for a Curve liquidity pool. |
| usdtToken.sol | Solidity | Mock | A smart contract that implements a mock for the base token for the arbitrage strategy. |
| susdToken.sol | Solidity | Mock | A smart contract that implements a mock for the target token for the arbitrage strategy. |
| DeploySabotStaking.sol | Solidity | Deployment | The smart contract that deploys the on-chain portions of the SabotStaking solution. |
| DeployTestAssets.sol | Solidity | Deployment | The smart contract that deploys the on-chain mock contracts needed for testing. |

---

## DEPLOYMENT AND TESTING
Since this solution consists of Web3 applications and and smart contracts, Ganache is used as the test environment in the following section.

### 1. Allocate Wallet Addresses   (John)

*a table that lists how many of the ganache wallets will be used and for what purpose*

### 2. Deploy Test Assets          (John)
If deploying in a test environment, deploy dependencies using **DeployTestAssets.sol**.

*Instructions needed, additionally, video even better*
*list addresses that need to be retrieved and how to do that*

### 3. Deploy SabotStaking         (Yanick)

*Instructions needed, additionally, video even better*
*list addresses that need to be retrieved and how to do that*

### 4. Configure REMIX IDE         (Yanick)
*Instructions on how to configure REMIX IDE for Testing*

### 5. Configure participant wallets   (Yanick)
*Instructions on how to connect participant wallets, e.g. adding USDT sUSD and CLOG tokens, video even better*

---

### TEST SCENARIOS

#### Participant Staking      (Quintin)
*Instructions / demo on how a participant stakes USDT in order to join the pool and receives CLOG, video even better**

#### Automated arbitrage trading    (John)
*Instructions on how to set up the monitor and / demo showing automated arbitrage trading, video even better**



---

```
wallet 1: 0x753f95da5E01A463c0952F81C3a4366e405019b1 - deployTestAssets(owns USDT, SUSD, curvePool) deploySabotStakingAssets(admin of Clog and SabotStaking)
wallet 2: 0x59fe7E0c4303125Ee5e1fA6248723BF017668835
wallet 3: 0x5771e5c030Aa3594E3385eBcdC2c3ea50A27a24f
wallets to initialize: ["0x753f95da5E01A463c0952F81C3a4366e405019b1","0x59fe7E0c4303125Ee5e1fA6248723BF017668835","0x5771e5c030Aa3594E3385eBcdC2c3ea50A27a24f"]

botWallet: 0x1c4b2bBBf8F31786Cd1de8c160A44De1152A6375   (in deployment configured to be SABOT_BOT_ROLE -> swap())
usdt: 0x563f1aAca7578AA493140d60be939d6bE9FA92De
susd: 0x3A5608A6F2B4bf13D98629Ca2207D4d2f674287F
curve pool: 0x776F4B255b8936963Fa1e9478063bA0E79486D50
clog: 
sabotStaking: 
```

```
Yanick's Cheat Sheet
wallet 1: 0x9aDdD9779374F638DFaac82A34B6c9E267839cE4 - deployTestAssets(owns USDT, SUSD, curvePool) deploySabotStakingAssets(admin of Clog and SabotStaking)
wallet 2: 0x1BDFEa7eB5405Ec90188f8dF38Fa1Ed60faA03f6
wallet 3: 0xb5B9458B59532a46510D07715d4663a2b4281c90
wallets to initialize: ["0x9aDdD9779374F638DFaac82A34B6c9E267839cE4","0x1BDFEa7eB5405Ec90188f8dF38Fa1Ed60faA03f6","0xb5B9458B59532a46510D07715d4663a2b4281c90"]

botWallet: 0x1c4b2bBBf8F31786Cd1de8c160A44De1152A6375   (in deployment configured to be SABOT_BOT_ROLE -> swap())
usdt: 0x9a664A426d0EB8353E8B150EC368B02e610F83e3
susd: 0x3f9844C447608a4E59D94A3c97013744CF243E8F
curve pool: 0xF1567B4f34f38C3e03708e5774e742C30c783E05
clog: 
sabotStaking: 
```

