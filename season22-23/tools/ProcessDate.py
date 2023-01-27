import sys, getopt
from datetime import date, timedelta
import json
import requests
from bs4 import BeautifulSoup

from EloTool import EloTool
from PostgresConnector import PostgresConnector

paramsPath = '../Params/S22Params.json'

class Game:

    def __init__(self, home_name, away_name, home_score, away_score):
        self.home_name = home_name
        self.away_name = away_name
        self.home_score = home_score
        self.away_score = away_score
    
    def is_valid(self):
        if self.home_name is None:
            return False
        if self.away_name is None:
            return False
        if self.home_score is None:
            return False
        if self.away_score is None:
            return False
        return True
    
    def __str__(self):
        s = f'--- {self.away_name} {self.away_score} - {self.home_name} {self.home_score} ---'
        return s

def get_url_page_data(url):

    pageDataResponse = requests.get(url)

    if pageDataResponse.status_code != 200:
        return None

    return pageDataResponse.content

def clean_name(name):
    s = name
    s = s.replace('.', '')
    s = s.replace("'", '')
    s = s.replace('-', ' ')
    s = s.replace('&', ' ')
    s = s.replace('Saint', 'St')
    return s

def get_team_data(schemaName, teamName, addIfAbsent=False):

    results = pgc.query(f"SELECT * FROM {schemaName}.teams WHERE team_name='{teamName}';")

    if results is None or len(results) == 0:
        print(f"Team '{teamName}' not found in teams table")

        if addIfAbsent is False:
            print(f'addIfAbsent set to False, skipping add')
            return None

        # insert into teams (id,name,confid) values (0,'test',1)
        pgc.insert(f"INSERT INTO {schemaName}.teams (team_name) VALUES ('{teamName}');")
        
        results = pgc.query(f"SELECT * FROM {schemaName}.teams WHERE team_name='{teamName}';")
    
    return results

def parse_page_data(pageData):

    # init beautiful soup parser
    soup = BeautifulSoup(pageData, 'html.parser')

    teamsCell = ('div', 'game_summary nohover')
    isolateTeams = ('tr', None)

    teamName = ('a', None)
    score = ('td', 'right')

    teamCells = soup.find_all(teamsCell[0], class_=teamsCell[1])

    if teamCells is None:
        print(f'No Games Reported on Date {date}')
        return None
        
    print(f'Found {len(teamCells)} team cells')

    games = []

    for teamCell in teamCells:

        awayTeam = None
        homeTeam = None

        teams = teamCell.find_all(isolateTeams[0])

        awayTeam = teams[0]
        homeTeam = teams[1]

        # extract team data
        awayName = awayTeam.find_all(teamName[0])[0].get_text()
        awayScore = -1
        try:
            awayScore = int(awayTeam.find_all(score[0], class_=score[1])[0].get_text())
        except:
            print('Away Team has no score reported')

        homeName = homeTeam.find_all(teamName[0])[0].get_text()
        homeScore = -1
        try:
            homeScore = int(homeTeam.find_all(score[0], class_=score[1])[0].get_text())
        except:
            print('Home Team has no  score reported')
        
        if awayScore == -1 or homeScore == -1:
            print('No Score, skipping')
            continue
        
        awayName = clean_name(awayName)
        homeName = clean_name(homeName)

        games.append(Game(homeName, awayName, homeScore, awayScore))

    return games

