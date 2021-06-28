import jsonRevit.config as cf
from jsonRevit.dataRevit import DataRevit
import json

class MainObject:
  def __init__(self):
    self.__config = cf.Config()
    self.__errors = {}
    self.__jsonObject = {}
    for target in ["Etude", "Exe", "Gaia"]:
      self.__jsonObject[target] = {}
      for typeObject in ["system", "product"]:
        fileName = self.__config.getData("jsonName")[typeObject][target]
        self.__jsonObject[target][typeObject] = DataRevit(fileName)
    # print(self.__jsonObject["Etude"]["product"].findField('A01.01.000_PL.20.1', 'Nom'), self.__jsonObject["Etude"]["product"].errors)

  @property
  def products(self):
    return self.__jsonObject["Gaia"]["product"]

  @property
  def systems(self):
    return self.__jsonObject["Gaia"]["system"]

  def generateJson(self, listIdSystem):
    
    return False