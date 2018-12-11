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

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

#if we do 36 queries within 1.5 hour, we are busted
searchCount = 0
interestedDates = ['08/13/2018', '08/14/2018', '08/15/2018', '08/16/2018']
interestedDates = ['12/21/2018', '12/22/2018', '12/23/2018']
#interestedDates = ['03/08/2019', '06/09/2019', '09/21/2018', '08/14/2018']
landingSearchDate = '05/19/2018'
landingSpan = 1

currentTotalExceptions = 0
accounts = ['1675359815', '1675587382', '1675587444']
accountIndex = 0

errorCount = 0


home = expanduser("~")
screenshotDir = "{0}/Desktop/screenshots".format(home)

useChrome = True

url = "https://www.alaskaair.com/"



def insert_space(string, integer):
	return string[0:integer] + ' ' + string[integer:]


def parseHTML(html):
	with io.open('search5.html', 'r', encoding="utf-8") as myfile:
		data = myfile.read()
		if html:
			data = html
		soup = BeautifulSoup(data, "html.parser")
		lis = soup.find_all('li', id=re.compile("^option-0"))
		results = []
		for li in lis:
			#print "whattttt {}".format(li.text.encode('utf-8'))
			flightResult = {}
			if 'Nonstop' not in li.text:
				continue
			#print "kkkkk"
			rowText = ' '.join(li.text.split())
			print "=========================================="
			print rowText
			print "=========================================="
			if '50k' in li.text or '60k' in li.text:
				flightResult['status'] = "Business available"
				flightNumber = li.find('div', class_=re.compile("^optionHeaderFltNum"))
				flightResult['flight'] = flightNumber.text
				selectedDateDiv = soup.find('div', class_=re.compile("^shoulderSelected"))
				selectedDate = selectedDateDiv.text.split('\n')[-3]
				flightTimes = li.find_all('div', class_=re.compile("^DetailsTime"))
				selectedTime = li.find('div', class_=re.compile("^optionTime"))
				flightResult['time'] = selectedDate + ' ' + selectedTime.text
				location = li.find('div', class_=re.compile("^optionCityCode"))
				flightResult['location'] = location.text
				locations = li.find_all('div', class_=re.compile("^DetailsStation"))
				results.append(flightResult)
			
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



def shouldIgnore(flightResult):
	if '7956' in flightResult['flight'] and '21' in flightResult['time'] and 'Business' in flightResult['status']:
		print "we know about this one, dont report"
		return True
	if 'Flight 2' in flightResult['flight'] and '22' in flightResult['time'] and 'Business' in flightResult['status']:
		print "we know about this one, dont report"
		return True
	if 'Flight 2' in flightResult['flight'] and '23' in flightResult['time'] and 'Business' in flightResult['status']:
		print "we know about this one, dont report"
		return True
	return False


def sendMessage(results):
	finalMassege = ""
	for result in results:
		if shouldIgnore(result):
			continue
		finalMassege += "From alaska search: " + result['time'] + '#' + result['location'] + "#" + result['flight'] + "#" + result['status'] + "            "
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
	os.system(cmd) 





def monthConvert(month):
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	return months[int(month) - 1]




def getQueryCities(airportCode):
	cityNameMap = {'PVG':'Shanghai, China (PVG-Shanghai Pu Dong)',
					'SFO':'San Francisco, CA (SFO-San Francisco Intl.)',
					'SEA':'Seattle, WA (SEA-Seattle/Tacoma Intl.)',
					'SJC':'San Jose, CA (SJC-San Jose Intl.)',
					'PEK':'Beijing, China (PEK-Beijing Capital)',
					'HND':'Tokyo, Japan (HND-Tokyo Haneda)'
	}
	if airportCode in cityNameMap:
		return cityNameMap[airportCode]
	return airportCode

