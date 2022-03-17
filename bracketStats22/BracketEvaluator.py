

from numpy import empty_like


class BracketEvaluator:

    def evaluate_bracket(self, bracketPredictionPath, bracketTruthPath):

        predictionLines = []
        truthLines = []

        with open(bracketPredictionPath, 'r') as f:
            predictionLines = f.readlines()
        
        with open(bracketTruthPath, 'r') as f:
            truthLines = f.readlines()
        
        if not len(predictionLines) == len(truthLines):
            print('Error in provided bracket(s)')
            return
        
        dualLines = zip(predictionLines, truthLines)

        correctPredictions = 0
        totalGames = 0

        for line in dualLines:
            pred = line[0].strip()
            truth = line[1].strip()

            if (not pred) or (not truth):
                continue
            
            totalGames += 1

            if pred == truth:
                correctPredictions += 1
        
        return correctPredictions, totalGames

if __name__ == '__main__':

    predictionPath = 'data/output/output.txt'
    truthPath = 'data/raw/bracket21Results.txt'

    be = BracketEvaluator()
    result, totalGames = be.evaluate_bracket(predictionPath, truthPath)
    print(f'Num of Correct Predictions: {result} of {totalGames} games')