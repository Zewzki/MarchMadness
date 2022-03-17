import json
import urllib.request
import time
#from Translator import Translator

class GameCollector:

	__translatorPath = 'translationTable.txt'

	__httpStatusCodeField = 'HttpStatusCode'
	__gameIdField = 'GameID'
	__statusField = 'Status'
	__dateField = 'Day'
	__awayTeamAbbrField = 'AwayTeam'
	__homeTeamAbbrField = 'HomeTeam'
	__awayTeamIdField = 'AwayTeamID'
	__homeTeamIdField = 'HomeTeamID'
	__awayTeamScoreField = 'AwayTeamScore'
	__homeTeamScoreField = 'HomeTeamScore'

	__canceledValue = 'Canceled'
	__postponedValue = 'Postponed'

	__finalValue = 'Final'

	__maxMonth = 12
	__maxDay = 31

	__sleepTime = 6

	def __init__(self, url, apiKey):
		self.url = url
		self.apiKey = key
		#self.translator = Translator(self.__translatorPath)

	def getGamesOnDate(self, date):

		dateURL = self.url + date + '?key=' + self.apiKey

		try:

			response = urllib.request.urlopen(dateURL)
			data = json.loads(response.read())

		except urllib.error.HTTPError:
			print('Invalid Date: %s' % date)
			return ''

		print(data)

		gamesOnDate = ''

		for record in data:

			try:

				gameId = record[self.__gameIdField]
				status = record[self.__statusField]
				date = record[self.__dateField]
				date = date.replace('T00:00:00', '')
				awayId = record[self.__awayTeamIdField]
				homeId = record[self.__homeTeamIdField]
				awayScore = record[self.__awayTeamScoreField]
				homeScore = record[self.__homeTeamScoreField]
				
				if status == self.__canceledValue or status == self.__postponedValue:
					continue

				s = '%s,%s,%s,%s,%s,%s,%s\n' % (gameId, status, date, awayId, homeId, awayScore, homeScore)
				gamesOnDate += s

			except KeyError:
				print('Error loading field from record')
				continue

		print('%s retrieved' % date)

		return gamesOnDate

	def getGamesInDateRange(self, outputPath, start = '2021-11-08', end = '2022-3-16'):

		startSplit = start.split('-')
		endSplit = end.split('-')

		startYear = int(startSplit[0])
		startMonth = int(startSplit[1])
		startDay = int(startSplit[2])
		
		endYear = int(endSplit[0])
		endMonth = int(endSplit[1])
		endDay = int(endSplit[2])

		file = open(outputPath, 'w')

		startString = '%d-%d-%d' % (startYear, startMonth, startDay)
		endString = '%d-%d-%d' % (endYear, endMonth, endDay)

		while not startString == endString:
			
			if startDay > self.__maxDay:
				startDay = 1
				startMonth += 1

			if startMonth > self.__maxMonth:
				startMonth = 1
				startYear += 1

			startString = '%d-%d-%d' % (startYear, startMonth, startDay)
			file.write(self.getGamesOnDate(startString))

			startDay += 1

			time.sleep(self.__sleepTime)

		print('All Dates Retrieved')

		file.close()

if __name__ == '__main__':

	url = 'https://api.sportsdata.io/v3/cbb/scores/json/GamesByDate/'
	key = '70840ff8e1b7410f8d6acb9d2f072b8e'
	outputPath = 'data/raw/gameData/allGames22.txt'

	gc = GameCollector(url, key)
	gc.getGamesInDateRange(outputPath = outputPath)