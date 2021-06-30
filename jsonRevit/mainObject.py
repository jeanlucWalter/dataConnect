import jsonRevit.config as cf
from jsonRevit.dataRevit import DataRevit
import copy
import sys

class MainObject:
  def __init__(self):
    self.__config = cf.Config()
    self.__errors = {}
    self.__jsonObject = {}
    for typeObject in ["system", "product"]:
      fileName = self.__config.getData("jsonName")[typeObject]
      self.__jsonObject[typeObject] = DataRevit(fileName)

  @property
  def products(self):
    return self.__jsonObject["product"]

  @property
  def systems(self):
    return self.__jsonObject["system"]

  def generateJson(self, listIdSystem:dict) -> dict:
    systemsData = self.systems.findListObjects(listIdSystem["systems"])
    listIdProducts = self.__computeListProducts(systemsData["ids"], listIdSystem["products"])
    self.__errors = copy.copy(self.systems.errors)
    productsData = self.products.findListObjects(listIdProducts)
    revit = self.__computeRevit(systemsData, productsData)
    return {"systems":systemsData, "products":productsData, "revit":revit, "errors":self.__errors}

  def __computeListProducts(self, listIdSystems:'list(str)', listIdProducts:'list(str)') -> 'list(str)':
    listIdProducts = copy.copy(listIdProducts)
    for systemId in listIdSystems:
      for field in self.__config.getData("idsProduct"):
        productId = self.systems.findField(systemId, field)
        if productId:
          if not self.products.findByDichotomy(productId, "ids"):
            self.__addError(systemId, "product Id {} does not exist".format(productId))
          elif not productId in listIdProducts:
            listIdProducts.append(productId)
    return listIdProducts

  def __computeRevit(self, systemsData:dict, productsData:dict) -> dict:
    revit = copy.deepcopy(self.__config.getData("revit"))
    self.fillUpRevit(revit, self.__config.getData("compoundStructure"), systemsData)
    for key in ["WallTypes", "CeilingTypes"]:
      if not revit[key]:
        del revit[key]
    return revit

  def fillUpRevit(self, revit:dict, compoundStructure:dict, systemData:dict):
    for systemId in systemData["ids"]:
      cStruct = copy.deepcopy(compoundStructure)
      name = self.systems.findField(systemId, cStruct["name"])
      groupIndex = self.systems.findField(systemId, "ID Groupes d'ouvrages")
      groupIndex = groupIndex if not "PLA_" in groupIndex else groupIndex.replace("PLA_", "")
      if type(name) == str:
        cStruct["name"] = name
        typeObject = "CeilingTypes" if groupIndex in ['G', 'H'] else "WallTypes"
        revit[typeObject].append(cStruct)
        self.fillupCompoundStructure(cStruct["CompoundStructure"], systemId)

  def fillupCompoundStructure(self, CStructElement, systemId):
    for field, dictFields in self.__config.getData("idsProductCoeff").items():
      # print(field)
      productId = self.systems.findField(systemId, field)
      if productId:
        element = copy.deepcopy(self.__config.getData("elementStructure"))
        position = self.systems.findField(systemId, "CompoundStructure_" + dictFields["number"]).replace('"', '')
        CStructElement[position].append(element)
        element["Function"] = self.systems.findField(systemId, "Function_" + dictFields["number"]).replace('"', '')
        element["Material"] = self.products.findField(productId, "Libellé long")
        # print(systemId, field, dictFields, productId)
        print(position, CStructElement[position], element)
        # print()
    #     print()
    # sys.exit()


  def __addError(self, systemId:str, message:str):
    if not systemId in self.__errors:
      self.__errors[systemId] = []
    self.__errors[systemId].append(message)



  



  

