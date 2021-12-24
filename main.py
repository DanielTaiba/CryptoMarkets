from exchanges import Markets, coinGecko
from data import stats
if __name__ == '__main__':
  #Markets(refresh=True)
  #print(Markets().huobi())
  #coinGecko().coinList()
  print(stats().uniteCoins(others=['kucoin','huobi','coinbase']))