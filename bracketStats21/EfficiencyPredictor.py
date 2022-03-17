from PredictorInterface import PredictorInterface

class EfficiencyPredictor(PredictorInterface):

	__avgScore = 67.5

	def __init__(self, offEffPath, defEffPath):
		
		self.__offensiveEfficiency = {}
		self.__defensiveEfficiency = {}

		oe = open(offEffPath, 'r')
		lines = oe.readlines()

		for line in lines:
			line = line.replace('\n', '')
			split = line.split(':')
			self.__offensiveEfficiency[split[0]] = float(split[1])

		oe.close()

		de = open(defEffPath, 'r')
		lines = de.readlines()

		for line in lines:
			line = line.replace('\n', '')
			split = line.split(':')
			self.__defensiveEfficiency[split[0]] = float(split[1])

		de.close()

	def predict(self, leftName, rightName):

		leftOff = None
		leftDef = None

		rightOff = None
		rightDef = None

		try:
			leftOff = self.__offensiveEfficiency[leftName]
			leftDef = self.__defensiveEfficiency[leftName]
		except KeyError:
			print('Unrecognized Team: %s' % leftName)
			return None, (None, None)

		try:
			rightOff = self.__offensiveEfficiency[rightName]
			rightDef = self.__defensiveEfficiency[rightName]
		except KeyError:
			print('Unrecognized Team: %s' % rightName)
			return None, (None, None)

		leftOffAbs = leftOff - 1.0
		leftDefAbs = 1.0 - leftDef

		rightOffAbs = rightOff - 1.0
		rightDefAbs = 1.0 - rightDef

		predLeftScore = (1.0 + (leftOffAbs - rightDefAbs)) * self.__avgScore
		predRightScore = (1.0 + (rightOffAbs - leftDefAbs)) * self.__avgScore

		winningTeam = 'Tie'
		if predLeftScore > predRightScore:
			winningTeam = leftName
		elif predLeftScore < predRightScore:
			winningTeam = rightName

		return winningTeam, (predLeftScore, predRightScore)

if __name__ == '__main__':

	offEffPath = 'data/cleaned/cleanedOffensiveEfficiency.txt'
	defEffPath = 'data/cleaned/cleanedDefensiveEfficiency.txt'

	ep = EfficiencyPredictor(offEffPath, defEffPath)

	t1 = 'Kansas'
	t2 = 'E Washington'

	winner, score = ep.predict(t1, t2)

	print('%s: %f - %f' % (winner, score[0], score[1]))