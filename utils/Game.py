from ISerializeable import ISerializeable
import re

class Game (ISerializeable):

    __fieldRegexString = '<[a-zA-Z\d\w]*>'
    __valueRegexString = '>[a-zA-Z\d\w]<\\'

    def __init__(self):
        self.__fieldsDict = {}
    
    def add_field(self, key, val):
        if key in self.__fieldsDict:
            print(f'Key {key} already present in dictionary')
        self.__fieldsDict[key] = val
    
    def get_field(self, key):
        if key not in self.__fieldsDict:
            print(f'Key {key} not present in dictionary')
        return self.__fieldsDict[key]
    
    def serialize(self):
        s = '<Game>\n'
        for key, val in self.__fieldsDict.items():
            s += f'\t<{key}>{val}</{key}>\n'
        s += '</Game>\n'
    
    def deserialize(self, data):
        fieldPattern = re.compile(self.__fieldRegexString)
        valuePattern = re.compile(self.__valueRegexString)

        fields = fieldPattern.findall(data)
        values = valuePattern.findall(data)

        if not len(fields) == len(values):
            print(f'Error Deserializing, number of keys does not match number of values: {len(fields)} != {len(values)}')
            return
        
        for key, val in zip(fields, values):
            key = key.replace('<', '').replace('>', '')
            self.__fieldsDict[key] = val
        
        print('Completed Deserializing')
    
    def __str__(self):
        s = ''
        for key, val in self.__fieldsDict.items():
            s += f'{key}:{val}\n'
        return s

    