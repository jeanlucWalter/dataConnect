import math
import sys
import copy
import json

class DataTable:
  def __init__(self, jsonFileName): #fields:[{}], ids:[str], data:[[]]
      with open(jsonFileName) as jsonFile:
        data = json.load(jsonFile)
      self.ids = data["ids"]
      self.fields = data["fields"]
      self.data = data["data"]

      self.__errors = {}

  @property
  def errors(self):
    return self.__errors

  def findField(self, id:str, field:str):
    if not id in self.__errors:
      self.__errors[id] = []
    indexField = self.findByDichotomy (search = field, field = "fields")
    if type(indexField) == int:
      indexObject = self.findByDichotomy(search = id, field = "ids")
      if type(indexObject) == int:
        return self.__cleanString(self.data[indexObject][indexField])
      self.__errors[id].append("no such id")
    else:
      self.__errors[id].append("no field named : " + field)
    return None

  def findByDichotomy(self, search:str, field:str) -> int:
    return self.__findDichotomy(search=search, start=0, end=len(getattr(self, field)) - 1, field = field, data = getattr(self, field))

  def __findDichotomy(self, search:str, start:int, end:int, field:str, data:dict) -> int:
    middleIndex = (start + end) // 2
    middleValue = data[middleIndex]
    if search == middleValue:
      return self.__findDichotomyValue(middleIndex, field)
    if end - start <= 0:
      return None
    if search > middleValue:
      return self.__findDichotomy(search, middleIndex + 1, end, field, data)
    return self.__findDichotomy(search, start, middleIndex - 1, field, data)

  def __findDichotomyValue(self, index:int, field:str):
    return index


  def __cleanString(self, value):
    return value