import sys, getopt  
import json

sys.path.append('../dbConnector')
from PostgresConnector import PostgresConnector

schemaName = "season22"

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

            print(f'{currArg} = {currVal}')

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

    conferencesPath = '../RawData/conferencesTeamsList22.json'

    jsonData = None

    with (open(conferencesPath, 'r') as f):
        jsonData = json.load(f)
    
    if jsonData is None:
        print('Error loading conferences file')
        quit()
    
    pgc = PostgresConnector(host, user, pass_, db)
    pgc.connect()
    
    for key in jsonData.keys():
        #print(f'Loading {key}')
        conf = jsonData[key]

        teams = conf['teams']

        selectCmd = f"SELECT conference_id FROM {schemaName}.conferences WHERE conference_name='{key}';"
        confId = pgc.query(selectCmd)

        if confId is None or len(confId) == 0:
            continue

        confId = confId[0][0]

        for team in teams:

            insertTeamCmd = f"INSERT INTO {schemaName}.teams (conference_id,team_name) VALUES ({confId},'{team}');"
            pgc.insert(insertTeamCmd)

    pgc.close()