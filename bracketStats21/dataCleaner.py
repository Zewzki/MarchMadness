import json

def cleanEfficiencyData(path, outputName):
	
	file = open(path, 'r')
	lines = file.readlines()

	new = open(outputName, 'w')

	for line in lines:
		split = line.split('\t')
		s = '%s:%s\n' % (split[1], split[2])
		new.write(s)

	file.close()

def generateTranslationTable(path, outputName):

	data = open(path, 'r').read()
	jsonData = json.loads(data)

	output = open(outputName, 'w')

	for i in jsonData:
		line = '%s:%s:%s' % (i['Name'], i['Team'], i['TeamID'])
		output.write('%s\n' % line)

def cleanRawTeamStats(teamStatsPath, relevantFieldsPath, outputPath):

	fieldsFile = open(relevantFieldsPath, 'r')
	fields = [x.replace('\n', '') for x in fieldsFile.readlines()]

	data = open(teamStatsPath, 'r').read()
	jsonData = json.loads(data)

	output = open(outputPath, 'w')

	for record in jsonData:

		s = ''

		for field in fields:

			s += '%s,' % record[field]

		s = s[:-1] + '\n'

		output.write(s)

	print('Complete')

def appendTeamEfficiencies(teamStatsPath, offEffPath, defEffPath, outputPath):
	print('f')
	

if __name__ == '__main__':
	
	#raw = '../teamStats.txt'
	#processed = '../translationTable.txt'

	teamStatsPath = 'data/raw/teamStats.txt'
	relevantFieldsPath = 'data/cleaned/relevantFields.txt'
	outputPath = 'data/cleaned/cleanedTeamData.txt'

	cleanRawTeamStats(teamStatsPath, relevantFieldsPath, outputPath)