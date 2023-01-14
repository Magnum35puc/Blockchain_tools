from web3 import Web3
import json
from datetime import datetime
from Blockchain_Objects.ERC20 import ERC20Token

class Wallet:
    def __init__(self, adrs:str,list_token=[], ERC20ABI_file:str="ABIs\ABI_ERC20.json",rpc ='https://api.avax.network/ext/bc/C/rpc'):
        self.adress = adrs
        self.tokens = list_token

        with open(ERC20ABI_file, 'r') as f: #ABI Pangolin works for TJOE too
            self.ERC20_ABI = json.load(f)
        self.w3=Web3(Web3.HTTPProvider(rpc))
        self.last_balance = self.w3.fromWei(self.w3.eth.getBalance(self.w3.toChecksumAddress(self.adress)),"ether")

    def updateBalance(self):
        self.last_balance = self.w3.fromWei(self.w3.eth.getBalance(self.w3.toChecksumAddress(self.adress)),"ether")

    def getAllBalances(self):
        self.last_balance = self.w3.fromWei(self.w3.eth.getBalance(self.w3.toChecksumAddress(self.adress)),"ether")
        allbalances = {"Main Token":float(self.last_balance)}
        for token in self.tokens :
            allbalances.update({token.symbol: token.getBalanceOf(self.adress)})
        return allbalances



    


        