import sys, getopt
from datetime import date
from EloTool import EloTool
import json

sys.path.append('../dbConnector')
from PostgresConnector import PostgresConnector

paramsJsonPath = '../Params/S22Params.json'

def main(pgc, eloParams):

    default_elo = eloParams['default_elo']

    # select all teams with current_elo = NULL or elo_history = NULL
    teamStatement = f"SELECT * FROM {schemaName}.teams WHERE current_elo IS NULL;"
    teamResults = pgc.query(teamStatement)

    conn = pgc.get_conn()
    cur = conn.cursor()

    for team in teamResults:

        teamElo = default_elo

        try:
            queryStatement = f"SELECT current_elo FROM season21.teams WHERE team_name=%s;"
            teamElo = cur.query(queryStatement, (team[2]))[0]
        except:
            pass

        updateStatement = f"UPDATE {schemaName}.teams SET current_elo=%s WHERE team_name=%s;"
        cur.execute(updateStatement, (teamElo, team[2]))
        conn.commit()
    
    # select all conferences with current_elo = NULL or elo_history = NULL
    confStatement = f"SELECT * FROM {schemaName}.conferences WHERE conference_elo IS NULL;"
    confResults = pgc.query(confStatement)

    for conf in confResults:

        confElo = default_elo

        try:
            queryStatement = f"SELECT conference_elo FROM season21.conferences WHERE conference_name=%s;"
            confElo = cur.query(queryStatement, (conf[2]))[0]
        except:
            pass

        updateStatement = f"UPDATE {schemaName}.conferences SET conference_elo=%s WHERE conference_name=%s;"
        cur.execute(updateStatement, (confElo, conf[2]))
        conn.commit()

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
    
    params = None
    with (open(paramsJsonPath, 'r') as f):
        params = json.load(f)
    
    if params is None or len(params) == 0:
        print('Error loading params file')
        quit()
    
    eloParams = params['elo_params']
    schemaName = params['db']['schema_name']

    pgc = PostgresConnector(host, user, pass_, db)
    pgc.connect()

    main(pgc, eloParams)

    pgc.close()



