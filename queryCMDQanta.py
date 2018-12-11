import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select
import time
from optparse import OptionParser
from bs4 import BeautifulSoup
import re
import time
import datetime
import subprocess
import traceback
from os.path import expanduser
import sys
import requests
import io

#if we are just testing the script
devTest = False

# 2 means both first and business, 1 only business, 0 only first
searchMode = 2

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
#20190420
#, '20190417',
interestedDates = ['20181221','20181222','20181223']
#HKG-TLV no flight on sunday
interestedDates = ['20190114','20190115', '20190120', '20190121']

#interestedDates = ['20181210']
landingSearchDate = '05/19/2018'
landingSpan = 1

currentTotalExceptions = 0
accounts = ['1675359815', '1675587382', '1675587444']
accountIndex = 0

home = expanduser("~")
screenshotDir = "{0}/Desktop/screenshots".format(home)

useChrome = True

url = "https://www.alaskaair.com/"

errorCount = 0

def insert_space(string, integer):
	return string[0:integer] + ' ' + string[integer:]

def shouldIgnore(flightResult):
	if 'Mon 10 Dec' in flightResult['time'] and 'Business' in flightResult['status']:
		print "we know about this one, dont report"
		return True
	if 'Mon 17 Dec' in flightResult['time'] and 'Business' in flightResult['status']:
		print "we know about this one, dont report"
		return True
	return False


def parseHTML(html, expectedAirline = None, allowedSegments = 1, expectedLongSegDest = None, expectedAirlineAllTheWay = False):
	#print html
	results = []
	with io.open('search5.html', 'r', encoding="utf-8") as myfile:
		data = myfile.read()
		if html:
			data = html
		if 'Alternative' in data:
			print "we dont have anything for that day, system suggested Alternative dates"
		else:
			soup = BeautifulSoup(data, "html.parser")
			flightIn = soup.find('div', id='flightIn')
			if not flightIn:
				print "some how we dont have flight In {}".format(flightIn)
			else:
				tbodys = flightIn.find_all('tbody')
				for tbody in tbodys:
					flightResult = {}
					trs = tbody.find_all('tr', id=re.compile("^idLine"))
					if len(trs) > allowedSegments:
						#it's more than allowed segment, we skip
						print "allowed segments {0}, current segments {1}".format(allowedSegments, len(trs))
						continue
					#we always get the last segment
					tr = trs[-1]
					if len(trs) == 2:
						#we have a 2 segment flight, need to find out which is shorter
						shortFlightRow = None
						duration1 = trs[0].find('span', {"class": "duration"}).text
						duration1 = re.sub("\D", "", duration1)
						duration2 = trs[1].find('span', {"class": "duration"}).text
						duration2 = re.sub("\D", "", duration2)
						if int(duration1) > int(duration2):
							tr = trs[0]
							shortFlightRow = trs[1]
						else:
							tr = trs[-1]
							shortFlightRow = trs[0]					
						previousFN = shortFlightRow.find('th', {"class": "flight-number"}).text
						flightResult['prevFlight'] = previousFN
					th = tr.find('th', id=re.compile("^bloc"))
					departureTime = th.find('span', {"class": "time"}).text
					location = th.find('span', {"class": "location"}).text
					flightNumber = tr.find('th', {"class": "flight-number"}).text
					if expectedAirline:
						if expectedAirline not in flightNumber:
							#we dont have the airline we are looking for, we skip
							print "expectedAirline {0}, actual flightNumber {1}".format(expectedAirline, flightNumber)
							continue
						if expectedAirlineAllTheWay:
							if expectedAirline not in flightResult['prevFlight']:
								print "expectedAirline {0}, actual previous flightNumber {1}".format(expectedAirline, flightResult['prevFlight'])
								continue
					div = soup.find('div', {"class": "date"})
					departDate = div.find('p').text
					print departDate
					#somehow class information are always on first row
					seatRow = trs[0]
					if seatRow.find('td', id=re.compile("_BU")):
						status = seatRow.find('td', id=re.compile("_BU")).text
						print "Business flight status {} ".format(status)
						validTrip = True
						validTripStr = '{} will be in'.format(expectedLongSegDest)
						print validTripStr
						if validTripStr in status:
							print "we dont want non Business filght in our last route, we invalide trip"
							validTrip = False
						if 'No Seats' not in status and validTrip:
							flightResult['status'] = "Business available"
					if seatRow.find('td', id=re.compile("_FI")):
						status = seatRow.find('td', id=re.compile("_FI")).text
						print "First flight status {} end".format(status)
						validTrip = True
						validTripStr = '{} will be in'.format(expectedLongSegDest)
						print validTripStr
						if validTripStr in status:
							print "we dont want non first filght in our last route, we invalide trip"
							validTrip = False
						if 'No Seats' not in status and validTrip:
							if 'status' in flightResult:
								flightResult['status'] += " First available"
							else:
								flightResult['status'] = "First available"

					# if seatRow.find('td', id=re.compile("ECO")):
					# 	status = seatRow.find('td', id=re.compile("ECO")).text
					# 	print "Economy flight status {} ".format(status)
					# 	if 'No Seats' not in status:
					# 		if 'status' in flightResult:
					# 			flightResult['status'] += " Economy available"
					# 		else:
					# 			flightResult['status'] = "Economy available"

					# we have either first or business class available or economy avaiable 
					if 'status' in flightResult:
						if 'available' in flightResult['status']:
							flightResult['flight'] = flightNumber
							flightResult['location'] = location
							flightResult['time'] = departDate + "_" + departureTime
							shouldAddResult = True
							for addedResult in results:
								if addedResult['flight'] == flightNumber:
									#we already have this flight, we dont add
									shouldAddResult = False
									break
							if shouldAddResult:
								results.append(flightResult)
						# print departureTime
						# print location
						# print flightNumber
						# print status
	ts = time.time()
	sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
	print "\n=================================={0}=============================\n".format(sttime)
	if len(results) > 0:
		print "\nwe got available flights \n"
		print results
		print "\n"
		sendMessage(results)
	else:
		print "\nwe dont have flights available \n"
	print "\n==================================END=============================\n"

