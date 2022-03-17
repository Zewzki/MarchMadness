
class BracketLoader:

    __divisionDelimiter = '@'
    __matchupDelimiter = '\n'
    __teamDelimiter = ':'

    def __init__(self):
        self.__bracketPath = None
        self.__brackets = None
    
    def set_bracket_path(self, bracketPath):
        self.__bracketPath = bracketPath
    
    def get_bracket_dict(self):
        return self.__brackets
    
    def load_bracket(self, bracketPath):
        
        self.__bracketPath = bracketPath

        if self.__bracketPath is None:
            return None

        self.__brackets = []

        lines = None
        with open(self.__bracketPath, 'r') as f:
            lines = f.read()
        
        if lines is None:
            self.__bracket = None
            return self.__bracket
        
        bracketDivisions = lines.split(self.__divisionDelimiter)

        for bracketDivision in bracketDivisions:
            matchups = bracketDivision.split(self.__matchupDelimiter)
            
            matchupList = []
            
            for i, matchup in enumerate(matchups):

                spl = matchup.split(self.__teamDelimiter)

                if len(spl) == 1:
                    continue
                elif len(spl) == 2:
                    teams = matchup.split(self.__teamDelimiter)
                    matchupList.append(teams[0])
                    matchupList.append(teams[1])
                else:
                    print('ERROR')
            
            self.__brackets.append(matchupList)
        
        return self.__brackets
