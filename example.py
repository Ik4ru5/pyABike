#!/usr/bin/python
from PyABike import *

cab = PyABike()

PyABike.buildGeoPos(cab, 8.4040, 49.0095)

freeBikes =  PyABike.listFreeBikes(cab, 2, 100)
returnLocations = PyABike.listReturnLocations(cab, '4242', 2, 100)

print freeBikes
print returnLocations