def sendMessage(results):
	finalMassege = ""
	for result in results:
		if searchMode == 1:
			if 'Business' not in result['status']:
				continue
		if searchMode == 0:
			if 'First' not in result['status']:
				continue
		if shouldIgnore(result):
			continue
		finalMassege += "From cmd qanta search: " + result['time'] + '#' + result['location'] + "#" + result['flight'] + "#" + result['status']
		if 'prevFlight' in result:
			#if we have previous flight
				finalMassege += ' #prev flight ' + result['prevFlight'] + '#'
		finalMassege += "        "
	if finalMassege == "":
		return
	textMessage(finalMassege)



def textMessage(message):
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(message)
	os.system(cmd)
	time.sleep(5)
	cmd = 'osascript sendMessage.scpt 4159944384 "{0}"'.format(message)
	os.system(cmd) 	


def monthConvert(month):
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	return months[int(month) - 1]




def getQueryCities(airportCode):
	cityNameMap = {'PVG':'Shanghai',
					'SFO':'San Francisco',
					'SEA':'Seatle',
					'SJC':'San Jose',
					'PEK':'Beijing',
					'HKG':'Hong Kong',
					'TLV':'Tel Aviv',
					'LAX':'Los Angeles'
	}
	if airportCode in cityNameMap:
		return cityNameMap[airportCode]
	return airportCode

