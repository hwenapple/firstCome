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
import traceback
from os.path import expanduser
from threading import Timer

home = expanduser("~")
screenshotDir = "{0}/Desktop/screenshots".format(home)
stopLoop = False
ourBrowser = None

class AnyEc:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args
    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver): return True
            except:
                pass


def check_exists_id(browser, idName):
    try:
        result = browser.find_element_by_id(idName)
    except Exception as e:
    	print "we have exception in check exists {0}".format(e)
        return False
    return True

def check_exists_xpath(browser, path):
    try:
        result = browser.find_elements_by_xpath(path)
        if len(result) > 0:
        	return True
    except Exception as e:
    	print "we have exception in check exists {0}".format(e)
        return False
    return False



def getToSearchPage(browser):
	time.sleep(1)
	loginButtonPath = '//*[@id="header"]/div/div[2]/button'
	results = browser.find_elements_by_xpath(loginButtonPath);
	results[0].click()
	time.sleep(3)

	userName = "1938908959"
	membershipNumberPath = '//input[@aria-label="Membership Number"]'
	results = browser.find_elements_by_xpath(membershipNumberPath);
	results[0].send_keys(userName);
	time.sleep(1)

	lastName = "wen"
	lastNamePath = '//input[@aria-label="Last name"]'
	results = browser.find_elements_by_xpath(lastNamePath);
	results[0].send_keys(lastName);
	time.sleep(1)

	pin = "1228"
	pinPath = '//input[@aria-label="PIN Number"]'
	results = browser.find_elements_by_xpath(pinPath);
	results[0].send_keys(pin);
	time.sleep(1)

	browser.execute_script("document.querySelector('#randomId1').click()")
	time.sleep(1)

	buttons = browser.find_elements_by_xpath("//*[contains(text(), 'LOG IN')]")
	buttons[0].click()
	time.sleep(2)
	url = "https://www.qantas.com/us/en.html"
	browser.get(url)
	time.sleep(2)




def searchOurTicket(browser, ori, dest, departDate):
	inputID ='classic'
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, inputID)))
	inputElement = browser.find_element_by_id(inputID)
	if inputElement.get_attribute('aria-checked') == 'false':
		inputElement.send_keys(Keys.SPACE)
	time.sleep(1)


	onewayID ='oneway'
	inputElement = browser.find_element_by_id(onewayID)
	if inputElement.get_attribute('aria-checked') == 'false':
		#inputElement.click()
		browser.execute_script("document.querySelector('#oneway').click()")
	time.sleep(1)

	departureID = "typeahead-input-from"
	inputElement = browser.find_element_by_id(departureID)
	inputElement.clear()
	inputElement.send_keys(ori)
	inputElement.send_keys('\n')	
	time.sleep(1)

	destiID = "typeahead-input-to"
	inputElement = browser.find_element_by_id(destiID)
	inputElement.clear()
	inputElement.send_keys('San Fran')
	inputElement.send_keys('\n')
	time.sleep(1)

	time.sleep(1)
	navigateDatePicker(browser, departDate)
	time.sleep(2)

	memberID = 'form-member-id-bookFlights'
	if browser.find_elements_by_css_selector('#{0}'.format(memberID)):
		print "we somehow still not signed in, re do it"
		getToSearchPage(browser)
		searchOurTicket(browser, 'HKG', 'SFO', departDate)
		return		


	buttons = browser.find_elements_by_xpath("//*[contains(text(), 'SEARCH FLIGHTS')]")
	buttons[0].click()
	time.sleep(3)

	try:
		buttons = browser.find_elements_by_xpath("//*[contains(text(), 'Continue')]")
		buttons[0].click()
		time.sleep(3)
	except Exception as e:
		print "somehow continue button is not visibale for click {0}".format(repr(e))

	time.sleep(3)
	if browser.find_elements_by_css_selector('#classic'):
		print "somehow we are still in search page, return now"
		return

	modifyID = 'modify_search_button'
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, modifyID)))


	# if checkIfValidation(browser):
	# 	print "we got validation problem, waiting for human"
	# 	ts = time.time()
	# 	sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
	# 	finalMassege = "we got validation problem {0}".format(sttime)
	# 	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
	# 	os.system(cmd) 
	# 	raw_input("Press Enter to continue looping search...")



def checkIfValidation(browser, text):
	src = browser.page_source
	text_found = re.search(r'LOG IN AND SEARCH FLIGHTS', src)
	if text_found:
		print text_found
		return True
	return False

