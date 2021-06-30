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
      "jsonName":{
        "system":"dataBase/Data/systemGaia.json",
        "product":"dataBase/Data/productGaia.json"
        },
      "revit" : {"SystemsGroup":"A", "LengthUnits":"meters", "WallTypes":[], "CeilingTypes":[]},
      "compoundStructure":{"name":"Nom de l'ouvrage", "CompoundStructure":{"Exterior":[], "Structure":[], "Interior":[]}},
      "elementStructure":{"Function":False, "Material":False, "width":0.0125, "StructuralMaterial":False},
      "CompoundFields":["CompoundStructure", "Function"],
      "idsProduct": [
        "Enduit \u00e0 joints - Face 1",
        "Bande \u00e0 joints - Face 1",
        "Vis couche 3 - Face 1",
        "Vis couche 2 - Face 1",
        "Vis couche 1 - Face 1",
        "Plaque ext\u00e9rieure - Face 1",
        "Plaque du milieu - Face 1",
        "Plaque int\u00e9rieure - Face 1",
        "Vide de construction",
        "Isolant couche 1",
        "Isolant couche 2",
        "Rail bas",
        "Rail haut, semelle ou lisse",
        "Ossature horizontale compl\u00e9mentaire",
        "Ossature verticale 1",
        "Ossature verticale 2",
        "Suspentes ou appuis",
        "Vis autoforeuses",
        "Pointes pour cloueur ou chevilles",
        # "Polyane pied de cloison ou U plastique",
        "Bande r\u00e9siliente",
        "Mortier adh\u00e9sif ou colle",
        "Mat\u00e9riaux divers 1",
        "Mat\u00e9riaux divers 2",
        "Mat\u00e9riaux divers 3",
        "Plaque int\u00e9rieure - Face 2",
        "Plaque du milieu - Face 2",
        "Plaque ext\u00e9rieure - Face 2",
        "Vis couche 1 - Face 2",
        "Vis couche 1 - Face 2",
        "Vis couche 2 - Face 2",
        "Vis couche 3 - Face 2",
        "Bande \u00e0 joints - Face 2",
        "Enduit \u00e0 joints - Face 2"
      ],
      "idsProductCoeff": {
        "Enduit à joints - Face 1":{"ratio":"Ratio enduit à joints - Face 1", "number":"1"},
        "Bande à joints - Face 1":{"ratio": "Ratio bande à joints - Face 1", "number":"2"},
        "Vis couche 3 - Face 1":{"ratio": "Ratio vis couche 3 - Face 1", "number":"3"},
        "Vis couche 2 - Face 1":{"ratio": "Ratio vis couche 2 - Face 1", "number":"4"},
        "Vis couche 1 - Face 1":{"ratio": "Ratio vis couche 1 - Face 1", "number":"5"},
        "Plaque extérieure - Face 1":{"ratio": "Coef de chute de toutes les plaques du système", "number":"6"},
        "Plaque du milieu - Face 1":{"ratio": "Coef de chute de toutes les plaques du système", "number":"7"},
        "Plaque intérieure - Face 1":{"ratio": "Coef de chute de toutes les plaques du système", "number":"8"},
        "Vide de construction":{"ratio": "Coef de chute de toutes les plaques du système", "number":"9"},
        "Isolant couche 1":{"ratio": "Ratio isolant toutes couches", "number":"10"},
        "Isolant couche 2":{"ratio": "Ratio isolant toutes couches", "number":"11"},
        "Rail bas":{"ratio": "Ratio rail bas", "number":"12"},
        "Rail haut, semelle ou lisse":{"ratio": "ratio rail haut, semelle ou lisse", "number":"13"},
        "Ossature horizontale complémentaire":{"ratio": "Ratio ossature horizontale complémentaire", "number":"14"},
        "Ossature verticale 1":{"ratio": "Ratio ossature verticale 1", "number":"15"},
        "Ossature verticale 2":{"ratio": "Ratio ossature verticale 2", "number":"16"},
        "Suspentes ou appuis":{"ratio": "Ratio suspentes ou appuis", "number":"17"},
        "Vis autoforeuses":{"ratio": "Ratio vis autoforeuse", "number":"18"},
        "Pointes pour cloueur ou chevilles":{"ratio": "Ratio pointes pour cloueur ou chevilles", "number":"19"},
        # "Polyane pied de cloison ou U plastique":{"ratio": "Ratio polyane pied de cloison ou U plastique", "number":"20"},
        "Bande résiliente":{"ratio": "Ratio bande résiliente", "number":"21"},
        "Mortier adhésif ou colle":{"ratio": "Ratio mortier adhésif ou colle", "number":"22"},
        "Matériaux divers 1":{"ratio": "Ratio matériaux divers 1", "number":"23"},
        "Matériaux divers 2":{"ratio": "Ratio matériaux divers 2", "number":"24"},
        "Matériaux divers 3":{"ratio": "Ratio matériaux divers 3", "number":"25"},
        "Plaque intérieure - Face 2":{"ratio": "Coef de chute de toutes les plaques du système", "number":"26"},
        "Plaque du milieu - Face 2" :{"ratio": "Coef de chute de toutes les plaques du système", "number":"27"},
        "Plaque extérieure - Face 2":{"ratio": "Coef de chute de toutes les plaques du système", "number":"28"},
        "Vis couche 1 - Face 2":{"ratio": "Ratio vis couche 1 - Face 2", "number":"29"},
        "Vis couche 2 - Face 2":{"ratio": "Ratio vis couche 2 - Face 2", "number":"30"},
        "Vis couche 3 - Face 2":{"ratio": "Ratio vis couche 3 - Face 2", "number":"31"},
        "Bande à joints - Face 2":{"ratio": "Ratio bande à joints - Face 3", "number":"32"},
        "Enduit à joints - Face 2":{"ratio": "Ratio bande à joints - Face 3", "number":"33"}
      }
    }
    with open(self.__fileConfigName, 'w') as jsonFile:
      json.dump(data, jsonFile, indent = 3)
