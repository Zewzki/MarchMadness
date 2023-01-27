import psycopg2

class PostgresConnector:


    def __init__(self, hostName, username, password, databaseName):
        self.__hostName = hostName
        self.__username = username
        self.__password = password
        self.__databaseName = databaseName
        self.__conn = None
    
    def connect(self):

        if self.__conn is not None:
            print(f'Active connection is open, please close before opening new connection')
            return

        try:
            self.__conn = psycopg2.connect(host=self.__hostName, database=self.__databaseName, user=self.__username, password=self.__password)  
        except:
            print(f'Error connecting to database {self.__databseName} at host {self.__hostName}')
            return
        
        print(f'Successfully Connected to database {self.__databaseName} at host {self.__hostName}')


    def query(self, cmd, values=None):

        if self.__conn is None:
            print('No Open Connection, ignoring')
            return None
        
        results = None
        with self.__conn.cursor() as cur:

            if values is None:

                try:
                    cur.execute(cmd)
                    results = cur.fetchall()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')

            else:

                try:
                    cur.execute(cmd, values)
                    results = cur.fetchall()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')

        return results
    
    def insert(self, cmd, values=None):

        if self.__conn is None:
            print('No Open Connection, ignoring')
            return
        
        with self.__conn.cursor() as cur:

            if values is None:

                try:
                    cur.execute(cmd)
                    self.__conn.commit()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')
                    self.__conn.rollback()

            else:

                try:
                    cur.execute(cmd, values)
                    self.__conn.commit()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')
                    self.__conn.rollback()

    def update(self, cmd, values=None):

        if self.__conn is None:
            print('No Open Connection, ignoring')
            return
        
        with self.__conn.cursor() as cur:
            
            if values is None:
            
                try:
                    cur.execute(cmd)
                    self.__conn.commit()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')
                    self.__conn.rollback()

            else:

                try:
                    cur.execute(cmd, values)
                    self.__conn.commit()
                except Exception as e:
                    print(f'Error executing command: {cmd}\n{e}')
                    self.__conn.rollback()


    def get_elo_info(self, teamId):
        queryStatement = f"SELECT team_elo, team_elo_history, conference_elo, conference_elo_history FROM season21.elo_view WHERE team_id={teamId}"
        return self.query(queryStatement)
    
    def get_all_games_by_date(self, date):
    
        queryStatement = f"SELECT * FROM season21.game_view WHERE date_played='{date}'"
        return self.query(queryStatement)

    def get_all_teams(self):
        queryStatement = f"SELECT * from season21.teams;"
        return self.query(queryStatement)
    
    def get_conn(self):
        return self.__conn

    def close(self):

        if self.__conn is None:
            print('No Open Connection to close')
            return

        try:
            self.__conn.close()
            self.__conn = None
        except:
            print('Error closing connection')