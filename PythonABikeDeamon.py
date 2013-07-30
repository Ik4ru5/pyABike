#!/usr/bin/python
from PythonABike import *
import sqlite3
conn = sqlite3.connect('pythonABike.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stations
			(id, description, longitude, latitude, isOutside, firstSeen)''')
c.execute('''CREATE TABLE IF NOT EXISTS bikes
			(id, number, stationID, canBeRented, canBeReturned, version, dateTime, lastSeen)''')
conn.commit()
