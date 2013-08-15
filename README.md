PyABike
===========

Python library for Call A Bike 


Requirements
--------------

* suds (https://fedorahosted.org/suds/)
* Python (tested with 2.7.2)



Usage
-------

	from PyABike import *
	
	cab = PyABike()
	freeBikes = PyABike.listFreeBikes(cab, longitude, latitude, 100, 1000)
	