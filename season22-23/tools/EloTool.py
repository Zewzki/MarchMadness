
class EloTool:

    def __init__(self, k_tiers):
        self.k_tiers = k_tiers
        self.stagedConferenceEloUpdates = {}

    def calc_score_expectation(self, elo1, elo2):
        return 1.0 / (1.0 + pow(10, ((elo2 - elo1) / 400.0)))

    def predict_matchup(self, conf_weight, team_weight, c1, t1, c2, t2):

        team1EffectiveElo = (conf_weight * c1) + (team_weight * t1)
        team2EffectiveElo = (conf_weight * c2) + (team_weight * t2)

        # could also calc just one and do 1 - expectation
        team1Expectation = self.calc_score_expectation(team1EffectiveElo, team2EffectiveElo)
        team2Expectation = self.calc_score_expectation(team2EffectiveElo, team1EffectiveElo)

        return team1Expectation, team2Expectation

    def get_outcome_by_score(self, homeScore, awayScore):

        homeOutcome = 0.5
        awayOutcome = 0.5

        if homeScore > awayScore:
            homeOutcome = 1.0
            awayOutcome = 0.0
        elif homeScore < awayScore:
            homeOutcome = 0.0
            awayOutcome = 1.0
        
        return homeOutcome, awayOutcome

    def calculate_new_elo(self, elo, expectedScore, realScore):
        return int(elo + (self.get_k(elo) * (realScore - expectedScore)))
    
    def get_k(self, elo):

        for k_tier in self.k_tiers:
            if elo >= k_tier[0] and elo < k_tier[1]:
                return k_tier[2]
        
        print(f'No valid elo range in k_tiers for elo {elo}')
        return None