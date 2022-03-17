from __future__ import division
from BracketEvaluator import BracketEvaluator
from DataLoader import DataLoader
from KenPomDataLoader import KenPomDataLoader
from BracketLoader import BracketLoader
from KenPomMatchupPredictorV1 import KenPomMatchupPredictorV1
from MatchupPredictor import MatchupPredictor
from AllGameEloDataLoader import AllGameEloDataLoader
from EloMatchupPredictor import EloMatchupPredictor

class BracketPredictor:

    __nameKey = 'Team'

    def __init__(self, bracketLoader, dataLoader : DataLoader, matchupPredictor : MatchupPredictor, outputPath : str):
        self.__bracketLoader = bracketLoader
        self.__dataLoader = dataLoader
        self.__matchupPredictor = matchupPredictor

        self.__outputPath = outputPath

        self.__teamDict = {}
        self.__bracket = []
    
    def load(self, dataPath, bracketPath):
        self.__teamDict = self.__dataLoader.load_data(dataPath)
        self.__bracket = self.__bracketLoader.load_bracket(bracketPath)

        #for teamName in self.__teamDict:
        #    print(self.__teamDict[teamName])
    
    def predict_bracket(self):

        divisionWinners = []

        with open(self.__outputPath, 'w') as f:
        
            for i, matchupList in enumerate(self.__bracket):

                divisionName = 'defaultDivisionName'

                if i == 0:
                    divisionName = 'West'
                elif i == 1:
                    divisionName = 'East'
                elif i == 2:
                    divisionName = 'South'
                elif i == 3:
                    divisionName = 'Midwest'

                f.write(f'{divisionName}\n')

                #print(f'{divisionName}\n{matchupList}')

                while len(matchupList) > 1:
                    team1 = self.__teamDict[matchupList.pop(0)]
                    team2 = self.__teamDict[matchupList.pop(0)]
                    winner = self.__matchupPredictor.predict_matchup(team1, team2)
                    
                    #print(f'{team1.get_stat(self.__nameKey)} vs {team2.get_stat(self.__nameKey)} -> {winner.get_stat(self.__nameKey)}')
                    
                    matchupList.append(winner.get_stat(self.__nameKey))
                    f.write(f'{team1.get_stat(self.__nameKey)} vs. {team2.get_stat(self.__nameKey)} --> {winner.get_stat(self.__nameKey)}\n')
            
                divisionWinners.append(matchupList.pop())
                f.write('\n')
            

            westChamp = self.__teamDict[divisionWinners.pop()]
            southChamp = self.__teamDict[divisionWinners.pop()]
            eastChamp = self.__teamDict[divisionWinners.pop()]
            midwestChamp = self.__teamDict[divisionWinners.pop()]

            leftHandWinner = self.__matchupPredictor.predict_matchup(westChamp, southChamp)
            f.write(f'{westChamp.get_stat(self.__nameKey)} vs. {southChamp.get_stat(self.__nameKey)} --> {leftHandWinner.get_stat(self.__nameKey)}\n')

            rightHandWinner = self.__matchupPredictor.predict_matchup(eastChamp, midwestChamp)
            f.write(f'{eastChamp.get_stat(self.__nameKey)} vs. {midwestChamp.get_stat(self.__nameKey)} --> {rightHandWinner.get_stat(self.__nameKey)}\n')

            champion = self.__matchupPredictor.predict_matchup(leftHandWinner, rightHandWinner)
            f.write(f'{leftHandWinner.get_stat(self.__nameKey)} vs. {rightHandWinner.get_stat(self.__nameKey)} --> {champion.get_stat(self.__nameKey)}\n')

        print('Evaluation Complete')

    def teams_to_string(self):
        s = ''
        for team in self.__teamList:
            s += str(team) + '\n'
        return s

if __name__ == '__main__':

    dataPath = 'data/raw/kenPom/kenPomData22.txt'
    bracketPath = 'data/raw/brackets/bracket22.txt'
    outputPath = 'data/output/bracket22Prediction.txt'
    #truthPath = 'data/raw/brackets/bracket21Results.txt'

    #dataPath = 'data/raw/gameData/allGames21.txt'
    #bracketPath = 'data/raw/brackets/bracket21Rename.txt'
    #outputPath = 'data/output/bracket21EloPrediction.txt'
    #truthPath = 'data/raw/brackets/bracket21ResultsRename.txt'
    #translationTablePath = 'data/resources/translationTableV1.txt'

    be = BracketEvaluator()

    kpdl = KenPomDataLoader()
    bl = BracketLoader()
    kpmp = KenPomMatchupPredictorV1()

    #agedl = AllGameEloDataLoader(translationTablePath)
    #emp = EloMatchupPredictor()

    bp = BracketPredictor(bl, kpdl, kpmp, outputPath)
    bp.load(dataPath, bracketPath)
    bp.predict_bracket()

    #result, totalGames = be.evaluate_bracket(outputPath, truthPath)
    #print(f'Num of Correct Predictions: {result} of {totalGames} games')