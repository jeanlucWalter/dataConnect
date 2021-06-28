from os.path import isfile
import json

class Config:
  __fileConfigName:str = "jsonRevit/config.json"
  __data:dict = {}

  def __init__(self):
    if not isfile(self.__fileConfigName):
      print("json config created")
      self.__createJson()
    with open(self.__fileConfigName) as jsonFile:
      self.__data = json.load(jsonFile)

  def getData (self, key):
    if key in self.__data:
      return self.__data[key]
    print ("error config getData key {} does not exist\r\n".format(key))

  def __createJson(self):
    data:dict = {
      "target":"Etude",
      "jsonName":{
        "system":{"Exe":"dataBase/Data/systemExe.json", "Etude":"dataBase/Data/systemEtude.json", "Gaia":"dataBase/Data/systemGaia.json"},
        "product":{"Exe":"dataBase/Data/productExe.json", "Etude":"dataBase/Data/productEtude.json", "Gaia":"dataBase/Data/productGaia.json"}
        }
    }
    with open(self.__fileConfigName, 'w') as jsonFile:
      json.dump(data, jsonFile, indent = 3)
