from DataLoader import DataLoader
from Team import Team
from Translator import Translator

class AllGameEloDataLoader(DataLoader):

    __homeIdIndex = 3
    __awayIdIndex = 4

    __homeScoreIndex = 5
    __awayScoreIndex = 6

    __homeIdKey = 'HomeTeamId'
    __awayIdKey = 'AwayTeamId'

    __nameKey = 'Team'
    __eloKey = 'ELO'
    __gameCountKey = 'GameCount'

    __stringDelim = ','

    __defaultELO = 1300.0

    __kFactor = 20.0
    
    def __init__(self, translationTablePath):
        self.__keyList = []
        self.__translator = Translator(translationTablePath)

    def load_data(self, dataPath):

        print('Loading Game Data')

        teams = {}
        dataLines = []

        with open(dataPath, 'r') as f:
            dataLines = f.readlines()
        
        for i, line in enumerate(dataLines):

            line = line.replace('\n', '')
            items = self.parse_string(line)

            if i == 0:
                self.keyList = items
                continue
            
            homeName = self.__translator.idToName(items[3])
            awayName = self.__translator.idToName(items[4])

            # add home team if not present
            if homeName not in teams.keys():
                newTeam = Team()
                newTeam.add_stat(self.__nameKey, homeName)
                newTeam.add_stat(self.__eloKey, self.__defaultELO)
                newTeam.add_stat(self.__gameCountKey, 0)
                teams[homeName] = newTeam
            
            # add away team if not preset
            if awayName not in teams.keys():
                newTeam = Team()
                newTeam.add_stat(self.__nameKey, awayName)
                newTeam.add_stat(self.__eloKey, self.__defaultELO)
                newTeam.add_stat(self.__gameCountKey, 0)
                teams[awayName] = newTeam
            
            # select home and away team records

            t1 = teams[homeName]
            t2 = teams[awayName]

            t1Elo = t1.get_stat(self.__eloKey)
            t2Elo = t2.get_stat(self.__eloKey)

            homeScore = int(items[self.__homeScoreIndex])
            awayScore = int(items[self.__awayScoreIndex])

            # 1 = homeWins, 0 = Tie, -1 = awayWins
            winner = 0
            if homeScore > awayScore:
                winner = 1
            elif awayScore > homeScore:
                winner = -1

            t1EloUpdate, t2EloUpdate = self.calculate_updated_elos(t1Elo, t2Elo, winner)

            t1.update_stat(self.__eloKey, t1Elo + t1EloUpdate)
            t2.update_stat(self.__eloKey, t2Elo + t2EloUpdate)

            t1.update_stat(self.__gameCountKey, t1.get_stat(self.__gameCountKey) + 1)
            t2.update_stat(self.__gameCountKey, t2.get_stat(self.__gameCountKey) + 1)

            teams[homeName] = t1
            teams[awayName] = t2
        
        print('Done Loading Game Data')
        return teams

    # winner: 1 = homeWins, 0 = Tie, -1 = awayWins
    def calculate_updated_elos(self, t1Elo : float, t2Elo : float, winner : int):

        p1 = t1Elo / (t1Elo + t2Elo)
        p2 = t2Elo / (t1Elo + t2Elo)

        u1 = 1 / (1 + 10 ** ((t2Elo - t1Elo) / 400))
        u2 = 1 / (1 + 10 ** ((t1Elo - t2Elo) / 400))

        e1Update = self.__kFactor * (winner - u1)
        e2Update = self.__kFactor * ((not winner) - u2)

        return e1Update, e2Update
    
    def parse_string(self, dataString):
        return dataString.split(self.__stringDelim)
            

