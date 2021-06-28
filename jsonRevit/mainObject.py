import jsonRevit.config as cf
import json

class MainObject:
  def __init__(self):
    self.__config = cf.Config()
    self.__errors = {}
    print("mainObject created")