import requests
from utils import writeResponses,loadFile
import pandas as pd
import time

class exchanges(object):
  def __init__(self,refresh = False) -> None:
    if refresh:
      markets = {
        'binance' : self.binance(),
        'kucoin' : self.kucoin(),
        'coinbase': self.coinbase(),
        'huobi':self.huobi(),
      }

      writeResponses(markets,fileName='summaryMarkets')
      
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
    self.allSeparateSymbol = loadFile('responsesJson/separateCoins.json')
    self.allUniteSymbol = loadFile('responsesJson/uniteCoins.json')
    self.rateLimit = 1.2

  def __query(self,endpoint,parameters={}):

    head={
      'Accepts': 'application/json',
    }
    try:
      time.sleep(self.rateLimit)
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
      data=df[(df['symbol']==arg) | (df['symbol']==arg.lower())]
      #print(arg, data['id'].values) 
      yield data['id'].values  
  
  def createDataFrame(self):
    for key,value in self.allUniteSymbol.items():
      if key == 'binance+kucoin+coinbase+huobi':
        pd.DataFrame(data=self.extractInfo(*value)).to_csv('responsesJson/infoCoins.csv')
  
    
  def extractInfo(self,*symbols):
    
    info_coins=list()
    for ids in self.symbolsToIds(*symbols):
      if len(ids)==0:
        continue
      elif len(ids)>1:
        high_mcap=10000000
        selectID=None
        for i in ids:
          data=self.__query(f'coins/{i}')
          if data:
            mcap=int(data['market_cap_rank'] or 10000001)
            if mcap<high_mcap:
              selectID=i
  
      else:
        selectID=ids[0]
      print (f'add {selectID} ...')
      data=self.__query(f'coins/{selectID}')
      if data:
        info_coins.append(self.parseInfo(data=data))
      
    return info_coins

  def parseInfo(self,data={}):
    category = data['categories']
    if len(category)>=1:
      category=category[0]
    else: 
      category = None

    coin = {
      'id':str(data['id'] or None),
      'symbol':str(data['symbol'] or None),
      'name':str(data['name'] or None),
      'category':str(category or None),
      'genesis_date':str(data['genesis_date'] or None),
      'sentiment_votes_up_percentage':data['sentiment_votes_up_percentage'],
      'sentiment_votes_down_percentage':data['sentiment_votes_down_percentage'],
      'market_cap_rank':data['market_cap_rank'],
      'coingecko_score':data['coingecko_score'] ,
      'developer_score':data['developer_score'] ,
      'community_score':data['community_score'] ,
      'liquidity_score':data['liquidity_score'] ,
      'public_interest_score':data['public_interest_score'] ,
      'market_cap':data['market_data']['market_cap']['usd'],
      'total_volume':data['market_data']['total_volume']['usd'],
      'total_supply':data['market_data']['total_supply'],
      'max_supply':data['market_data']['max_supply'],
      'circulating_supply':data['market_data']['circulating_supply']
    }

    return coin

