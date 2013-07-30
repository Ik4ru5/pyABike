#!/usr/bin/python
from PythonABike import *

def startLogging(arg):
	import logging
	logging.basicConfig(level=logging.INFO)
	logging.getLogger('suds.client').setLevel(logging.DEBUG)
	logging.getLogger('suds.transport').setLevel(logging.DEBUG)
	logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
	logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)


def print_help():
	print sys.argv[0] + ' TODO'

if __name__ == '__main__':
	user = ''
	passwd = ''
	maxRes = 10
	radius = 1000
	cab = PythonABike()
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'dhlr:u:p:g:', ['help', 'rent=', 'debug=', 'list', 'user=', 'pass=', 'geo=', 'maxResults=', 'searchRadius='])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('--help', '-h'):
			print_help()
			sys.exit()
		elif opt in ('--user', '-u'):
			user = arg
		elif opt in ('--pass', '-p'):
			passwd = arg
		elif opt == '--maxResults':
			maxRes = arg
		elif opt  == '--searchRadius':
			radius = arg
		elif opt in ('--geo', '-g'):
			try:
				pos = arg.split(",")
				PythonABike.buildGeoPos(cab, pos[0], pos[1])
			except:
				try:
					pos = arg.split(":")
					PythonABike.buildGeoPos(cab, pos[0], pos[1])
				except:
					print "USAGE: --geo=longitude,latitude or --geo=longitude:latitude"		
		elif opt in ('--debug', '-d'):
			startLogging(arg)

	# for evaluation of execute parameters
	for opt, arg in opts:
		if opt in ('--list', '-l'):
			try:
				print PythonABike.listFreeBikes(cab, maxRes, radius)
			except Exception as e:
				print "No Geoposition defined! Use --geo=longitude,latitude"
				sys.exit(2)
		elif opt in ('--rent', '-r'):
			print 'rent ' + arg 