def process_date_games(pgc, paramsJson, year, month, day):

    # sample url
    # https://www.sports-reference.com/cbb/boxscores/index.cgi?month=11&day=9&year=2021 
    baseUrl = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?'

    dbParams = paramsJson['db']
    logParams = paramsJson['logging']

    schemaName = dbParams['schema_name']

    dateStamp = f'{year}-{month}-{day}'
    dateUrl = f'{baseUrl}month={month}&day={day}&year={year}'

    # Setup Logging
    errLogger = open(logParams['scraping_error_path'] + f'{dateStamp}_scraping_error.log', 'w')
    debugLogger = open(logParams['scraping_debug_path'] + f'{dateStamp}_scraping_debug.log', 'w')

    pageData = get_url_page_data(dateUrl)

    if pageData is None:
        print(f'No page data found for url: {dateUrl}')
        errLogger.write(f'{dateStamp}:No page data found for url: {dateUrl}')
        exit()
    
    # get games from page data
    games = parse_page_data(pageData)

    conn = pgc.get_conn()
    cur = conn.cursor()

    # operate on all games
    for game in games:

        print(game)

        if not game.is_valid():
            errLogger.write(f'{dateStamp}:[{game}] not added. Detected as invalid')
            continue
        
        homeTeamSQL = f"SELECT * FROM {schemaName}.teams WHERE team_name=%s;"
        awayTeamSQL = f"SELECT * FROM {schemaName}.teams WHERE team_name=%s;"
        
        awayTeamQueryResult = pgc.query(awayTeamSQL, [game.away_name])
        homeTeamQueryResult = pgc.query(homeTeamSQL, [game.home_name])

        print(awayTeamQueryResult)
        print(homeTeamQueryResult)
        print('-------------')

        invalidTeams = []
        isValidGame = True
        if awayTeamQueryResult is None or len(awayTeamQueryResult) == 0:
            invalidTeams.append(game.away_name)
            isValidGame = False
        if homeTeamQueryResult is None or len(homeTeamQueryResult) == 0:
            invalidTeams.append(game.home_name)
            isValidGame = False
        
        if not isValidGame:
            # log game, specifically showing team not found in DB
            errLogger.write(f"{dateStamp}:[{game}] not added. {invalidTeams} not found\n")
            continue
        
        homeTeamQueryResult = homeTeamQueryResult[0]
        awayTeamQueryResult = awayTeamQueryResult[0]
        
        homeConfId = homeTeamQueryResult[0]
        homeId = homeTeamQueryResult[1]
        homeScore = game.home_score

        awayConfId = awayTeamQueryResult[0]
        awayId = awayTeamQueryResult[1]
        awayScore = game.away_score
        
        try:
            addGameSql = f"INSERT INTO {schemaName}.games (home_id,away_id,home_score,away_score,date_played) VALUES (%s,%s,%s,%s,%s);"
            pgc.insert(addGameSql, [homeId, awayId, homeScore, awayScore, dateStamp])
            #curr.execute(addGameSql, (homeId, awayId, homeScore, awayScore, dateStamp))
            #conn.commit()
        except Exception as ex:
            errLogger.write(f'{dateStamp}:Error performing insert operation for game {game}\n{ex}')
            continue

        debugLogger.write(f"{dateStamp}:Added [{game}]\n")

    errLogger.close()
    debugLogger.close()

