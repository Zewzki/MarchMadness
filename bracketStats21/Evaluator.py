from DataLoader import DataLoader
from Team import Team

class Evaluator:
	
	def __init__(self, teamDataPath, relevantFieldsPath):

		dataLoader = DataLoader(teamDataPath)
		self.teamList = dataLoader.buildTeamList(relevantFieldsPath)

	def evaluateTeam(self, name):

		t = None

		try:
			t = self.teamList[name]
		except KeyError:
			print("Invalid Key Entered")

		if t is None:
			return 0.0

		t = t.getValues()

		pointsPerGame = float(t['Points']) / float(t['Games'])

		val = 0
		val += float(t['Wins'] - t['Losses'])
		val += float(t['FieldGoalsMade']) * (float(t['FieldGoalsPercentage']) / 100)
		val += float(t['TwoPointersMade']) * (float(t['TwoPointersPercentage']) / 100)
		val += float(t['ThreePointersMade']) * (float(t['ThreePointersMade']) / 100)
		val += float(t['FreeThrowsMade']) * (float(t['FreeThrowsPercentage']) / 100)
		val += float(t['Rebounds']) * .1
		val += float(t['Steals']) * .30
		val += float(t['BlockedShots']) * .25
		val += float(t['Turnovers']) * .30
		val -= float(t['PersonalFouls']) * .2
		val += float(t['Points']) * .5

		return val

	def getTeam(self, name):

		t = None

		try:
			t = self.teamList[name]
		except KeyError:
			print("Invalid Key Entered")

		return t

	def evaluateAllTeams(self, allTeamNamesPath, print = False):

		results = {}

		allTeamNames = open(allTeamNamesPath, 'r')
		lines = allTeamNames.readlines()
	
		for name in lines:
			nameAdj = name.replace('\n', '')
			val = evaluator.evaluateTeam(nameAdj)

			results[nameAdj] = val

		sortedResults = {k: v for k, v in sorted(results.items(), reverse = True, key = lambda item: item[1])}

		if print:
			for key in sortedResults:
				print('%s:%f' % (key, sortedResults[key]))

		return sortedResults



if __name__ == '__main__':

	teamDataPath = 'teamStats.txt'
	relevantFieldsPath = 'relevantFields.txt'
	allTeamNamesPath = 'allTeamNames.txt'

	evaluator = Evaluator(teamDataPath, relevantFieldsPath)

	
