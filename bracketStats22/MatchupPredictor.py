from abc import ABCMeta, abstractmethod
from Team import Team

class MatchupPredictor:

    @abstractmethod
    def predict_matchup(self, team1 : Team, team2 : Team) : raise NotImplementedError 