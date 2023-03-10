from Blockchain_Objects.Pool import Avalanche_Pool
from Blockchain_Objects.Wallet import Wallet
from Blockchain_Objects.Blockchain import Blockchain
from Blockchain_Objects.ERC20 import ERC20Token
from Backtests.Datas.BinanceAPI import Binance_API_data
from web3 import Web3
from typing import List
import pandas as pd
from backtesting import Backtest
from Backtests.Strategies.SMACross import SmaCross
from Backtests.Strategies.RSIxSMA import RSIxSMA 
from Backtests.Strategies.RSI import RSI_S
from Backtests.Strategies.Pct_Change import Pct_Change
import shelve




def getBestArbitrage(list_pool:List[Avalanche_Pool]):
    prices={}
    for pool in list_pool : 
        prices.update({pool.pool_name+': '+'/'.join(pool.getTokenNames()) : pool.getTokenPrice(0)})
    maxPricedPool = max(prices.values(), key=lambda x:x[0])
    minPricedPool = min(prices.values(), key=lambda x:x[0])
    keymaxPricedPool = [k for k, v in prices.items() if v == maxPricedPool]
    keysminPricedPool = [k for k, v in prices.items() if v == minPricedPool]

    print(f"Best arbitrage on AVAX/USD would be to buy {keysminPricedPool[0]} at {minPricedPool[0]} and to sell {keymaxPricedPool[0]} at {maxPricedPool[0]} for a profit(free of fees) of {maxPricedPool[0]-minPricedPool[0]} per token swapped")

def main():
    Avalanche_blockchain =  Blockchain()
    Avalanche_blockchain.getStatus()
    list_token_adrs = ["0x9702230a8ea53601f5cd2dc00fdbc13d4df4a8c7","0xb97ef9ef8734c71904d8002f8b6bc66dd9c48a6e","0xec3492a2508DDf4FDc0cD76F31f340b30d1793e6","0x49d5c2bdffac6ce2bfdb6640f4f80f226bc10bab","0xa7d7079b0fead91f3e65f86e8915cb59c1a4c664","0xc7198437980c041c805a1edcba50c1ce5db95118","0xd586e7f844cea2f87f50152665bcbc2c279d8d70","0x50b7545627a5162f82a992c33b87adc75187b218"]
    list_pool_adrs = ["0x9ee0a4e21bd333a6bb2ab298194320b8daa26516", "0x0e0100ab771e9288e0aa97e11557e6654c3a9665", "0xf4003f4efbe8691b60249e6afbd307abe7758adb"]
    #WBTCvETH_Uniswap_adrs = "0xcbcdf9626bc03e24f779434178a73a0b4bad62ed"
    #WBTCvETH_Uniswap_Pool = Avalanche_Pool(WBTCvETH_Uniswap_adrs,"ABIs\ABI_Uniswap.json","ABIs\ABI_ERC20.json","https://nd-072-228-848.p2pify.com/3f7a80739e2f6739cae0256a2660725b" ) 

    list_token =[]
    list_pool =[]
    for adrs in list_token_adrs : 
        list_token.append(ERC20Token(adrs))
    for adrs in list_pool_adrs : 
        list_pool.append(Avalanche_Pool(adrs))

    
    Wallet_adrs = "0x0d0707963952f2fba59dd06f2b425ace40b492fe"
    Wallet_GateIO =  Wallet(Wallet_adrs, list_token)
    #print(Wallet_GateIO.getAllBalances())
    getBestArbitrage(list_pool)

def save_data(API,filename="data_binance"):
    s = shelve.open(filename)
    s['Dates']= [API.start,API.end]
    s['data'] = API.full_data.to_json()
    s.close()




def main_bt():
    #API = Binance_API_data(2021,2022)
    #save_data(API)
    s = shelve.open("data_binance")
    data = pd.read_json(s['data'])
    print(data)
    bt = Backtest(data, Pct_Change,
                cash=100000, commission=.002,
                exclusive_orders=True)

    output = bt.run()
    bt.plot()
    print(output['_trades'])


if __name__ == "__main__":
    main_bt()