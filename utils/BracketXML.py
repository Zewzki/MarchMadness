import ISerializeable

class BracketXML(ISerializeable):

    __nameKey = ''

    def __init__(self, path):
        self.__path = path
        self.__gameDict = {}
        
    def add_game(self, newGame):
        if newGame.get_field(self.__nameKey) in self.__gameList:
            print(f'Game titled "{newGame.get_field(self.__nameKey)}" is already present in game dictionary. Use "update_game" to change game fields')
            return
        self.__gameDict[newGame.get_field(self.__nameKey)] = newGame
    
    def get_game(self, name):
        if name not in self.__gameList:
            print(f'"{name}" not present in game dictionary')
            return
        return self.__gameDict[name]
    
    def serialize(self):
        print('f')
    
    def deserialize(self):
        print('f')
