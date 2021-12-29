from markets import exchanges, coinGecko
from data import coins
if __name__ == '__main__':
  #exchanges(refresh=True)
  #print(exchanges().huobi())
  """
  coin =coins(refresh=True)
  coin.uniteCoins()
  coin.separateCoins()
  """
  
  coinGecko().createDataFrame()
  #print(coins().uniteCoins(others=['kucoin','huobi','coinbase']))
