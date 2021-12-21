import requests
import json
import os

class Markets(object):
  def __init__(self,refresh = False) -> None:
    if refresh:
      markets = {
        'binance' : self.binance(),

      }

      self.__writeResponses(markets,fileName='summaryMarkets')
      
  def __query(self, url, params = {}, header = {}):
    try:
      response = requests.get(url,params=params,headers=header)

      if response.status_code == 200:
        return response.json()
      
      else:
        print(f'error: {response.status_code}')
        return {}
    except Exception as e:
      print(e)

  def __writeResponses(self,data,fileName='test'):
    
    if not os.path.isdir('./responsesJson'):
      os.mkdir('./responsesJson')

    with open(f'responsesJson/{fileName}.json','w') as f:
      json.dump(data,f,indent=2)
  
  def binance(self,**kwargs):
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
    self.__writeResponses(data,fileName='binanceMarketStats')

    #filter
    symbols = [s['baseAsset'] for s in data['symbols'] if s['status']!= 'BREAK']
    
    return list(set(symbols))
