import json
from Team import Team

class DataLoader:

	def __init__(self, src):
		
		data = open(src, 'r').read()
		self.jsonData = json.loads(data)

	def buildTeamList(self, relevantFieldsPath):

		teamList = {}

		for i in self.jsonData:
			
			newTeam = Team(relevantFieldsPath)
			fields = newTeam.getFields()

			for j in fields:

				newTeam.setValue(j, i[j])

			teamList[newTeam.getValue('Name')] = newTeam

		return teamList

if __name__ == '__main__':

	src = 'teamStats.txt'
	fields = 'relevantFields.txt'

	dataLoader = DataLoader(src)
	teamList = dataLoader.buildTeamList(fields)