
class Translator:
	
	def __init__(self, translationTablePath, delimiter = ','):
		self.path = translationTablePath

		self.__nameToAbbrev = {}
		self.__nameToId = {}
		self.__abbrevToName = {}
		self.__abbrevToId = {}
		self.__idToName = {}
		self.__idToAbbrev = {}

		file = open(self.path, 'r')
		lines = file.readlines()

		for line in lines:
			line = line[:-1]
			split = line.split(delimiter)

			self.__nameToAbbrev[split[0]] = split[1]
			self.__nameToId[split[0]] = split[2]

			self.__abbrevToName[split[1]] = split[0]
			self.__abbrevToId[split[1]] = split[2]

			self.__idToName[split[2]] = split[0]
			self.__idToAbbrev[split[2]] = split[1]

	def abbrevToName(self, abbrev):
		return self.__abbrevToName[abbrev]

	def nameToAbbrev(self, name):
		return self.__nameToAbbrev[name]

	def idToName(self, ID):
		if ID not in self.__idToName:
			name = f'UnknownTeam{ID}'
			abbrev = f'UT{ID}'
			with open(self.path, 'a') as f:
				f.write(f'{name},{abbrev},{ID}\n')
			self.__nameToAbbrev[name] = abbrev
			self.__nameToId[name] = ID
			self.__abbrevToName[abbrev] = name
			self.__abbrevToId[abbrev] = ID
			self.__idToName[ID] = name
			self.__idToAbbrev[ID] = abbrev
		
		return self.__idToName[ID]

	def nameToId(self, name):
		return self.__nameToId[name]

	def idToAbbrev(self, ID):
		return self.__idToAbbrev[ID]

	def abbrevToId(self, abbrev):
		return self.__abbrevToId[abbrev]


if __name__ == '__main__':

	translationTablePath = 'translationTable.txt'

	t = Translator(translationTablePath)

	name = 'Gonzaga Bulldogs'
	abbrev = 'GNZG'
	ID = '334'

	print('Name to Abbrev: %s -> %s' % (name, t.nameToAbbrev(name)))
	print('Name to ID: %s -> %s' % (name, t.nameToId(name)))
	print('Abbrev to Name: %s -> %s' % (abbrev, t.abbrevToName(abbrev)))
	print('Abbrev to ID: %s -> %s' % (abbrev, t.abbrevToId(abbrev)))
	print('ID to Name: %s -> %s' % (ID, t.idToName(ID)))
	print('ID to Abbrev: %s -> %s' % (ID, t.idToAbbrev(ID)))

