from os.path import isfile
import json

class Config:
  __fileConfigName:str = "jsonRevit/config.json"
  __data:dict = {}

  def __init__(self):
    if not isfile(self.__fileConfigName):
      print("json config created")
      self.__createJson()
    print("read json config")


  def __createJson(self):
    data:dict = {
      "target":"Etude"
    }
    with open(self.__fileConfigName, 'w') as jsonFile:
      json.dump(data, jsonFile, indent = 3)
