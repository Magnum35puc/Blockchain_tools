from web3 import Web3
import json


class Blockchain:
    def __init__(self,rpc ='https://api.avax.network/ext/bc/C/rpc'):
        self.w3=Web3(Web3.HTTPProvider(rpc))

    def isConnected(self):
        return self.w3.isConnected()
    def getBlockNumber(self):
        return self.w3.eth.blockNumber
    def getGasPrice(self):
        return self.w3.fromWei(self.w3.eth.gas_price,"ether")
    def getStatus(self):
        if self.isConnected():
            print(f"You are connected to the blockchain at the block {self.getBlockNumber()}")
            print(f"The current gas price is : { self.getGasPrice() }")
        else : 
            print("You're not connected to the blockchain")


    


        