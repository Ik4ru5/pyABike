import datetime
import sys, getopt
from suds import WebFault
from suds.client import Client
from suds.plugin import *


class PythonABike:
	client = ''
	def __init__(self):
		url = 'https://xml.dbcarsharing-buchung.de/hal2_cabserver/definitions/HAL2_CABSERVER_3.wsdl' # current api url
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
			self.listFreeBikes = getattr(self.client.service, 'CABSERVER.listFreeBikes')(CommonParams = self.commonParams, SearchPosition = self.geoPos, maxResults = maxRes, searchRadius = radius)
			return self.listFreeBikes
			
	def getCustomerInfo(self, user = '', passwd = ''):
		#CommonParams: 
		#CustomerData:
		if user != '' & passwd != '':
			self.buildCustomerData(user, passwd)
		else:	
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.getCustomerInfo')(CommonParams = self.commonParams, CustomerData = self.customerData)
				return self.requestResponse
			except Execption as e:
				print e
	
	
	def requestNewPassword(self, phone):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#PhoneNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerPhone
		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.requestNewPassword')(CommonParams = self.commonParams, PhoneNumber = phone)
			return self.requestResponse
		except Execption as e:
			print "An Error occurred during the request: "
			print e
	

	def listReturnLocations(self, bike, maxRes = 100, radius = 5000):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		#SearchPosition: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_GeoPosition
		#maxResults: http://www.w3.org/2001/XMLSchema:int
		#searchRadius: http://www.w3.org/2001/XMLSchema:int
		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.listReturnLocations')(CommonParams = self.commonParams, BikeNumber = bike, SearchPosition = self.geoPos, maxResults = maxRes, searchRadius = radius)
			return self.requestResponse
		except Execption as e:
			print "An Error occurred during the request: "
			print e
		
		
	def rentBike(self, bike, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		if user != '' & passwd != '':
			self.buildCustomerData(user, passwd)
		else:
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.listReturnLocations')(CommonParams = self.commonParams, CustomerData = self.customerData, BikeNumber = bike)
				return self.requestResponse
			except Execption as e:
				print "An Error occurred during the request: "
				print e
			
		
	def returnBike(self, bike, retCode, locID, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		#ReturnCode: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeCode
		#LocationUID: http://www.w3.org/2001/XMLSchema:int
		#CustomerDataOptional: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerDataOptional
		if user != '' & passwd != '':
			self.buildCustomerData(user, passwd)
		else:
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.listReturnLocations')(CommonParams = self.commonParams, BikeNumber = bike, ReturnCode = retCode, LocationUID = locID, CustomerData = self.customerData)
				return self.requestResponse
			except Execption as e:
				print "An Error occurred during the request: "
				print e
	
	
	def requestNewPassword(self, phone):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#PhoneNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerPhone
		try:
			self.requestResponse getattr(self.client.service, 'CABSERVER.requestNewPasswords')(CommonParams = self.commonParams, phone)
			return self.requestResponse
		except Execption as e:
			print "An Error occurred during the request: "
			print e
	
	"""	
	def checkTripStart(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
				
	def changePersCode(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#persCode: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeCode
	
	def getBikeInfo(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		
	def listProductInfo(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
	
	def addCustomer(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#NewCustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_NewCustomerData
	
	def reportDamage(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#DamageData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_DamageData
	
	def redeemBonusCode(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BonusCode: http://www.w3.org/2001/XMLSchema:string
	
	def listCompletedTrips(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#TripLimits: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_TripLimits
	"""