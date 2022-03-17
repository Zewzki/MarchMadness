import json

class Team:

	__fieldDir = 'relevantFields.txt'

	def __init__(self, relevantFieldsPath):

		self.__fields = []
		self.__valueDict = {}

		with open(relevantFieldsPath, 'r') as file:
			lines = file.readlines()
			for line in lines:
				self.__fields.append(line.replace('\n', ''))
	
	def getFields(self):
		return self.__fields

	def getValue(self, field):
		if field in self.__fields:
			return self.__valueDict[field]
		else:
			print('Field %s unkown' % field)
			return None

	def getValues(self):
		return self.__valueDict

	def setValue(self, field, value):
		if field in self.__fields:
			self.__valueDict[field] = value
		else:
			print('Field %s unknown' % field)

	def __str__(self):

		s = ''

		for key in self.__valueDict:
			s += '%s : %s' % (key, self.__valueDict[key]) + '\n'

		return s

if __name__ == '__main__':

	team = Team()
	team.setValue('Wins', 1)

	print(team.getFields())
	print(team)
