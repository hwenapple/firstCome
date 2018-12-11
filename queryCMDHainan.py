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

sessionID = '72942B38A9004A9AB29A13BCD61E3F30.s5'
userID = '49'

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
#20190420
#, '20190417',
interestedDates = ['2018-08-10', '2018-08-11', '2018-08-12','2018-08-13']
#interestedDates = ['2019-06-05', '2019-03-08','2018-11-14', '2019-03-15']
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


def stripChinese(inputStr):
	out = ''
	for w in inputStr:
		if w>= u'\u4e00' and w<=u'\u9fa5':
			out += ' '
			continue
		out += w
	return out


def parseHTML(html):
	results = []
	with io.open('search6.html', 'r', encoding="utf-8") as myfile:
		data = myfile.read()
		data = html
		soup = BeautifulSoup(data, "html.parser")
		#id="validCode"
		validInput = soup.find('div', id='validCode')
		flightIn = soup.find('div', id='go_fight_div')
		if validInput:
			message = 'we are getting validInput, may be cookie expired'
			sendErrorMessage(message)
			return
		if not flightIn:
			print "request timed out, some how we dont have flight In {}".format(flightIn)
			loginForm = soup.find('input', id = 'userName_login')
			if loginForm:
				message = 'our cookie has expired, we should update hainan search'
				sendErrorMessage(message)
		else:
			calInputs = soup.find_all('input', id=re.compile("^listmileage"))
			selectedInput = None
			for calInput in calInputs:
				if 'checked' in calInput.attrs:
					selectedInput = calInput
					break
			if not selectedInput:
				print "we probaly dont have anything on this day, move on"
			else:
				departDate = selectedInput.attrs['onclick'].split("('")[-1].split("'")[0]
				sections = flightIn.find_all('div', class_=re.compile("^section"))
				for section in sections:
					flightResult = {}
					nonMid = section.find_all('div', class_=re.compile("^non-mid"))
					if not nonMid:
						print "its not a non stop flight, move on"
						continue
					bussinessCabinID = "cabin_li_gdc"
					bussinessCabin = section.find('li', id=re.compile("^cabin_li_gdc"))
					if not bussinessCabin:
						print "we dont have bussinessCabin avaible, move on"
						continue
					if '-' in bussinessCabin.text:
						print "we have no points displayed here, move on"
						continue
					airportInfos = section.find_all('div', class_=re.compile("^airport"))
					departureInfo = ""
					for airportInfo in airportInfos:
						info = stripChinese(airportInfo.text)
						print info
						departureInfo = info
						break;
					splits = section.text.split('|')
					for split in splits:
						if 'HU' in split:
							flightResult['flight'] = split
							break
					flightResult['status'] = "Business available"
					flightResult['location'] = ' '.join(departureInfo.split())
					flightResult['time'] = departDate
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

def sendMessage(results):
	finalMassege = ""
	for result in results:
		finalMassege += "From cmd hainan search: " + result['time'] + '#' + result['location'] + "#" + result['flight'] + "#" + result['status'] + "            "
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
	os.system(cmd) 





def monthConvert(month):
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	return months[int(month) - 1]




def getQueryCities(airportCode):
	cityNameMap = {'PVG':'Shanghai,(PVG)',
					'SFO':'San+Francisco,(SFO)',
					'SEA':'Seatle,(SEA)',
					'SJC':'San+Jose,(SJC)',
					'PEK':'Beijing,(PEK)'
	}
	if airportCode in cityNameMap:
		return cityNameMap[airportCode]
	return airportCode



def curlForOurTicket(ori, dest, departDate):
	cookies = {
	    'JSESSIONID': sessionID,
	    'SEARCHCITY': 'PEK,SJC,I#PVG,SEA,I',
	    'UID': 'xcaeXXSmNiPXs4AIUWs6/g==',
	    '4_vq': userID,
	    'cookieWindow': 'CN',
	}


	headers = {
	    'Host': 'ffp.hnair.com',
	    'Accept': 'text/html,application/xhtml xml,application/xml;q=0.9,*/*;q=0.8',
	    'Accept-Language': 'en-us',
	    'Origin': 'http://ffp.hnair.com',
	    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0.2 Safari/604.4.7',
	    'Upgrade-Insecure-Requests': '1',
	    'Referer': 'http://ffp.hnair.com/FFPClub/redeemTicket/user/searchView',
	}

	data = [
	  ('tripType', '1'),
	  ('orgCodeX', '({0})'.format(ori)),
	  ('orgCode', '{}'.format(ori)),
	  ('orgCode_domOrInt', 'D'),
	  ('dstCodeX', '({})'.format(dest)),
	  ('dstCode', '{}'.format(dest)),
	  ('dstCode_domOrInt', 'I'),
	  ('departDate', '{}'.format(departDate)),
	  ('airLine', 'HU'),
	  ('cabin', '3'),
	  ('adultCount', '1'),
	  ('childCount', '0'),
	  ('nonstop', '1'),
	]

	response = requests.post('http://ffp.hnair.com/FFPClub/redeemTicket/user/searchData/0', headers=headers, cookies=cookies, data=data)

	print response.status_code
	if response.status_code == 200:
		return response.content
	sendErrorMessage(response.content)
	return None

def sendErrorMessage(errorStr):
	errorStr += " from cmd hainan"
	errorStr = ' '.join(errorStr.split())
	errorStr = re.sub('[^0-9a-zA-Z]+', ' ', errorStr)
	if 'Max retries exceeded' in errorStr:
		print "we are query to many, we cool down a bit"
		time.sleep(300)
	global errorCount
	errorCount = errorCount + 1
	if not errorCount > 20:
		print "we are not over error message threshHold yet, dont report"
		return

	if errorCount > 25:
		errorStr = "we are over the error limit for hainan search, we abort the program and wait for update"
	print "sendErrorMessage {}".format(errorStr)
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(errorStr)
	os.system(cmd) 
	if errorCount > 25:
		sys.exit(1)

def routeQuery(ori, dest, departDate, isJapan = False):
	print "checking {} {} {}".format(ori, dest, departDate)
	htmlData = None
	htmlData = curlForOurTicket(ori, dest, departDate)
	if htmlData:
		print "We have results returned, we now parse it"
		parseHTML(htmlData)
	time.sleep(10)


def start():
	global currentTotalExceptions
	while True:
		print "\n----------------------------we are trying the infinite cmd search via hainan------------------------------\n"
		numOfDatesToQuery = len(interestedDates)
		exceptionCount = 0
		threshHold = numOfDatesToQuery / 2
		shoudRestart = False
		#start isolated search
		exceptionThreshhold = False
		for departDate in interestedDates:
			print "We are now querying {0}".format(departDate)
			try:
				routeQuery('PVG','SEA', departDate)
				routeQuery('PEK','SJC', departDate)
			except Exception as e:
				currentTotalExceptions = currentTotalExceptions + 1
				message = "We have exception {}".format(e)
				print message
				sendErrorMessage(message)
				traceback.print_exc()
				time.sleep(5)
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
	global interestedDates
	newDates = []
	startDate = datetime.datetime.today()
	for x in xrange(1,5):
		startDate += datetime.timedelta(days=1)
		strDate = startDate.strftime('%Y-%m-%d')
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


