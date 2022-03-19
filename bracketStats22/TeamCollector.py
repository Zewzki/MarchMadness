import json
import urllib.request
import time

class TeamCollector:

    def __init__(self, url, apiKey):
        self.url = url
        self.apiKey = apiKey
    
    def getTeams(self):
        
        fullURL = self.url + '?key=' + self.apiKey
        
        try:
            response = urllib.request.urlopen(fullURL)
            data = json.loads(response.read())

        except urllib.error.HTTPError as e:
            print(e)
            return ''

        print(data)

        for record in data:

            print(record)

        return data


if __name__ == '__main__':

    url = 'https://api.sportsdata.io/v3/nfl/scores/json/Teams/'
    key = '70840ff8e1b7410f8d6acb9d2f072b8e'
    outputPath = 'data/raw/gameData/allTeams22.txt'

    tc = TeamCollector(url, key)
    data = tc.getTeams()
    
