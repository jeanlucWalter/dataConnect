import jsonRevit.mainObject as mo
import sys
import json

index, param, key = 1, {}, "undefined"
if len(sys.argv) >= 2:
  while index < len(sys.argv):
    if index % 2 == 1:
      key = sys.argv[index]
    else:
      param[key] = sys.argv[index]
    index += 1

listIdSystem = {
  "systems":[
    "P_E01.01.05.A01.D.V20.1",
    "P_E01.01.05.A01.A.V20.1",
    "P_C17.02.01.A01.0.V20.1",
    "P_C17.02.01.A01.D.V20.1" #"P_A16.01.01.A05.0.V20.1", "P_A01.02.03.A02.0.V20.1", "P_C15.02.01.A01.0.V20.1", "P_C17.01.01.A01.0.V20.1", "P_C17.01.01.A01.B.V20.1"
  ],
  "products": []}
main = mo.MainObject ()
if "generateJson" in param:
  data = main.generateJson(listIdSystem)
  with open("Result/jsonRevit.json", 'w') as jsonFile:
      json.dump(data, jsonFile, indent = 3)
  print("json saved in Result/jsonRevit.json")