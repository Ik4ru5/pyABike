PyABike
===========

Python library for Call A Bike 


Requirements
--------------

* suds (two files modified)
* Python (tested with 2.7.2)



Basic usage
-------

	from PyABike import *
	
	cab = PyABike()
	freeBikes = PyABike.listFreeBikes(cab, 100, 1000, longitude, latitude)
	
