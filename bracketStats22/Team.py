
class Team:

    __stringTypeKeys = ['Team', 'Conf', 'W-L']
    __intTypeKeys = ['Rank']
    __floatTypeKeys = ['AdjEffMar', 'AdjOffEff', 'AdjDefEff', 'AdjTemp', 'Luck', 'StrOfSch', 'OppOffEff', 'OppDefEff', 'NonConfStrOfSch']

    def __init__(self):
        self.__statDict = {}
    
    def get_dict(self):
        return self.__statDict
    
    def get_stat(self, key):
        if key not in self.__statDict.keys():
            print(f'Key "{key}" not present in dictionary')
            return None
        return self.__statDict[key]
    
    def update_stat(self, key, newVal):
        if key not in self.__statDict.keys():
            print(f'Key "{key}" not present in dictionary')
            return None
        self.__statDict[key] = newVal
    
    def add_all(self, keys, vals):
        for i, key in enumerate(keys):
            self.add_stat(key, vals[i])
    
    def add_stat(self, key, val):
        self.__statDict[key] = self.recast_value(key, val)

    def recast_value(self, key, val):
        v = val
        if key in self.__stringTypeKeys:
            v = str(v)
        elif key in self.__intTypeKeys:
            v = int(v)
        elif key in self.__floatTypeKeys:
            v = float(v)
        return v
    
    def __str__(self):
        s = ''
        for key in self.__statDict:
            s += f'{key}:{self.__statDict[key]}, '
        return s

