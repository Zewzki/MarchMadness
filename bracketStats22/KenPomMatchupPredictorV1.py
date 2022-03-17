from MatchupPredictor import MatchupPredictor
from Team import Team

class KenPomMatchupPredictorV1(MatchupPredictor):
    
    __adjOffEffKey = 'AdjOffEff'
    __adjDefEffKey = 'AdjDefEff'
    __nameKey = 'Team'

    __avgScore = 67.5

    # return winning team
    def predict_matchup(self, team1: Team, team2: Team):

        t1AdjOffEff = team1.get_stat(self.__adjOffEffKey)
        t1AdjDefEff = team1.get_stat(self.__adjDefEffKey)

        t2AdjOffEff = team2.get_stat(self.__adjOffEffKey)
        t2AdjDefEff = team2.get_stat(self.__adjDefEffKey)

        t1MarginalOffEff = t1AdjOffEff - 100.0
        t1MarginalDefEff = t1AdjDefEff - 100.0

        t2MarginalOffEff = t2AdjOffEff - 100.0
        t2MarginalDefEff = t2AdjDefEff - 100.0

        t1Score = (t1MarginalOffEff + t2MarginalDefEff) + self.__avgScore
        t2Score = (t2MarginalOffEff + t1MarginalDefEff) + self.__avgScore

        #print(f'{team1.get_stat(self.__nameKey)} vs. {team2.get_stat(self.__nameKey)} : {t1Score} - {t2Score}')

        if t1Score > t2Score:
            return team1
        else:
            return team2