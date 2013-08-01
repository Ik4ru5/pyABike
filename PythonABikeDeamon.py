#!/usr/bin/python
from PythonABike import *
import threading
import sqlite3
import time
import datetime

conn = sqlite3.connect('pythonABike.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stations
			(id INTEGER PRIMARY KEY, description, longitude, latitude, isOutside, dateTime)''')
c.execute('''CREATE TABLE IF NOT EXISTS bikes
			(id INTEGER PRIMARY KEY, number, stationID, canBeRented, canBeReturned, version, dateTime)''')
conn.commit()


cab = PythonABike()

class myThread (threading.Thread):
	def __init__(self, cab, longi, lati):
			threading.Thread.__init__(self)
			self.cab = cab
			self.longi = longi
			self.lati = lati
	
	def run(self):
		try:
			PythonABike.buildGeoPos(self.cab, self.longi, self.lati)
			availBikes = PythonABike.listFreeBikes(cab, 100, 1000)
			conn = sqlite3.connect('pythonABike.db')
			c = conn.cursor()
			
			if len(availBikes) > 0:
				for location in availBikes.Locations:
					c.execute("SELECT * FROM stations WHERE longitude = :long AND latitude = :lat", {"long":location.Position.Longitude, "lat":location.Position.Latitude})
					result = c.fetchall()
					if len(result) == 0:
						c.execute("INSERT INTO stations (id, description, longitude, latitude, isOutside, dateTime) VALUES (null, :desc, :long, :lat, :out, strftime('%s', 'now'))", {"desc":location.Description, "long":location.Position.Longitude, "lat":location.Position.Latitude, "out":location.isOutside})
						station = c.lastrowid
						
						conn.commit()
						print "new station found with id " + str(station)
					else:
						station = result[0][0]
						
					
					
					for bike in location.FreeBikes:
						c.execute("SELECT * FROM bikes WHERE number = :number AND stationID = :station", {"number":bike.Number, "station":station})
						result = c.fetchall();
						
						if len(result) == 0:
							c.execute("INSERT INTO bikes (id, number, stationID, canBeRented, canBeReturned, version, dateTime) VALUES (null, :number, :station, :rentable, :returnable, :version, strftime('%s', 'now'))", {"number":bike.Number,"station":station,"rentable":bike.canBeRented,"returnable":bike.canBeReturned,"version":bike.Version,})
							conn.commit()
							print "new bike with id " + str(bike.Number) + " found at station " + str(station)
				c.close()
		except Exception as e:
			print e
	
myThreads = []

while 1:
	for latitude in range(0,30):
		for longitude in range(0,10):
			lati = (48.98+((longitude+1)*0.004))
			longi = (8.36+((latitude+1)*0.004))
			
			thread = myThread(cab, longi, lati)
			myThreads.append(thread)
			thread.start()
			while threading.activeCount() >= 8:
				time.sleep(1)