def process_date_elos(pgc, paramsJson, year, month, day):

    dbParams = paramsJson['db']
    eloParams = paramsJson['elo_params']

    logParams = paramsJson['logging']

    schemaName = dbParams['schema_name']

    teamWeight = eloParams['team_elo_weight']
    confWeight = eloParams['conf_elo_weight']

    dateStamp = f'{year}-{month}-{day}'

    # Setup Logging
    errLogger = open(logParams['processing_error_path'] + f'{dateStamp}_processing_error.log', 'w')
    debugLogger = open(logParams['processing_debug_path'] + f'{dateStamp}_processing_debug.log', 'w')


    conn = pgc.get_conn()
    cur = conn.cursor()

    eloTool = EloTool(eloParams['k_tiers'])

    getAllGamesSql = f"SELECT * FROM {schemaName}.game_view where date_played=%s;"
    games = pgc.query(getAllGamesSql, [dateStamp])

    # 0        1             2        3          4           5             6        7          8           9                            10
    # game_id, home_conf_id, home_id, home_name, home_score, away_conf_id, away_id, away_name, away_score, date_played,                 elo_processed
    # (47,     26,           273,     'Holy Cross',68,       18,           181,     'Siena',   75,         datetime.date(2022, 11, 7)), false
    for game in games:

        gameId = game[0]

        homeConfId = game[1]
        homeId = game[2]
        homeName = game[3]
        homeScore = game[4]

        awayConfId = game[5]
        awayId = game[6]
        awayName = game[7]
        awayScore = game[8]

        datePlayed = game[9]

        elo_processed = bool(game[10])

        if elo_processed:
            print(f'skipping game {gameId}')
            continue

        # get team elo data
        homeTeamSQL = f"SELECT current_elo FROM {schemaName}.teams WHERE team_id=%s;"
        awayTeamSQL = f"SELECT current_elo FROM {schemaName}.teams WHERE team_id=%s;"

        homeTeamElo = pgc.query(homeTeamSQL, [homeId])[0]
        awayTeamElo = pgc.query(awayTeamSQL, [awayId])[0]

        homeTeamCurrentElo = homeTeamElo[0]
        awayTeamCurrentElo = awayTeamElo[0]

        # get conference elo data
        homeConfSQL = f"SELECT conference_elo FROM {schemaName}.conferences WHERE conference_id=%s;"
        awayConfSQL = f"SELECT conference_elo FROM {schemaName}.conferences WHERE conference_id=%s;"

        homeConfElo = pgc.query(homeConfSQL, [homeConfId])[0]
        awayConfElo = pgc.query(awayConfSQL, [awayConfId])[0]

        homeConfCurrentElo = homeConfElo[0]
        awayConfCurrentElo = awayConfElo[0]

        # calculate new elos
        homeNormalizedScore, awayNormalizedScore = eloTool.get_outcome_by_score(homeScore, awayScore)
        homeExpectation, awayExpectation = eloTool.predict_matchup(confWeight, teamWeight, homeConfCurrentElo, homeTeamCurrentElo, awayConfCurrentElo, awayTeamCurrentElo)
        
        newHomeElo = eloTool.calculate_new_elo(homeTeamCurrentElo, homeExpectation, homeNormalizedScore)
        newAwayElo = eloTool.calculate_new_elo(awayTeamCurrentElo, awayExpectation, awayNormalizedScore)

        homeDelta = (newHomeElo - homeTeamCurrentElo) * teamWeight
        awayDelta = (newAwayElo - awayTeamCurrentElo) * teamWeight

        newHomeElo = homeTeamCurrentElo + homeDelta
        newAwayElo = awayTeamCurrentElo + awayDelta

        # update team current_elo
        try:
            teamCurrEloUpdateSQL = f"UPDATE {schemaName}.teams SET current_elo=%s WHERE team_id=%s;"
            pgc.update(teamCurrEloUpdateSQL, [newHomeElo, homeId])
            pgc.update(teamCurrEloUpdateSQL, [newAwayElo, awayId])
        except Exception as ex:
            errLogger.write(f"Error updating elo: {ex}")
            continue

        newHomeConfElo = homeConfCurrentElo
        homeConfDelta = 0

        newAwayConfElo = awayConfCurrentElo
        awayConfDelta = 0

        # update conference elo for non-conference games
        if homeConfId != awayConfId:

            newHomeConfElo = eloTool.calculate_new_elo(homeConfCurrentElo, homeExpectation, homeNormalizedScore)
            newAwayConfElo = eloTool.calculate_new_elo(awayConfCurrentElo, awayExpectation, awayNormalizedScore)

            homeConfDelta = (newHomeConfElo - homeConfCurrentElo) * confWeight
            awayConfDelta = (newAwayConfElo - awayConfCurrentElo) * confWeight

            try:
                eloTool.stagedConferenceEloUpdates[homeConfId] += homeConfDelta
            except:
                eloTool.stagedConferenceEloUpdates[homeConfId] = homeConfDelta
            
            try:
                eloTool.stagedConferenceEloUpdates[awayConfId] += awayConfDelta
            except:
                eloTool.stagedConferenceEloUpdates[awayConfId] = awayConfDelta
        
        # add new record in game_elo table
        try:
            sql = f"UPDATE {schemaName}.games SET"
            sql += " home_conf_elo=%s, home_team_elo=%s, home_conf_delta=%s, home_team_delta=%s,"
            sql += " away_conf_elo=%s, away_team_elo=%s, away_conf_delta=%s, away_team_delta=%s"
            sql += " WHERE game_id=%s;"
            pgc.insert(sql, [homeConfCurrentElo, homeTeamCurrentElo, homeConfDelta, homeDelta, awayConfCurrentElo, awayTeamCurrentElo, awayConfDelta, awayDelta, gameId])
        except Exception as ex:
            errLogger.write(f"Error inserting game_elo record {ex}")
            continue
        
        # update game status to elo_processed
        try:
            gameProcessedUpdateSQL = f"UPDATE {schemaName}.games SET elo_processed=true WHERE game_id=%s;"
            pgc.update(gameProcessedUpdateSQL, [gameId])
        except Exception as ex:
            errLogger.write(f"Error updating game_processed flag: {ex}")
            continue
    
    for confId in eloTool.stagedConferenceEloUpdates.keys():

        conferenceSQL = f"SELECT conference_elo FROM {schemaName}.conferences WHERE conference_id=%s;"
        confElo = pgc.query(conferenceSQL, [confId])[0]

        confCurrentElo = confElo[0]

        newConfElo = confCurrentElo + eloTool.stagedConferenceEloUpdates[confId]

        updateSQL = f"UPDATE {schemaName}.conferences SET conference_elo=%s WHERE conference_id=%s;"
        pgc.update(updateSQL, [newConfElo, confId])

        insertSQL = f"INSERT INTO {schemaName}.conferences_elo_history (conference_id,elo,delta,date_updated) VALUES (%s,%s,%s,%s);"
        pgc.insert(insertSQL, [confId, newConfElo, newConfElo-confCurrentElo,dateStamp])
    
    debugLogger.close()
    errLogger.close()

