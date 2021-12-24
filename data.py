import json
from markets import exchanges
from itertools import combinations

class coins():
  def __init__(self,refresh=False) -> None:
    self.currencies = exchanges(refresh=refresh)
    self.infoPath = 'responsesJson/summaryMarkets.json'
    self.coinsByExchange = self.__loadFile(self.infoPath)

  def __loadFile(self,path)-> dict:
    with open(path,'r') as f:
      return json.load(f)

  def __comb(self,lista ) -> list:
    combinaciones=list()
    for i in range (1,len (lista)+1):
      for c in combinations(lista,i):
        combinaciones.append(list(c))
    return combinaciones
  
  def __conjunction(self,*argv)-> set:
    result = []
    for arg in argv:
      result= result+self.coinsByExchange[arg]
    return set(result)
  
  def __intersection(self,key,*argv)->set:
    return set(self.coinsByExchange[key]).intersection(self.__conjunction(*argv))

  def separateCoins(self, exchange ='binance', others = ['kucoin'])-> dict:
    result = dict()    
    for comb in self.__comb(others):
      name='+'.join(comb)
      result[exchange+'-('+name+')']=set(self.coinsByExchange[exchange]) - self.__intersection(exchange,*comb)
    return result
    
  def uniteCoins(self, exchange ='binance', others = ['kucoin'])-> dict:
    result = dict()    
    for comb in self.__comb(others):
      name='+'.join(comb)
      result[exchange+'+'+name]= self.__intersection(exchange,*comb)
    return result
