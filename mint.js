const Web3 = require('web3'); //Import Web3

//##########################################
//#                                       ##
//#   ##   ##   #   ##    #   #########   ##
//#   # # # #       # #   #       #       ##
//#   #  #  #   #   #  #  #       #       ##
//#   #     #   #   #   # #       #       ##
//#   #     #   #   #    ##       #       ##
//#                                       ##
//##########################################
//            Created by Fonex

//READ ME !!!!!!!!!!!!!!!!!
//PARAM CHANGE
// - MINT INFO
// - NFT
// - GAS (if you want)
// - RPC (if not avalanche C-Chain)
// - WALLET INFO
// - CONTRACT  (abi and address)
// AND in "DoingTransaction", var swap
// !! Don't touch the rest !!

//MINT INFO
var hours = 16; //Hours 
var min = 10; //Minutes
var sec = 0; //Seconds
var milisec = 0; //MiliSeconds

//NFT
var pricenft = 0; //Price of mint (in ETH, Avax ...)
var numbernft = 1; //Number of nft mint

//GAS (BOOST TX)
var FeePerGas = 300; //FeePerGas
var PriorityFeePerGas = 80; //PriorityFeePerGas

//RPC
var web3 = new Web3(new Web3.providers.HttpProvider("https://api.avax.network/ext/bc/C/rpc")); //RPC of blockchain

//WALLET INFO
var private_key = '.......................'; //Private key
var wallet_addr = web3.utils.toChecksumAddress('.........................'); //Wallet address

//CONTRACT
var contract_abi1 = "......................";
var contract_address1 = web3.utils.toChecksumAddress('......................'); //Address of smart contract 
var ContractCrypto1 = new web3.eth.Contract(contract_abi1, contract_address1); //Create smart contract

async function DoingTransaction(){ 
    var count = await web3.eth.getTransactionCount(wallet_addr); //For nonce
    var swap = ContractCrypto1.methods.mint(numbernft) //Call function "mint" in smart contract      !!!!!!! This function can be changed (name or paramÃ¨tre) !!!!!!!
    var tx = ({
        gas: 250000, //Gas Limit
        from: wallet_addr, //From 
        to: contract_address1, //To
        value: web3.utils.toWei(String(numbernft*pricenft), 'ether'), //Value of transaction = value of mint
        data: swap.encodeABI(), //Data of transaction (function call)
        nonce:web3.utils.toHex(count), //Nonce
        maxPriorityFeePerGas: web3.utils.toWei(String(PriorityFeePerGas), 'gwei'), //MaxPriorityFeePerGas
        maxFeePerGas:  web3.utils.toWei(String(FeePerGas), 'gwei'), //MaxFeePerGas
    })
    var signedTx = await web3.eth.accounts.signTransaction(tx, private_key) //Sign tx
    web3.utils.isHex(signedTx.rawTransaction) //Convert in Hex
    web3.eth.sendSignedTransaction(signedTx.rawTransaction) //Send Signed
    console.log("DONE") //End
}

async function run() {
    console.log("AMENO") //Ameno
    DoingTransaction() //Call function "DoingTransaction"
} 

var now = new Date(); //Date of excute script

var time = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, min, sec, milisec) - Date.now(); //Date of mint - Date of excute script
setTimeout(() => {run()}, time); //Call function "run" when timer is 0