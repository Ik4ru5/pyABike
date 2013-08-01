#!/usr/bin/python

import sqlite3
import time
import datetime

f = open('heatmap.js', 'w')

conn = sqlite3.connect('pythonABike.db')
c = conn.cursor()

c.execute("SELECT longitude, latitude FROM bikes LEFT OUTER JOIN stations ON stationID = stations.id")
result = c.fetchall()

f.write('var taxiData = [\n')

counter = 0;
for station in result:
	print station
	if counter != 0:
		f.write(',\n')
	f.write('new google.maps.LatLng(' + str(station[1]) + ', ' + str(station[0]) + ')')
	counter = counter + 1
	
f.write('];\n')