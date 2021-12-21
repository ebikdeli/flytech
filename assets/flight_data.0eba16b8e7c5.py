import os
import sqlite3
from sqlite3.dbapi2 import OperationalError
import requests
import datetime

API_ROOT = 'https://opensky-network.org/api'

os.chdir('D:/Works_Backups/Python/flytech/flytech')

r = requests.get(url=API_ROOT + '/states/all')
time = r.json()['time']
ctime = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d - %H:%M:%S')
# states is a two dimensional list
states = r.json()['states']
conn = sqlite3.connect('apadana.sqlite3')
cur = conn.cursor()
try:
    data = cur.execute('SELECT id FROM dflight')
except OperationalError:
    sql = """CREATE TABLE dflight(
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                icao varchar(8),
                callsign varchar(10),
                country varchar(100),
                updated DATETIME
            );"""
    cur.execute(sql)
    print('dflight created')
for state in states:
    sql = """INSERT INTO dflight (icao, callsign, country, updated)
             VALUES(?, ?, ?, ?);"""
    cur.execute(sql, (state[0], state[1], state[2], ctime))
conn.commit()
conn.close()
