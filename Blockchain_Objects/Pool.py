from web3 import Web3
import json
from datetime import datetime
from Blockchain_Objects.ERC20 import ERC20Token

class Avalanche_Pool:
    def __init__(self, adrs:str, POOLABI_file:str="ABIs\ABI_Pangolin.json", ERC20ABI_file:str="ABIs\ABI_ERC20.json",rpc ='https://api.avax.network/ext/bc/C/rpc'):
        self.adress = adrs
        with open(POOLABI_file, 'r') as f: #ABI Pangolin works for TJOE too
            self.Pool_ABI = json.load(f)
        self.w3=Web3(Web3.HTTPProvider(rpc))
        self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.adress), abi=self.Pool_ABI)
        try : 
            self.pool_name = self.contract.functions.name().call()
            self.pool_symbol = self.contract.functions.symbol().call()
        except : 
            self.pool_name = "Undefined"
            self.pool_symbol = "Undefined"
        self.tokens = [ERC20Token(self.contract.functions.token0().call(), ERC20ABI_file,self.w3),ERC20Token(self.contract.functions.token1().call(), ERC20ABI_file,self.w3)]
        
    def printPoolinfos(self):
        #Get updated data 
        reserves = self.contract.functions.getReserves().call() # Reserves token 0 ,  Reserves token 1 , Timestamp

        print(f"[{self.pool_symbol}] {self.pool_name} pool  has a total tokens in the pool: {round(reserves[0]/10**self.tokens[0].decimals,3)} {self.tokens[0].symbol} and {round(reserves[1]/10**self.tokens[1].decimals,3)} {self.tokens[1].symbol}. Last updated at : {datetime.fromtimestamp(reserves[2])}")


        price_t0 = (reserves[1]/10**self.tokens[1].decimals) / (reserves[0]/10**self.tokens[0].decimals)
        price_t1 = (reserves[0]/10**self.tokens[0].decimals) / (reserves[1]/10**self.tokens[1].decimals)

        print(f"Total liquidity of the pool : {((reserves[0]/10**self.tokens[0].decimals)*price_t0) + reserves[1]/10**self.tokens[1].decimals}")

        print (f"Price of {self.tokens[0].symbol} = {round(price_t0,5)} {self.tokens[1].symbol}")
        print (f"Price of {self.tokens[1].symbol} = {round(price_t1,5)} {self.tokens[0].symbol}")
    
    def getTokenPrice(self,token_index):
        '''
        Function that queries the pool and returns the price of token X in the unit of token Y and the time of the query 
        '''
        valid = {0, 1}
        if token_index not in valid:
            raise ValueError("results: status must be one of %r." % valid)
        else : 
            reserves = self.contract.functions.getReserves().call() # Reserves token 0 ,  Reserves token 1 , Timestamp
            timestamp = reserves[2]
            price = (reserves[1-token_index]/10**self.tokens[1-token_index].decimals) / (reserves[token_index]/10**self.tokens[token_index].decimals)
            units = self.tokens[1-token_index].symbol
            return price, units, timestamp
    def getTokenList(self):
        return self.tokens
    def getBalanceOf(self,adrss):
        return (self.contract.functions.balanceOf(self.w3.toChecksumAddress(adrss)).call())

