import mysql.connector
from mysql.connector import Error
from configparser import ConfigParser
import numpy as np

# http://www.mysqltutorial.org/python-mysql-query/

db = 'log'

conn = mysql.connector.connect(host='10.6.66.160', database=db, user='debian-sys-maint', password = 'SoLcxvfgbzqU0ixI')
# curser = area where all the records are stored
dbcursor = conn.cursor()


# dbcursor.execute('SHOW TABLES')
# print(dbcursor.fetchall())

table = 'SELECT * FROM cfvdata'
dbcursor.execute(table)

table_name = [i[0] for i in dbcursor.description]
print(table_name)

BMS = dbcursor.fetchall()

BMSnp = np.array(BMS)
print(np.shape(BMSnp))
