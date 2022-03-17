from EfficiencyPredictor import EfficiencyPredictor

class BracketPredictor:

	offEffPath = 'cleanedOffensiveEfficiency.txt'
	defEffPath = 'cleanedDefensiveEfficiency.txt'

	def __init__(self, bracketPath):
		self.__west = []
		self.__east = []
		self.__south = []
		self.__midwest = []
		self.ep = EfficiencyPredictor(self.offEffPath, self.defEffPath)
		self.loadBracket(bracketPath)

	def loadBracket(self, bracketPath):

		f = open(bracketPath, 'r')
		lines = f.readlines()

		curr = self.__west = []

		for line in lines:
			line = line.replace('\n', '')

			if line == 'West':
				curr = self.__west
				continue
			elif line == 'East':
				curr = self.__east
				continue
			elif line == 'South':
				curr = self.__south
				continue
			elif line == 'Midwest':
				curr = self.__midwest
				continue

			split = line.split(':')
			curr.append((split[0], split[1]))

	def generatePredictions(self, outputPath):
		
		of = open(outputPath, 'w')

		self.predictSubBracket(of, self.__west, 'WEST')
		self.predictSubBracket(of, self.__south, 'SOUTH')
		self.predictSubBracket(of, self.__east, 'EAST')
		self.predictSubBracket(of, self.__midwest, 'MIDWEST')

		westChamp = self.__west[0]
		southChamp = self.__south[0]
		eastChamp = self.__east[0]
		midChamp = self.__midwest[0]

		of.write('---Final Four---\n')

		leftWinner, score = self.ep.predict(westChamp, southChamp)
		rightWinner, score = self.ep.predict(eastChamp, midChamp)

		of.write('%s v %s   --->   %s\n' % (westChamp, southChamp, leftWinner))
		of.write('%s v %s   --->   %s\n' % (eastChamp, midChamp, rightWinner))

		of.write('---Championship---\n')

		champ, score = self.ep.predict(leftWinner, rightWinner)
		of.write('%s v %s   --->   %s\n' % (leftWinner, rightWinner, champ))

		of.close()

	def predictSubBracket(self, file, bracket, bracketName):

		file.write('---%s---\n' % bracketName)

		i = 1
		step = 4

		while len(bracket) > 1:

			matchup1 = bracket.pop(0)
			winner1, score = self.ep.predict(matchup1[0], matchup1[1])

			matchup2 = bracket.pop(0)
			winner2, score = self.ep.predict(matchup2[0], matchup2[1])

			file.write('%s v %s   --->   %s\n' % (matchup1[0], matchup1[1], winner1))
			file.write('%s v %s   --->   %s\n' % (matchup2[0], matchup2[1], winner2))

			print('%d, %d' % (i, step))

			if i == step:
				print('here')
				file.write('\n')
				i = 1
				step /= 2
			else:
				i += 1

			bracket.append((winner1, winner2))
			

		final = bracket.pop(0)
		champ, score = self.ep.predict(final[0], final[1])

		file.write('\n%s v %s   --->   %s\n\n' % (final[0], final[1], champ))

		bracket.append(champ)


if __name__ == '__main__':

	bracketPath = 'bracket2021.txt'
	outputPath = 'prediction2021.txt'

	bp = BracketPredictor(bracketPath)
	bp.generatePredictions(outputPath)