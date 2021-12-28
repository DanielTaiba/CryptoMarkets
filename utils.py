import os
import json
def writeResponses(data,fileName='test') -> None:
    if not os.path.isdir('./responsesJson'):
      os.mkdir('./responsesJson')

    with open(f'responsesJson/{fileName}.json','w') as f:
      json.dump(data,f,indent=2)

def loadFile(path)-> dict:
    with open(path,'r') as f:
      return json.load(f)