import sqlite3
from env_vars import DB_FILE, LOGGER

class Sqllite:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        LOGGER.info("Connected to DB: {db}".format(db=DB_FILE))

    # Execute queries W/ return value
    def query(self, q):
        return self.cursor.execute(q)

    # Execute DDL and queries W/O return values
    def execute(self, q):
        self.cursor.execute(q)
        self.conn.commit()

    def close(self):
        self.conn.close()


