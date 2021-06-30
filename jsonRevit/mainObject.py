import jsonRevit.config as cf
from jsonRevit.dataRevit import DataRevit
import copy
import sys

class MainObject:
  def __init__(self):
    self.__config = cf.Config()
    self.__errors = {}
    self.__jsonObject = {}
    self.__usedWidth = 0.0
    self.__emptyWidth = 0.0
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
    self.__fillUpRevit(revit, self.__config.getData("compoundStructure"), systemsData)
    for key in ["WallTypes", "CeilingTypes"]:
      if not revit[key]:
        del revit[key]
    return revit

  def __fillUpRevit(self, revit:dict, compoundStructure:dict, systemData:dict):
    for systemId in systemData["ids"]:
      cStruct = copy.deepcopy(compoundStructure)
      name = self.systems.findField(systemId, cStruct["name"])
      groupIndex = self.systems.findField(systemId, "ID Groupes d'ouvrages")
      groupIndex = groupIndex if not "PLA_" in groupIndex else groupIndex.replace("PLA_", "")
      if type(name) == str:
        cStruct["name"] = name
        typeObject = "CeilingTypes" if groupIndex in ['G', 'H'] else "WallTypes"
        revit[typeObject].append(cStruct)
        self.__fillupCompoundStructure(cStruct["CompoundStructure"], systemId)

  def __fillupCompoundStructure(self, CStructElement:dict, systemId:str):
    self.__usedWidth, self.__emptyWidth = 0.0, 0.0
    for field, dictFields in self.__config.getData("idsProductCoeff").items():
      productId = self.systems.findField(systemId, field)
      position = self.systems.findField(systemId, "CompoundStructure_" + dictFields["number"])
      funct = self.systems.findField(systemId, "Function_" + dictFields["number"])
      productName = self.products.findField(productId, "Libellé long")
      if productId and position and funct and funct.replace('"', '') != "Membrane":
        element = copy.deepcopy(self.__config.getData("elementStructure"))
        CStructElement[position.replace('"', '')].append(element)
        element["Function"] = funct.replace('"', '')
        element["Material"] = productId + " - " + productName if productName else productId
        element["width"] = self.__computeWidth(systemId, productId, element, field)

  def __computeWidth(self, systemId:str, productId:str, element:dict, field:str) -> float:
    widthDefault = float(element["width"])
    groupIndex = self.systems.findField(systemId, "ID Groupes d'ouvrages")
    groupIndex = groupIndex if not "PLA_" in groupIndex else groupIndex.replace("PLA_", "")
    if groupIndex == "C" and field == "Vide de construction":
      width = self.systems.findField(systemId, "Épaisseur de l'isolant couche 1 (mm)")
      return self.__widthValueMessage(width, systemId, "no 'Épaisseur de l'isolant couche 1 (mm)'", widthDefault, thousand = True)
    elif groupIndex == "C" and field == "Plaque intérieure - Face 1":
      width = self.products.findField(productId, "Epaisseur de la plaque (m)")
      return self.__widthValueMessage(width, systemId, "no 'Epaisseur de la plaque (m)' for {}".format(productId), widthDefault)
    elif groupIndex == "C" and field == "Mortier adhésif ou colle":
      width = self.systems.findField(systemId, "Width_22")
      element["Function"] = "Finish1"
      return self.__widthValueMessage(width, systemId, "Width_22' has no float value", widthDefault)
    elif element["Material"][:6] ==  "Z01.01" and field == "Vide de construction":
      emptyWidth = self.systems.findField(systemId, "Épaisseur totale du système (mm)")
      self.__emptyWidth = float(emptyWidth) if emptyWidth and type(emptyWidth) in [str, int] and type(float(emptyWidth)) == float else 0.0
      if not self.__emptyWidth:
        self.__addError(systemId, "field 'Épaisseur totale du système (mm)' has no value, default value used {}".format(str(widthDefault))
      print("last elif", productId, element["Material"][:6])
    return widthDefault

  def __widthValueMessage(self, width:str, systemId:str, message:str, widthDefault:float, thousand = False) -> float:
    if width:
      coef = 1000.0 if thousand else 1
      self.__usedWidth += float(width) / coef
      return float(width) / coef
    self.__addError(systemId, message + ", default value used {}".format(str(widthDefault)))
    return widthDefault

  def __addError(self, systemId:str, message:str):
    if not systemId in self.__errors:
      self.__errors[systemId] = []
    self.__errors[systemId].append(message)



  



  