def curlForOurTicketGeneral(ori, dest, departDate, officeID):

	cookies = {
	}

	headers = {
	    'Host': 'book.qantas.com.au',
	    'accept': 'text/html,application/xhtml xml,application/xml;q=0.9,*/*;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://www.qantas.com',
	    'accept-language': 'en-us',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
	    'referer': 'https://www.qantas.com/tripflowapp/awardBooking.tripflow',
	}

	params = (
	    ('quc', 'locale'),
	)

	data = 'WDS_DISABLE_XBAG_RTA=FALSE&TRIP_TYPE=O&BOOKING_ENTRY_POINT=CLASSIC BOOKING&COMMERCIAL_FARE_FAMILY_1_1=AWARDECO&WDS_DISABLE_SEAT_RTA=FALSE&PREF_AIR_FREQ_MILES_1_1=0&WDS_DISABLED_CARD_CVV=FALSE&SO_SITE_IS_INSURANCE_ENABLED=FALSE&TRAVELLER_TYPE_1=ADT&B_LOCATION_1={1}&SO_SITE_MIN_AVAIL_DATE_SPAN=H3&DIRECT_LOGIN=YES&BOOKING_FLOW=AWARD&DISPLAY_TYPE=1&WDS_SPLIT_PAYMENT_ACTIVATION=FALSE&WDS_DISABLED_CARD_RTA=FALSE&PREF_AIR_FREQ_LEVEL_1_1=FFBR&USER_ID=4007C60CF&PREF_AIR_FREQ_AIRLINE_1_1=QF&WDS_DISABLE_ALL_INCLUSIVE=TRUE&TYPE_1=ADT&MODIFY_SEARCH_URL=https://www.qantas.com/travel/airlines/flight-search/global/en?showMod=0&FIRST_NAME_1=haoran&LANGUAGE=GB&LAST_NAME_1=wen&PREF_AIR_FREQ_NUMBER_1_1=1938908959&COMMERCIAL_FARE_FAMILY_TYPE_2=U&WDS_USE_OLD_MINIRULES=TRUE&COMMERCIAL_FARE_FAMILY_TYPE_1=C&SITE=QFQFQFFA&PRICING_TYPE=C&WDS_DISABLE_C2C_AMOP=FALSE&EMBEDDED_TRANSACTION=FlexPricerAvailabilityServlet&PASSWORD_2=AWARD&ENCT=1&PASSWORD_1=AWARD&TITLE_1=MR&PAGE_FROM=/bookingError/v1/redirect/us/en/book-a-trip/flights.html&B_DATE_1={0}0000&ARRANGE_BY=RN&SO_SITE_OFFICE_ID={3}QF08RR&SKIN=P&E_LOCATION_1={2}&SO_SITE_FP_POJO_ACTIVE=1&CONTACT_POINT_MOBILE=412000000&WDS_DISABLE_XBAG_CVV=TRUE&CONTACT_POINT_EMAIL_1=harrywenhr@gmail.com&WDS_ACTIVATE_SHOPPING_BASKET=TRUE&PREF_AIR_FREQ_PIN_1_1=6666&WDS_ACTIVATE_POINTS_CAR=TRUE&WDS_DISABLE_SEAT_CVV=FALSE&COMMERCIAL_FARE_FAMILY_2_1=AWARDALL&WDS_DISABLE_NPS=TRUE'.format(departDate, ori, dest, officeID)
	
	response = requests.post('https://book.qantas.com.au/pl/QFAward/wds/OverrideServlet#en%7CtvlDates#{0}0000%7Ccountry#US%7Ctvldate#{0}%7Cregion#AM%7Cdep#{1}%7Carr#{2}&alt_cam_param=&QF_Value=094138235183230130140180093240048011073247104215'.format(departDate, ori, dest), headers=headers, params=params, cookies=cookies, data=data)

	print response.status_code
	if response.status_code == 200:
		return response.content
	sendErrorMessage(response.content)
	return None


def sendErrorMessage(errorStr):
	global errorCount
	errorCount = errorCount + 1
	if not errorCount > 30:
		print "we are not over error message threshHold yet, dont report {}".format(errorStr)
		return
	errorStr += " from cmd qanta"
	errorStr = ' '.join(errorStr.split())
	errorStr = re.sub('[^0-9a-zA-Z]+', ' ', errorStr)
	if len(errorStr) > 155:
		errorStr = errorStr[:155]
	if errorCount > 40:
		errorStr = "we are over the error limit for qanta search, we abort the program and wait for update"
	print "sendErrorMessage {}".format(errorStr)
	textMessage(errorStr)
	if errorCount > 40:
		sys.exit(1)


def routeQuery(ori, dest, departDate, officeID, expectedAirline = None):
	print "checking {} {} {}".format(ori, dest, departDate)
	if '20180812' in departDate and 'HND' in ori:
		print "we know about this one, skip"
		return
	htmlData = None
	htmlData = curlForOurTicketGeneral(ori, dest, departDate, officeID)
	if htmlData:
		print "We have results returned, we now parse it"
		expectedAirlineAllTheWay = False
		allowedSegments = 1
		expectedLongSegDest = None
		if 'HKG' in ori or 'PVG' in ori:
			expectedAirline = 'CX'
		if 'HKG' in dest or 'PVG' in dest:
			expectedAirline = 'CX'
		if 'SFO' in ori and 'TLV' in dest:
			expectedAirline = 'CX'
			allowedSegments = 2
			expectedAirlineAllTheWay = True
		if 'SFO' in dest and 'TLV' in ori:
			expectedAirline = 'CX'
			allowedSegments = 2
			expectedAirlineAllTheWay = True
		if 'PVG' in ori:
			allowedSegments = 2
			expectedLongSegDest = getQueryCities(dest)
		if 'PVG' in dest:
			allowedSegments = 2
			expectedLongSegDest = getQueryCities('HKG')		
		parseHTML(htmlData, expectedAirline, allowedSegments, expectedLongSegDest, expectedAirlineAllTheWay)
	time.sleep(2)


