from web3 import Web3
import json


class ERC20Token :
    def __init__(self, adrs:str,ERC20ABI_file:str="ABIs\ABI_ERC20.json",w3=Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))):
        with open(ERC20ABI_file) as erc20File:
            self.ERC20_ABI = json.load(erc20File)
        self.w3=w3
        self.token = self.w3.eth.contract(address=self.w3.toChecksumAddress(adrs), abi=self.ERC20_ABI)
        self.symbol = self.token.functions.symbol().call()
        self.decimals = self.token.functions.decimals().call()

    def getBalanceOf(self,adrss):
        return (self.token.functions.balanceOf(self.w3.toChecksumAddress(adrss)).call())/10**self.decimals