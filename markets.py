import requests
from utils import writeResponses,loadFile
import pandas as pd

class exchanges(object):
  def __init__(self,refresh = False) -> None:
    if refresh:
      markets = {
        'binance' : self.binance(),
        'kucoin' : self.kucoin(),
        'coinbase': self.coinbase(),
        'huobi':self.huobi(),
      }

      self.__writeResponses(markets,fileName='summaryMarkets')
      
  def __query(self, url, params = {}, header = {}) -> dict:
    try:
      response = requests.get(url,params=params,headers=header)

      if response.status_code == 200:
        return response.json()
      
      else:
        print(f'error: {response.status_code}')
        return {}
    except Exception as e:
      print(e)
  
  def binance(self,**kwargs) -> list:
    endpoint = 'https://api.binance.com/api/v3/exchangeInfo'
    """
    **kwargs:
      - symbol: STRING -> ex: 'BTCUSDT'
      - symbols: List of STRINGs -> ex:['BTCUSDT','ETHUSDT']
    """
    parameters={
      **kwargs
      }
      
    header={
      'Accepts': 'application/json',
    }

    data = self.__query(endpoint,params=parameters,header=header)
    writeResponses(data,fileName='binanceCurrencies')

    #filter
    symbols = [s['baseAsset'] for s in data['symbols'] if s['status']!= 'BREAK']
    
    return list(set(symbols))

  def kucoin(self) -> list:
    endpoint = 'https://openapi-sandbox.kucoin.com/api/v1/currencies'
    header={
      'Accepts': 'application/json',
    }

    data = self.__query(endpoint,header=header)
    writeResponses(data,fileName='kucoinCurrencies')

    #filter
    symbols = [s['name'] for s in data['data']]
    return list(set(symbols))
  
  def coinbase(self):
    endpoint = 'https://api.exchange.coinbase.com/currencies'
    header={
      'Accepts': 'application/json',
    }

    data = self.__query(endpoint,header=header)
    writeResponses(data,fileName='coinbaseCurrencies')

    #filter
    symbols = [s['id'] for s in data if s['details']['type'] == 'crypto']
    return list(set(symbols))

  def huobi(self):
    endpoint = 'https://api.huobi.pro/v1/common/symbols'
    header={
      'Accepts': 'application/json',
    }

    data = self.__query(endpoint,header=header)
    writeResponses(data,fileName='huobiCurrencies')

    #filter
    symbols = [s['base-currency'].upper() for s in data['data'] if s['state'] == 'online']
    return list(set(symbols))

class coinGecko(object):
  def __init__(self) -> None:
    self.url = 'https://api.coingecko.com/api/v3/'

  def __query(self,endpoint,parameters={}):
    head={
      'Accepts': 'application/json',
    }
    try:
      r =requests.get(self.url+endpoint,params=parameters,headers=head)

      if r.status_code==200:
        return r.json()
      
      else:
        print(r.status_code)
        return {}

    except Exception as e :
      print(e)
      exit()

  def coinList(self):
    endpoint ='coins/list'
    p={
      'include_platform':True,
    }
    data = self.__query(endpoint,parameters=p)
    pd.DataFrame(data=data).to_csv('responsesJson/coinList.csv')

  def symbolsToIds(self,*args) :
    df = pd.read_csv('responsesJson/coinList.csv')
    
    for arg in args:
      arg.lower()
      data=df[df['symbol']==arg]
      yield data['id'].values
      #self.coinInformation(ids=data['id'].values[-1])
      

  def coinInformation(self,ids='bitcoin',**kwargs):
    endpoint=f'coins/{ids}'
    p={
      **kwargs
    }
    return self.__query(endpoint,parameters=p)
    
  
  def extractInfo(self):
    symbols = ('btc','eth','ada')
    
    for ids in self.symbolsToIds(*symbols):
      if len(ids)>1:
        high_mcap=10000000
        selectID=None
        for i in ids:
          data=self.__query(f'coins/{i}')
          mcap=int(data['market_cap_rank'] or 10000001)
          if mcap<high_mcap:
            selectID=i
  
      else:
        selectID=ids[0]
      
      writeResponses(data=self.__query(f'coins/{selectID}'),fileName=f'CG_{selectID}')



