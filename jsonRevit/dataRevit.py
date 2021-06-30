from dataBase.dataTable import DataTable

class DataRevit(DataTable):
  def __init__(self, jsonFileName):
    data = self._initCompute(jsonFileName)
    self.codes = data["codes"]
    self.__codesIndex = self.__computeInverseKeyCode (data["codesIndex"])
    self.labels = data["labels"]
    self.labelsIndex = self.__computeInverseKeyCode (data["labelsIndex"])
  
  def findListObjects(self, objectIds:'list(str)' , field = "ids") -> dict:
    ids, rowData = [], []
    for id in objectIds:
      if not id in self._errors:
        self.errors[id] = []
      indexObject = self.findByDichotomy(search = id, field = field)
      if type(indexObject) == int:
        ids.append(id)
        rowData.append(self.data[indexObject])
      else:
        self._errors[id].append("no such id")
    if len(rowData) != 0:
      return self.__findFieldsForListObjects(ids, rowData)
    return {"fields":[], field:[], "values":[]}

  def __findFieldsForListObjects(self, ids:'list(int)', rowData:list) -> dict:
    fields, fieldsDocumented, values, index = [], [], [ [] for _ in range(len(ids)) ], 0
    for index in range(len(self.fields)):
      if self.__notEmptyField(index, rowData):
        fieldsDocumented.append(index)
    for index in fieldsDocumented:
      code = self.codes[self.__codesIndex[index]]
      fields.append({"code":code, "label":self.fields[index]})
      for objectNb in range(len(ids)):
        values[objectNb].append(rowData[objectNb][index])
    return {"ids":ids, "fields":fields, "values":values}

  def __notEmptyField(self, index:int, rowData:list) -> bool:
    for line in rowData:
      if line[index]:
        return True
    return False

  def __computeInverseKeyCode (self, array):
    invKeyCodes, index = [0] * len(array), 0
    for index in range(len(array)):
      invKeyCodes[array[index]] = index
    return invKeyCodes

  