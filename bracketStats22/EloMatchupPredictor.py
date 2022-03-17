from MatchupPredictor import MatchupPredictor
from Team import Team

class EloMatchupPredictor(MatchupPredictor):

    __nameKey = 'Team'
    __eloKey = 'ELO'

    def predict_matchup(self, team1: Team, team2: Team):
        r1 = team1.get_stat(self.__eloKey)
        r2 = team2.get_stat(self.__eloKey)

        p1 = r1 / (r1 + r2)
        p2 = r2 / (r1 + r2)

        #print(f'{team1.get_stat(self.__nameKey)} ({r1}, {p1}) vs. {team2.get_stat(self.__nameKey)} ({r2}, {p2})')

        if p1 >= p2:
            return team1
        else:
            return team2