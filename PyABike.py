import datetime
from suds import WebFault
from suds.client import Client
from suds.plugin import *


class PyABike:
	client = ''
	def __init__(self):		
		url = 'https://xml.dbcarsharing-buchung.de/hal2_cabserver/definitions/HAL2_CABSERVER_3.wsdl' # current api url
		self.client = Client(url, faults=False)

		self.buildCommonParams()


	def buildCustomerData(self, user, passwd):
		if user != '' and passwd != '':
			self.customerData = self.client.factory.create('Type_CustomerData')
			self.customerData.Password = passwd
			self.customerData.Phone = user
			
			return True
		elif hasattr(self, 'customerData'):
			return True
		else:
			return False


	def buildGeoPos(self, longitude, latitude):
		if longitude != 0.0 and latitude != 0.0:
			self.geoPos = self.client.factory.create('Type_GeoPosition');
			self.geoPos.Longitude = longitude
			self.geoPos.Latitude = latitude
			
			return True
		elif hasattr(self, 'geoPos'):
			return True
		else:
			return False


	def buildCommonParams(self):
		self.commonParams = self.client.factory.create('Type_CommonParams');

		userData = self.client.factory.create('Type_UserData');
		userData.User = 't_cab_android' #from android app
		userData.Password = '3b3cc28469' #from android app

		self.commonParams.UserData = userData
		self.commonParams.LanguageUID = 1 #only option
		self.commonParams.RequestTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		self.commonParams.Version = 1 #only option		
	


	#requires self.payment
	def buildNewCustomerData(self, productID, name, surname, sex, birthday, street, number, town, zipCode, countryCode, email, phone):
		if hasattr(self, 'payment'):
			self.newCustomerData = self.client.factory.create('Type_NewCustomerData')
			if sex == 'm' or sex == 'w':
				self.newCustomerData.Sex 	= sex
			else:
				raise Exception('Invalid Sex')
			self.newCustomerData.Forename		= name
			self.newCustomerData.Surname		= surname
			self.newCustomerData.Birthday		= birthday
			self.newCustomerData.Street			= street
			self.newCustomerData.Streetnumber	= number
			self.newCustomerData.Town			= town
			self.newCustomerData.Zipcode		= zipCode
			self.newCustomerData.CountryCode 	= countryCode
			self.newCustomerData.Email			= email
			self.newCustomerData.Phonenumber	= phone
			self.newCustomerData.Payment		= self.payment
			if hasattr(self, 'bonusCard'):
				self.newCustomerData.BonusCard	= self.bonusCard
			self.newCustomerData.ProductID		= productID
		else:
			raise Exception('Missing payment data requirements')


	#iban and bic or bankcode and accountNumber are required
	#maybe split up into two functions
	def buildPaymentByWire(self, iban = 0, bic = 0, bankcode = 0, accountNumber = 0):
		self.payment = self.client.factory.create('Type_Payment')
		self.payment.PaymentMethod = 'L'
		
		self.wire = self.client.factory.create('Type_BankAccount')
		self.wire.IBAN			= iban
		self.wire.BIC			= bic
		self.wire.Bankcode		= bankcode
		self.wire.AccountNumber	= accountNumber


	def buildPaymentByCreditCard(self, cardNumber, expirationDate):
		self.payment = self.client.factory.create('Type_Payment')
		self.payment.PaymentMethod = 'K'
		
		self.creditCard = self.client.factory.create('Type_Creditcard')
		self.creditCard.CardNumber 		= cardNumber
		self.creditCard.ExpirationDate 	= expirationDate
		
		self.payment.CreditCard = self.creditCard


	def buildBounusCard(self, cardID, cardNumber, validDate, validDateFrom):
		self.bonusCard = self.client.factory.create('Type_BounusCard')
		
		self.bonusCard.CardID = cardID
		self.bonusCard.CardNumber = cardNumber
		self.bonusCard.ValidDate = validDate
		self.bonusCard.ValidDateFrom = validDateFrom


	def buildTripLimits(self, firstEntry = 0, entryCount = 20, startTime = '', endTime = ''):
		self.tripLimits = self.client.factory.create('Type_TripLimits')
		self.tripLimits.FirstEntry = firstEntry
		self.tripLimits.EntryCount = entryCount
		self.tripLimits.StartTime = startTime
		self.tripLimits.EndTime = endTime


	def buildDamageData(self, text, bike = 0, locID = 0):
		if hasattr(self, 'damageData') == False and text != '':
			if locID == 0 and bike != 0:
				self.damageData = self.client.factory.create('Type_DamageData')
				self.damageData.Text		= text
				self.damageData.BikeNumber	= bike
				
				return True
			elif bike == 0 and locID != 0:
				self.damageData = self.client.factory.create('Type_DamageData')
				self.damageData.Text		= text
				self.damageData.LocationUID	= locID
				
				return True
			else:
				raise Exception('BikeNumber oder LocationUID must be set')
		else:
			raise Exception('No damage description was given')
		
		return False


	def listFreeBikes(self, maxRes = 100, radius = 5000, longitude = 0.0, latitude = 0.0):
		if self.buildGeoPos(longitude, latitude):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.listFreeBikes')(CommonParams = self.commonParams, SearchPosition = self.geoPos, maxResults = maxRes, searchRadius = radius)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('There is no place like ::1') # no valid ongitude and latitude supplied



	#auth required
	def getCustomerInfo(self, user = '', passwd = ''):
		#CommonParams: 
		#CustomerData:
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.getCustomerInfo')(CommonParams = self.commonParams, CustomerData = self.customerData)
				return self.requestResponse
			except Exception as e:
				print e
		else:
			raise Exception('No username and password supplied for function getCustomerInfo')


	def listReturnLocations(self, bike, maxRes = 100, radius = 5000, longitude = 0.0, latitude = 0.0):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		#SearchPosition: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_GeoPosition
		#maxResults: http://www.w3.org/2001/XMLSchema:int
		#searchRadius: http://www.w3.org/2001/XMLSchema:int
		if self.buildGeoPos(longitude, latitude):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.listReturnLocations')(CommonParams = self.commonParams, BikeNumber = bike, SearchPosition = self.geoPos, maxResults = maxRes, searchRadius = radius)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('There is no place like ::1') # no valid longitude and latitude supplied



	#auth required
	def rentBike(self, bike, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.rentBike')(CommonParams = self.commonParams, CustomerData = self.customerData, BikeNumber = bike)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception("No username and password supplied for function rentBike")


	def returnBike(self, bike, retCode, locID, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		#ReturnCode: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeCode
		#LocationUID: http://www.w3.org/2001/XMLSchema:int
		#CustomerDataOptional: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerDataOptional
		if user == '' and passwd == '':	
			self.customerData = ''
		else:
			self.buildCustomerData(user, passwd)

		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.returnBike')(CommonParams = self.commonParams, BikeNumber = bike, ReturnCode = retCode, LocationUID = locID, CustomerDataOptional = self.customerData)
			return self.requestResponse
		except Exception as e:
			print "An Error occurred during the request: "
			print e


	def requestNewPassword(self, phone):
		#really slow send SMS with text: "Ihre Call a Bike Kundennummer lautet: <CustomerID>.Ihr Passwort lautet: <Password [a-zA-Z0-9\+]{8}>" fro the number +49 173 7290391
		#Password may contain more special chars
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#PhoneNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerPhone
		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.requestNewPassword')(CommonParams = self.commonParams, PhoneNumber = phone)
			return self.requestResponse
		except Exception as e:
			print "An Error occurred during the request: "
			print e


	def listProductInfo(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.listProductInfo')(CommonParams = self.commonParams)
			return self.requestResponse
		except Exception as e:
			print "An Error occurred during the request: "
			print e


	#auth required
	def checkTripStart(self, bike, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.checkTripStart')(CommonParams = self.commonParams, CustomerData = self.customerData, BikeNumber = bike)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('No username and password supplied for function checkTripStart')


	#auth required
	def changePersCode(self, code, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#persCode: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeCode
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.changePersCode')(CommonParams = self.commonParams, CustomerData = self.customerData, persCode = code)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('No username and password supplied for function changePersCode')


	def getBikeInfo(self, bike):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#BikeNumber: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_BikeNumber
		try:
			self.requestResponse = getattr(self.client.service, 'CABSERVER.getBikeInfo')(CommonParams = self.commonParams, BikeNumber = bike)
			return self.requestResponse
		except Exception as e:
			print "An Error occurred during the request: "
			print e


	#auth required
	def redeemBonusCode(self, bonusCode, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#BonusCode: http://www.w3.org/2001/XMLSchema:string
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.changePersCode')(CommonParams = self.commonParams, CustomerData = self.customerData, BonusCode = bonusCode)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('No username and password supplied for function redeemBonusCode')


	def addCustomer(self):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#NewCustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_NewCustomerData
		if hasattr(self, 'newCustomerData'):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.addCustomer')(CommonParams = self.commonParams, NewCustomerData = self.newCustomerData)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('No Customer specified')



	#auth required
	def reportDamage(self, damageText = '', bike = 0, locID = 0, user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#DamageData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_DamageData
		if self.buildDamageData(damageText, bike, locID):
			if self.self.buildCustomerData(user, passwd):
				try:
					self.requestResponse = getattr(self.client.service, 'CABSERVER.reportDamage')(CommonParams = self.commonParams, CustomerData = self.customerData, DamageData = self.damageData)
					return self.requestResponse
				except Exception as e:
					print "An Error occurred during the request: "
					print e
			else:
				raise Exception('No customerData supplied')
		else:
			raise Exception('No damage to report')


	#auth required
	def listCompletedTrips(self, firstEntry = 0, entryCount = 20, startTime = '', endTime = '', user = '', passwd = ''):
		#CommonParams: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CommonParams
		#CustomerData: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_CustomerData
		#TripLimits: https://xml.dbcarsharing-buchung.de/hal2_cabserver/:Type_TripLimits
		self.buildTripLimits(firstEntry, entryCount, startTime, endTime)
		
		if self.buildCustomerData(user, passwd):
			try:
				self.requestResponse = getattr(self.client.service, 'CABSERVER.listCompletedTrips')(CommonParams = self.commonParams, CustomerData = self.customerData, TripLimits = self.tripLimits)
				return self.requestResponse
			except Exception as e:
				print "An Error occurred during the request: "
				print e
		else:
			raise Exception('No customerData supplied')