if __name__ == '__main__':

    argList = sys.argv[1:]

    options = 'h:u:p:d:'
    longOptions = ['host=', 'user=', 'pass', 'db']

    host = None
    user = None
    pass_ = None
    db = None

    try:
        args, vals = getopt.gnu_getopt(argList, options, longOptions)
    
        for currArg, currVal in args:

            if currArg in ('-h', '--host'):
                host = currVal
            elif currArg in ('-u', '--user'):
                user = currVal
            elif currArg in ('-p', '--pass'):
                pass_ = currVal
            elif currArg in ('-d', '--db'):
                db = currVal
            else:
                print(f'Unknown arg provided "{currArg}", quitting...')
                quit()

    except getopt.error as err:
        print(str(err))
        quit()
    
    if None in (host,user,pass_,db):
        print(f'One or more of required arguments is empty, quitting...\n({host},{user},{pass_ is None},{db})')
        quit()
    
    paramsJson = None

    with open(paramsPath, 'r') as f:
        paramsJson = json.load(f)
    
    if paramsJson is None:
        print(f'Error loading params json:{paramsPath}')
        quit()
    
    # init db connection
    pgc = PostgresConnector(host, user, pass_, db)
    pgc.connect()

    today = date.today()
    yesterday = today - timedelta(days=1)
    #currYear = today.year
    #currMonth = today.month
    #currDay = today.day

    #startDate = date.fromisoformat("2022-11-07")
    #endDate = date.fromisoformat("2023-01-04")

    #startDate = date.fromisoformat("2023-01-20")
    #endDate = date.fromisoformat("2023-01-22")

    startDate = yesterday
    endDate = yesterday

    currDate = startDate

    while currDate <= endDate:

        currYear = currDate.year
        currMonth = currDate.month
        currDay = currDate.day

        process_date_games(pgc, paramsJson, currYear, currMonth, currDay)
        process_date_elos(pgc, paramsJson, currYear, currMonth, currDay)

        currDate = currDate + timedelta(days=1)

    pgc.close()
