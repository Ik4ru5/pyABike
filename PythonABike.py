import datetime
import sys, getopt
from suds import WebFault
from suds.client import Client
from suds.plugin import *


class PythonABike:
	client = ''
	def __init__(self):
		url = 'https://xml.dbcarsharing-buchung.de/hal2_cabserver/definitions/HAL2_CABSERVER_2.wsdl'
		self.client = Client(url)

		self.buildCommonParams()
		
	def buildCustomerData(self, user, passwd):
		self.customerData = self.client.factory.create('Type_CustomerData')
		self.customerData.Password = passwd
		self.customerData.Phone = user
		
	def buildGeoPos(self, longitude, latitude):
		self.geoPos = self.client.factory.create('Type_GeoPosition');
		self.geoPos.Longitude = longitude
		self.geoPos.Latitude = latitude
		
	def buildCommonParams(self):
		self.commonParams = self.client.factory.create('Type_CommonParams');

		userData = self.client.factory.create('Type_UserData');
		userData.User = 't_cab_android' #from android app
		userData.Password = '3b3cc28469' #from android app

		self.commonParams.UserData = userData
		self.commonParams.LanguageUID = 1 #only option
		self.commonParams.RequestTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.commonParams.Version = 1 #only option
		
	def listFreeBikes(self, maxRes = 100, radius = 5000):
		if hasattr(self, 'geoPos') == False:
			raise Exception("Not GeoPos")
		else:
			listFreeBikes = getattr(self.client.service, 'CABSERVER.listFreeBikes')(CommonParams = self.commonParams, SearchPosition = self.geoPos, maxResults = maxRes, searchRadius = radius)
			return listFreeBikes