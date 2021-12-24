from markets import exchanges, coinGecko
from data import coins
if __name__ == '__main__':
  #exchanges(refresh=True)
  #print(exchanges().huobi())
  #coinGecko().coinList()
  print(coins().uniteCoins(others=['kucoin','huobi','coinbase']))