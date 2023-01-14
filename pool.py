from web3 import Web3
import json
from datetime import datetime

class ERC20Token :
    def __init__(self, adrs:str,ERC20ABI_file:str="ER20_ABI.json",w3=Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))):
        with open(ERC20ABI_file) as erc20File:
            self.ERC20_ABI = json.load(erc20File)
        self.w3=w3
        self.token = self.w3.eth.contract(address=self.w3.toChecksumAddress(adrs), abi=self.ERC20_ABI)
        self.symbol = self.token.functions.symbol().call()
        self.decimals = self.token.functions.decimals().call()

class Avalanche_Pool:
    def __init__(self, adrs:str, POOLABI_file:str="ABI_Pangolin.json", ERC20ABI_file:str="ER20_ABI.json",w3=Web3(Web3.HTTPProvider('https://api.avax.network/ext/bc/C/rpc'))):
        self.adress = adrs
        with open(POOLABI_file, 'r') as f: #ABI Pangolin works for TJOE too
            self.Pool_ABI = json.load(f)
        self.w3=w3
        self.contract = self.w3.eth.contract(address=self.w3.toChecksumAddress(self.adress), abi=self.Pool_ABI)
        self.pool_name = self.contract.functions.name().call()
        self.pool_symbol = self.contract.functions.symbol().call()
        self.tokens = [ERC20Token(self.contract.functions.token0().call()),ERC20Token(self.contract.functions.token1().call())]
        
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


WAVAXvUSDT_Pangolin_adrs = "0x9ee0a4e21bd333a6bb2ab298194320b8daa26516"
WAVAXvUSDT_Pangolin_Pool = Avalanche_Pool(WAVAXvUSDT_Pangolin_adrs)
WAVAXvUSDC_Pangolin_adrs = "0x0e0100ab771e9288e0aa97e11557e6654c3a9665"
WAVAXvUSDC_Pangolin_Pool = Avalanche_Pool(WAVAXvUSDC_Pangolin_adrs)
WAVAXvUSDC_TJOE_adrs = "0xf4003f4efbe8691b60249e6afbd307abe7758adb"
WAVAXvUSDC_TJOE_Pool = Avalanche_Pool(WAVAXvUSDC_TJOE_adrs)

print(WAVAXvUSDT_Pangolin_Pool.getTokenPrice(0))
print(WAVAXvUSDC_Pangolin_Pool.getTokenPrice(0))
print(WAVAXvUSDC_TJOE_Pool.getTokenPrice(0))
print(WAVAXvUSDT_Pangolin_Pool.getTokenPrice(1))
print(WAVAXvUSDC_Pangolin_Pool.getTokenPrice(1))
print(WAVAXvUSDC_TJOE_Pool.getTokenPrice(1))