def navigateDatePicker(browser, departDate):
	print "departDate {0}".format(departDate)
	month = departDate.split("/")[0]
	monthString = monthConvert(month)
	locatorString = monthString + " " + departDate.split("/")[-1]
	locatorString = locatorString.lower()
	date = departDate.split("/")[1]
	departDateID = "datepicker-input-departureDate"
	inputElement = browser.find_element_by_id(departDateID)
	inputElement.click()
	pickerXpath ='//div[@class="date-picker__calendar-container"]'

	#result calendar
	for x in xrange(0,10):
		classAttri = "date-picker__arrow-left"
		prevMonthXpath = '//div[contains(@class, "{0}")]'.format(classAttri)
		results = browser.find_elements_by_xpath(prevMonthXpath)
		try:
			results[0].click()
		except Exception, e:
			print "we cannot go back in calendar anymore, continue"
		time.sleep(1)
		
	time.sleep(3)
	for x in xrange(0,10):
		results = browser.find_elements_by_xpath(pickerXpath);
		pickerText = results[0].text
		pickerText = pickerText.lower()
		foundCal = False
		if locatorString in pickerText:
			print "we found our month calendar, pick date now"
			calendarXpath = '//div[@class="date-picker__calendar"]'
			results = browser.find_elements_by_xpath(calendarXpath)
			for cal in results:
				if locatorString in cal.text.lower():
					print "looking inside the single calendar now"
					tds = cal.find_elements_by_tag_name('td')
					for td in tds:
						dateN = int(date)
						tdDN = -1
						try:
							tdDN = int(td.text)
						except Exception, e:
							continue
						if dateN == tdDN:
							print "we found our date"
							td.click()
							foundCal = True
							break
					break
		time.sleep(2)
		if not foundCal:
			classAttri = "date-picker__arrow-right"
			nextMonthXpath = '//div[contains(@class, "{0}")]'.format(classAttri)
			results = browser.find_elements_by_xpath(nextMonthXpath)
			results[0].click()
		else:
			break

def insert_space(string, integer):
	return string[0:integer] + ' ' + string[integer:]

def parseHTML(html, departDate):
	with open('testHTML1', 'r') as myfile:
		data = myfile.read()
		if html:
			data = html
		soup = BeautifulSoup(data, "html.parser")
		tbodys = soup.find_all('tbody')
		results = []
		for tbody in tbodys:
			flightResult = {}
			trs = tbody.find_all('tr', id=re.compile("^idLine"))
			if len(trs) > 1:
				#not a direct flight, skip
				continue
			tr = trs[0]
			th = tr.find('th', id=re.compile("^bloc"))
			departureTime = th.find('span', {"class": "time"}).text
			location = th.find('span', {"class": "location"}).text
			flightNumber = tr.find('th', {"class": "flight-number"}).text

			div = soup.find('div', {"class": "date"})
			departDate = div.find('p').text
			print departDate
			if tr.find('td', id=re.compile("_BU")):
				status = tr.find('td', id=re.compile("_BU")).text
				if 'No Seats' not in status:
					flightResult['status'] = "Business available"
					flightResult['flight'] = flightNumber
					flightResult['location'] = location
					flightResult['time'] = departDate + "_" + departureTime
					results.append(flightResult)
				print departureTime
				print location
				print flightNumber
				print status
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
		finalMassege += "From Qanta: " + result['time'] + '#' + result['location'] + "#" + result['flight'] + "#" + result['status'] + "            "
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
	os.system(cmd) 


def checkTicket(browser, departDate):
	resultsID = 'idAvailabilty0'
	allInfoID = 'flightIn'
	if browser.find_elements_by_css_selector('#{0}'.format(resultsID)):
		element = browser.find_element_by_id(allInfoID)
		html = element.get_attribute('outerHTML')
		parseHTML(html, departDate)
	else:
		print "we dont have anything on this page"

def research(browser, departDate, offset):
	date = datetime.datetime.strptime(departDate, "%m/%d/%Y").date()
	newDate = date + datetime.timedelta(days=offset)
	newDateStr = newDate.strftime('%m/%d/%Y')
	modifyID = 'modify_search_button'
	if browser.find_elements_by_css_selector('#{0}'.format(modifyID)):
		inputElement = browser.find_element_by_id(modifyID)
		inputElement.click()
	time.sleep(2)
	searchOurTicket(browser, 'HKG', 'SFO', newDateStr)
	time.sleep(3)
	checkTicket(browser, newDateStr)


def loopForTicket(browser, span, departDate):
	modifyID = 'modify_search_button'
	if browser.find_elements_by_css_selector('#{0}'.format(modifyID)):
		inputElement = browser.find_element_by_id(modifyID)
		inputElement.click()
	searchOurTicket(browser, 'HKG', 'SFO', departDate)
	checkTicket(browser, departDate)
	time.sleep(2)
	
	for x in xrange(1,span + 1):
		research(browser, departDate, x)
		research(browser, departDate, -x)


def monthConvert(month):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	return months[int(month) - 1]