def curlForOurTicket(departCity, destCity, departDate):

	cookies = {
	    'ADRUM': 's=1531964907348&r=https://m.alaskaair.com/shopping?0',
	    'Price0': 'l',
	    'Price1': 'l',
	    'ShowFilter0': '1',
	    'ShowFilter1': '1',
	    '_px2': 'eyJ1IjoiMTM4NDAxNDAtOGJjMC0xMWU4LWJjN2MtN2QzZGFhNjdjM2YyIiwidiI6ImMzMDM3MmIwLTgzYzEtMTFlOC1iZDE1LTNmZGNmZjlkZTMwNyIsInQiOjE1MzIwNTIyNzE0MzEsImgiOiI1MjU5NjIyZDgxZTNkZGIxYzJiMjg3NGExNDI4OGE4M2U3MjY0ZDY4ZTA0MDhlZTY0ZjFjMzgwOGZkMzhjZTM5In0=',
	    'DepFare': '',
	    'DepOptId': '-1',
	    'RetFare': '',
	    'RetOptId': '-1',
	    'ShowAllDep': '',
	    'ShowAllRet': '',
	    'SortBy0': '1',
	    'SortBy1': '1',
	    'VrtPos': '0',
	    'PersistentHeader': '',
	    '_pxff_tm': '1',
	}

	headers = {
	    'Host': 'm.alaskaair.com',
	    'accept': 'text/html,application/xhtml xml,application/xml;q=0.9,*/*;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded',
	    'origin': 'https://m.alaskaair.com',
	    'accept-language': 'en-us',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
	    'referer': 'https://m.alaskaair.com/shopping',
	}

	data = [
	  ('CacheId', ''),
	  ('ClientStateCode', 'CA'),
	  ('SaveFields.DepShldrSel', 'False'),
	  ('SaveFields.RetShldrSel', 'False'),
	  ('SaveFields.SelDepOptId', '-1'),
	  ('SaveFields.SelDepFareCode', ''),
	  ('SaveFields.SelRetOptId', '-1'),
	  ('SaveFields.SelRetFareCode', ''),
	  ('SearchFields.IsAwardBooking', 'true'),
	  ('SearchFields.IsAwardBooking', 'false'),
	  ('SearchFields.SearchType', 'OneWay'),
	  ('SearchFields.DepartureCity', '{}'.format(departCity)),
	  ('SearchFields.ArrivalCity', '{}'.format(destCity)),
	  ('SearchFields.DepartureDate', '{}'.format(departDate)),
	  ('SearchFields.ReturnDate', ''),
	  ('SearchFields.NumberOfTravelers', '1'),
	  ('SearchFields.PriceType', 'Lowest'),
	  ('SearchFields.UpgradeOption', 'none'),
	  ('SearchFields.DiscountCode', ''),
	  ('DiscountCode', ''),
	  ('SourcePage', 'Search'),
	  ('deals-link', ''),
	  ('SearchFields.IsCalendar', 'false'),
	]
	response = requests.post('https://m.alaskaair.com/shopping/flights', headers=headers, cookies=cookies, data=data)
	print response.status_code
	#print response.content
	if response.status_code == 200:
		return response.content
	sendErrorMessage(response.content)
	return None

def sendErrorMessage(errorStr):
	global errorCount
	errorCount = errorCount + 1
	if not errorCount > 5:
		print "we are not over error message threshHold yet, dont report"
		return
	errorStr += " from cmd alaska"
	errorStr = ' '.join(errorStr.split())
	errorStr = re.sub('[^0-9a-zA-Z]+', ' ', errorStr)
	if len(errorStr) > 155:
		errorStr = errorStr[:155]
		errorStr = 'From alaska search ' + errorStr
	if errorCount > 10:
		errorStr = "we are over the error limit for alaska search, we abort the program and wait for update"
	print "sendErrorMessage {}".format(errorStr)
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(errorStr)
	os.system(cmd)
	if errorCount > 10:
		sys.exit(1)


def routeQuery(ori, dest, departDate):
	global searchCount
	searchCount += 1
	# if searchCount > 30:
	# 	print "we have search for over 30 queries now, we stop for 30 minutes"
	# 	searchCount = 0
	# 	time.sleep(1800)
	# 	searchCount = 0
	print "checking {} {} {}".format(ori, dest, departDate)
	departCity = getQueryCities(ori)
	destCity = getQueryCities(dest)
	htmlData = curlForOurTicket(departCity, destCity, departDate)
	if htmlData:
		print "We have results returned, we now parse it"
		#print htmlData
		parseHTML(htmlData)
	time.sleep(10)


def start():
	
	global currentTotalExceptions
	while True:
		print "\n----------------------------we are trying the infinite search via alaskaair------------------------------\n"
		try:
			numOfDatesToQuery = len(interestedDates)
			exceptionCount = 0
			threshHold = numOfDatesToQuery / 2
			shoudRestart = False
			#start isolated search
			exceptionThreshhold = False
			for departDate in interestedDates:
				print "We are now querying {0}".format(departDate)
				# routeQuery('HND','SFO', departDate)
				# routeQuery('PEK','SJC', departDate)
				# routeQuery('PVG','SEA', departDate)
				routeQuery('SFO','HND', departDate)
				routeQuery('SJC','PEK', departDate)
				routeQuery('SEA','PVG', departDate)
				print "we have finished querying {0}".format(departDate)
				time.sleep(10)
		except Exception as e:
			currentTotalExceptions = currentTotalExceptions + 1
			message = "We have exception {}".format(e)
			sendErrorMessage(message)
			traceback.print_exc()
			time.sleep(30)
			if currentTotalExceptions > 10:
				print "we have too many exceptions, abort"
				break
			continue
		print "\n-----------------------------------We have finised one loop, contine with another----------------------\n"
		print "we now wait for 60 minute before next search"
		getInterestedDates()
		time.sleep(3600)


def getInterestedDates():
	return
	global interestedDates
	newDates = []
	startDate = datetime.datetime.today()
	startDate += datetime.timedelta(days=1)
	for x in xrange(1,5):
		startDate += datetime.timedelta(days=1)
		strDate = startDate.strftime('%m/%d/%Y')
		newDates.append(strDate)
	print newDates
	interestedDates = newDates

if __name__ == '__main__':
	getInterestedDates()
	# parseHTML("","","")
	# sys.exit(1)
	if not os.path.exists(screenshotDir):
		os.makedirs(screenshotDir)
	start()


