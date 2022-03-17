from Team import Team
from DataLoader import DataLoader

class KenPomDataLoader(DataLoader):

    __nameKey = 'Team'

    __stringDelim = ','

    def __init__(self):
        self.__keyList = []
    
    def load_data(self, dataPath):

        teamList = {}

        dataLines = []

        with open(dataPath, 'r') as f:

            dataLines = f.readlines()
        
        for i, line in enumerate(dataLines):

                line = line.replace('\n', '')

                items = self.parse_string(line)
                
                if i == 0:
                    self.__keyList = items
                    continue
                
                newTeam = Team()
                newTeam.add_all(self.__keyList, items)
                teamList[newTeam.get_stat(self.__nameKey)] = newTeam
        
        return teamList
    
    def parse_string(self, dataString):
        return dataString.split(self.__stringDelim)
