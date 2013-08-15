PyABike
===========

Python library for Call A Bike 


Requirements
--------------

* suds (https://fedorahosted.org/suds/)
* Python (tested with 2.7.2)



Basic usage
-------

	from PyABike import *
	
	cab = PyABike()
	freeBikes = PyABike.listFreeBikes(cab, 100, 1000, longitude, latitude)
	