def start():
	global currentTotalExceptions
	print "we started our qanta search now !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	while True:
		print "\n----------------------------we are trying the infinite cmd search via qanta------------------------------\n"
		numOfDatesToQuery = len(interestedDates)
		exceptionCount = 0
		threshHold = numOfDatesToQuery / 2
		shoudRestart = False
		#start isolated search
		exceptionThreshhold = False
		for departDate in interestedDates:
			print "We are now querying {0}".format(departDate)
			try:
				dateObj = datetime.datetime.strptime(departDate, '%Y%m%d')
				dateObj += datetime.timedelta(days=-1) 
				pvgDepartDate = dateObj.strftime('%Y%m%d')
				if devTest:
					#routeQuery('TLV','LHR', departDate,'LON', 'BA')
					#routeQuery('LHR','SFO', departDate,'LON', 'BA')
					#routeQuery('SFO','TLV', departDate,'LAX')
					#routeQuery('TLV','SFO', departDate,'LON')
					#routeQuery('SFO','PVG', departDate,'LAX')
					#routeQuery('HKG','SFO', departDate,'HKG')
					routeQuery('SFO','HKG', departDate,'LAX')
					routeQuery('SFO','PVG', departDate,'LAX')
					routeQuery('LAX','HKG', departDate,'LAX')
					routeQuery('LAX','PVG', departDate,'LAX')
					#routeQuery('HKG','TLV', departDate,'HKG')
					#routeQuery('TLV','HKG', departDate,'LON')
					#routeQuery('PVG','TLV', departDate,'SHA')
					#routeQuery('TLV','PVG', departDate,'LON')
					#routeQuery('PVG','SFO', departDate,'SHA')
					#routeQuery('HKG','SFO', departDate,'HKG')
					
				else:
					#YVR LON office for TLV
					numberDate = int(departDate)

					#search for 
					if numberDate < 20190101:
						if numberDate == 20181210:
							routeQuery('SFO','PVG', departDate,'LAX')
							routeQuery('SFO','HKG', departDate,'LAX')
						else:
							routeQuery('SFO','PVG', departDate,'LAX')
							routeQuery('SFO','HKG', departDate,'LAX')
							routeQuery('LAX','PVG', departDate,'LAX')
							routeQuery('LAX','HKG', departDate,'LAX')
					elif numberDate < 20190110:
						routeQuery('HKG','TLV', departDate,'HKG')
						routeQuery('PVG','TLV', departDate,'HKG')
						print "pvgDepartDate {}".format(pvgDepartDate)
						routeQuery('PVG','TLV', pvgDepartDate,'SHA')
					elif numberDate < 20190118:
						routeQuery('TLV','HKG', departDate,'LON')
						routeQuery('TLV','PVG', departDate,'LON')
						if numberDate == 20190115:
							routeQuery('LHR','SFO', departDate,'LON', 'BA')
					elif numberDate < 20190218:
						routeQuery('PVG','SFO', departDate,'SHA')
						routeQuery('HKG','SFO', departDate,'HKG')
						routeQuery('PVG','LAX', departDate,'SHA')
						routeQuery('HKG','LAX', departDate,'HKG')
						print "pvgDepartDate {}".format(pvgDepartDate)
						routeQuery('PVG','SFO', pvgDepartDate,'SHA')
						routeQuery('PVG','LAX', pvgDepartDate,'SHA')
					else:
						routeQuery('SFO','HKG', departDate,'LAX')
				

				

				#routeQuery('PVG','SFO', departDate,'SHA')
				#routeQuery('HKG','SFO', departDate,'HKG')
				#routeQuery('HND','SFO', departDate, 'TYO')

			except Exception as e:
				currentTotalExceptions = currentTotalExceptions + 1
				message = "We have exception {}".format(e)
				print message
				sendErrorMessage(message)
				traceback.print_exc()
				time.sleep(30)
				if currentTotalExceptions > 30:
					print "we have too many exceptions, abort"
					currentTotalExceptions = 0
					break
			print "we have finished querying {0}".format(departDate)
			time.sleep(10)
		print "\n-----------------------------------We have finised one loop, contine with another----------------------\n"
		print "we now wait for 30s before next search"
		getInterestedDates()
		time.sleep(30)


def getInterestedDates():
	return
	global interestedDates,devTest
	devTest = True
	newDates = []
	startDate = datetime.datetime.today()
	startDate += datetime.timedelta(days=1)
	#startDate += datetime.timedelta(days=150)
	#startDate = datetime.datetime.strptime('20181213', '%Y%m%d')
	for x in xrange(1,20):
		startDate += datetime.timedelta(days=1)
		strDate = startDate.strftime('%Y%m%d')
		newDates.append(strDate)
	interestedDates = newDates
	print interestedDates

if __name__ == '__main__':
	getInterestedDates()
	if not os.path.exists(screenshotDir):
		os.makedirs(screenshotDir)
	start()