def startSearch(browser, departDate):
	print "We start out search now, and we wont end unitl we close the terminal!!!"
	while True:
		loopForTicket(browser, 2, departDate)
		time.sleep(2)
		print "we now wait for 5 minutes before next search"
		time.sleep(300)


def oneTimeQuery(browser, departDate):
	url = "https://www.qantas.com/us/en.html"
	browser.get(url)
	getToSearchPage(browser)
	modifyID = 'modify_search_button'
	if browser.find_elements_by_css_selector('#{0}'.format(modifyID)):
		inputElement = browser.find_element_by_id(modifyID)
		inputElement.click()
	searchOurTicket(browser, 'HKG', 'SFO', departDate)
	checkTicket(browser, departDate)
	time.sleep(2)


def signIn(browser):
	url = "https://www.qantas.com/us/en.html"
	browser.get(url)
	browser.execute_script("window.focus();");
	time.sleep(5)
	getToSearchPage(browser)
	modifyID = 'modify_search_button'
	if browser.find_elements_by_css_selector('#{0}'.format(modifyID)):
		inputElement = browser.find_element_by_id(modifyID)
		inputElement.click()


def start(interestedDates):
	global ourBrowser
	browser = None
	browser = webdriver.Chrome()
	ourBrowser = browser
	shouldSignIn = True
	while True:
		if stopLoop:
			print "we are done"
			browser.close()
			break
		print "\n----------------------------we are trying the infinite search Qanta------------------------------\n"
		try:
			#sign in 
			if shouldSignIn:
				signIn(browser)

			numOfDatesToQuery = len(interestedDates)
			#start isolated search
			for departDate in interestedDates:
				try:
					print "We are now querying {0}".format(departDate)
					url = "https://www.qantas.com/us/en.html"
					browser.get(url)
					browser.execute_script("window.focus();");
					searchOurTicket(browser, 'HKG', 'SFO', departDate)
					checkTicket(browser, departDate)
					print "we have finished querying {0}".format(departDate)
				except Exception as e:
					message = "we have exception with query {0} we continue with next one".format(departDate)
					handleException(browser, e, message)
		except Exception as e:
			handleException(browser, e, "we have unexpected exceptions, close browser and re start")
			time.sleep(15)
			browser.close()
			browser = None
			browser = webdriver.Chrome()
			ourBrowser = browser
			shouldSignIn = True
			continue
		print "\n-----------------------------------We have finised one loop, contine with another----------------------\n"
		print "we now wait for 30s before next search"
		shouldSignIn = False
		time.sleep(30)


def stopExcution():
	print "we stop the loop"
	global stopLoop
	stopLoop = True
	ourBrowser.close()


def handleException(browser, e, message):
	ts = time.time()
	ttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S')
	exceptM = repr(e)
	print "{0} {1}".format(message, exceptM)
	traceback.print_exc()
	finalMassege = "From Qanta: we got new exception while running, re start the process {0} : {1}".format(message, ttime)
	cmd = 'osascript sendMessage.scpt hwenapple@icloud.com "{0}"'.format(finalMassege)
	os.system(cmd) 
	screenshotName = "{0}/qantas_{1}_screenshot.png".format(screenshotDir, ttime)
	browser.save_screenshot(screenshotName)
	browser.execute_script("window.focus();");

if __name__ == '__main__':

	if not os.path.exists(screenshotDir):
		os.makedirs(screenshotDir)
	parser = OptionParser(usage="python queryQantas.py --departDate departDate --interestedDates interestedDates")
	parser.add_option("--departDate", dest="departDate", help="departDate")
	parser.add_option("--interestedDates", dest="interestedDates", help="interestedDates")
	(options, args) = parser.parse_args()
	if options.departDate:
		print "we only query one time"
		browser = webdriver.Chrome()
		try:
			oneTimeQuery(browser, options.departDate)
			time.sleep(5)
			browser.close()
		except Exception as e:
			print "we have exception while running this, close brower {0}".format(exceptM)
			browser.close()
	elif options.interestedDates:
		t = Timer(3600.0, stopExcution)
		t.start()
		interestedDates = options.interestedDates.split(',')
		start(interestedDates)
		# while True:
		# 	ts = time.time()
		# 	sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
		# 	print "we are trying the infinite search"
		# 	browser = webdriver.Chrome()
		# 	try:
		# 		url = "https://www.qantas.com/us/en/book-a-trip/flights.html"
		# 		browser.get(url)
		# 		departDate = '05/26/2018'
		# 		getToSearchPage(browser)
		# 		# raw_input("Press Enter to start the looping search...")
		# 		startSearch(browser, departDate)
		# 	except Exception as e:
		# 		exceptM = repr(e)
		# 		print "we have exception while running this, close brower and re try {0}".format(exceptM)
		# 		finalMassege = "we got exception while running, re start the process {0}".format(sttime)
		# 		cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
		# 		os.system(cmd) 
		# 		browser.close()


