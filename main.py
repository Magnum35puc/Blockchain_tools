from Pool import Avalanche_Pool




def main():
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

    
if __name__ == "__main__":
    main()