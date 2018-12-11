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
from getVPNURL import *
previousCheckTime = None

devTest = False
interestedDates = ['12/21/2018', '12/22/2018', '12/23/2018']

interestedDates = ['01/05/2019', '01/07/2019', '01/14/2019', '01/15/2019', '01/20/2019', '01/21/2019']
#interestedDates = ['04/16/2019']
#interestedDates = ['08/09/2018']
interestedDates = ['12/17/2018', '12/18/2018', '12/19/2018', '12/20/2018']
landingSearchDate = '05/19/2018'
landingSpan = 1

currentTotalExceptions = 0
#first one is my actual account, becareful not to use it
realAccount = ['1672475232']
accounts = ['1679989024','1675359815', '1675587382', '1675587444', ]
accountIndex = 0

home = expanduser("~")
screenshotDir = "{0}/Desktop/screenshots".format(home)

useChrome = True

url = "https://www.asiamiles.com/en/redeem-awards/flight-awards/facade.html"

shouldSignIn = True
browser = None

interationStart = None


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

	userName = accounts[accountIndex]
	memberID = 'memID'
	result = browser.find_element_by_id(memberID);
	result.send_keys(userName);
	time.sleep(1)

	pin = "Hw19891228!"
	pinID = 'memPIN'
	result = browser.find_element_by_id(pinID);
	result.send_keys(pin);
	time.sleep(2)
	loginXpath= '//*[contains(@type, "submit")]'
	buttons = browser.find_elements_by_xpath(loginXpath)
	print "we have entered sigin details"
	for btn in buttons:
		if 'Log in' in btn.text:
			try:
				btn.click()
			except Exception as e:
				continue
			time.sleep(2)
	time.sleep(2)
	print "we check again to make sure we are signed in"
	if checkIfValidation(browser):
		print "we got validation problem, waiting for human"
		ts = time.time()
		sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
		finalMassege = "we got validation problem {0}".format(sttime)
		textMessage(finalMassege)
		raw_input("Press Enter to continue...")
	checkIfNeedSignIn(browser)


def textMessage(message):
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(message)
	os.system(cmd)
	time.sleep(5)
	cmd = 'osascript sendMessage.scpt 4159944384 "{0}"'.format(message)
	os.system(cmd) 


def searchOurTicket(browser, ori, dest, departDate):
	time.sleep(5)
	if browser.find_elements_by_css_selector('#buttons'):
		startNewSearch(browser)
		print "Somehow we are still in search results page, we re search it"
		time.sleep(10)

	onewayID = 'tab-itinerary-type-oneway'
	try:
		browser.find_element_by_id(onewayID).click()
		time.sleep(1)
	except Exception, e:
		print "was not able to click one way button, try sign in then javascript"
		checkIfNeedSignIn(browser)
		browser.execute_script("document.querySelector('#{0}').click()".format(onewayID))
	time.sleep(1)


	oriID ='input-origin'
	try:
		WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, oriID)))
	except Exception, e:
		print "searchOurTicket exception {0}".format(repr(e))
		traceback.print_exc()
		browser.get(url)
		browser.execute_script("window.focus();");
		time.sleep(5)
	inputElement = browser.find_element_by_id(oriID)
	for x in xrange(1,40):
		inputElement.send_keys(Keys.BACK_SPACE);
	inputElement.send_keys(ori)

	time.sleep(1)
	resultID = "results-origin"
	time.sleep(1)
	browser.find_element_by_id(resultID).click()
	time.sleep(1)

	destID = "input-destination"
	try:
		WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.ID, destID)))
	except Exception, e:
		print "searchOurTicket exception {0}".format(repr(e))
		traceback.print_exc()
		startNewSearch(browser)
		time.sleep(10)
	inputElement = browser.find_element_by_id(destID)
	for x in xrange(1,40):
		inputElement.send_keys(Keys.BACK_SPACE);
	inputElement.send_keys(dest)


	time.sleep(1)
	resultID = "results-destination"
	time.sleep(1)
	browser.find_element_by_id(resultID).click()
	time.sleep(3)

	# oneWayXpath = '//*[@id="byDest-trip-type"]/option[text()="One Way"]'
	# xpathScript = "document.getElementByXPath('{0}').click()".format(oneWayXpath);
	# browser.execute_script(xpathScript)




	selectID = "select-cabinSelectBoxItText"
	browser.find_element_by_id(selectID).click()
	time.sleep(1)
	buttons = browser.find_elements_by_xpath("//*[contains(text(), 'Business')]")
	buttons[0].click()
	time.sleep(1)
	# path = '#select-cabin [value="C"]'
	# query = "document.querySelector('{0}').selected = true".format(path);
	# browser.execute_script("{0}".format(query))

	#inputElement = browser.find_element_by_xpath('//*[@id="byDest-trip-type"]/option[text()="One Way"]')


	fixedDateID = 'flexible-dates'
	inputElement = browser.find_element_by_id(fixedDateID)	
	if inputElement.is_selected():
		print "we uncheck the flexible dates option"
		checkBoxXpath = '//*[contains(@class, "label-flexible-dates")]'
		checkBoxes = browser.find_elements_by_xpath(checkBoxXpath)
		for cBox in checkBoxes:
			cBox.click()
			time.sleep(2)
	else:
		print "we do nothing as flexile dates is not checked"
	time.sleep(1)

	navigateDatePicker(browser, departDate)
	time.sleep(2)


	searchButtonText = "Search flights"
	buttons = browser.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(searchButtonText))
	for btn in buttons:
		if 'Search flights' in btn.text:
			try:
				btn.click()
			except Exception as e:
				print "was not able to click this button {}".format(btn.text)
		

	time.sleep(1)

	# try:
	# 	inputElement = browser.find_element_by_id(searchID)
	# 	inputElement.click()
	# except Exception, e:
	# 	print "was not able to click search button, try javascript"
	# 	browser.execute_script("document.querySelector('#{0}').click()".format(searchID))
	# time.sleep(5)

	#IBE_BUS0005_S004
	passedDatesXpath = "//*[contains(text(), 'IBE_BUS0005_S004')]"

	try:
		WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, passedDatesXpath)))
		print "we are searching passed dates, we move on"
		return
	except Exception as e:
		print "we are good with search dates, continue"



	notYetXpath = "//*[contains(text(), 'ERR_DDS_9100')]"

	try:
		WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, notYetXpath)))
		print "we are not yet dates, we move on"
		return
	except Exception as e:
		print "we are good with search dates, we now continue"


	newSearchButtonXPath = "//*[contains(text(), 'New search')]"
	WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, newSearchButtonXPath)))

	# time.sleep(3)

	# filterClass = "flights-filter-button"
	# filterXpath = '//*[contains(@class, "{}")]'.format(filterClass)
	# buttons = browser.find_elements_by_xpath(filterXpath)
	# buttons[0].click()
	# time.sleep(1)

	# availableID = 'flights-departure-available-only'
	# avaiableXPath = '//*[contains(@for, "{}")]'.format(availableID)
	# buttons = browser.find_elements_by_xpath(avaiableXPath)
	# print "we show all flights by check and uncheck "
	# buttons[0].click()
	# time.sleep(1)
	# buttons[0].click()

	# time.sleep(3)



def clickXpathElementViaJavascript(browser, xpath):
	elements = browser.find_elements_by_xpath(xpath)
	browser.execute_script("arguments[0].click();", elements[0])


def checkIfValidation(browser):
	src = browser.page_source
	text_found = re.search(r'interruption', src)
	if text_found:
		print text_found
		return True
	return False

def navigateDatePicker(browser, departDate):
	
	month = departDate.split("/")[0]
	monthString = monthConvert(month)
	locatorString = monthString + " " + departDate.split("/")[-1]
	locatorString = locatorString.lower()
	year = departDate.split("/")[2]


	print "departDate {0} locatorString {1}".format(departDate, locatorString)

	date = departDate.split("/")[1]

	time.sleep(1)

	departureButtonText = "Depart"
	buttons = browser.find_elements_by_xpath("//*[contains(text(), '{0}')]".format(departureButtonText))
	for btn in buttons:
		if 'Depart' in btn.text:
			try:
				btn.click()
			except Exception as e:
				print "we cannot click btn {}".format(btn.text)

	time.sleep(1)
	#we reset perf calandar to first 
	for x in xrange(0, 10):
		prevMonthXpath = '//a[contains(@title, "Prev")]'
		results = browser.find_elements_by_xpath(prevMonthXpath)
		if results:
			#results[0].click()
			clickXpathElementViaJavascript(browser, prevMonthXpath)
		else:
			print "we have reached to left most in calendar"
			break
		time.sleep(1)



	pickerID = 'ui-datepicker-div'

	for x in xrange(0,15):
		result = browser.find_element_by_id(pickerID);
		pickerText = result.text
		pickerText = pickerText.lower()
		foundCal = False
		if locatorString in pickerText and year in pickerText:
			print "we found our month calendar, pick date now"
			results = result.find_elements_by_tag_name('div')
			for cal in results:
				if locatorString in cal.text.lower():
					print "looking inside the single calendar now"
					tds = cal.find_elements_by_tag_name('td')
					for td in tds:
						try:
							tdNumberStr = re.sub("[^0-9]", "", td.text.split(',')[0])
							dateN = int(date)
							tdDN = -1
							tdDN = int(tdNumberStr)
							if dateN == tdDN:
								print "we found our date"
								td.click()
								foundCal = True
								break
						except Exception, e:
							#print "we have error converting td number str {}".format(e)
							continue

					break
		time.sleep(2)
		if not foundCal:
			titleAttri = "Next"
			nextMonthXpath = '//a[contains(@title, "{0}")]'.format(titleAttri)
			clickXpathElementViaJavascript(browser, nextMonthXpath)
			#results[0].click()
		else:
			break

def insert_space(string, integer):
	return string[0:integer] + ' ' + string[integer:]


def checkWithOtherSearchs(departDate, weIgnore = False):
	command = "python queryQantas.py --departDate {0}".format(departDate)
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	print process.returncode
	if not weIgnore:
		command = "python queryBA.py --departDate {0}".format(departDate)
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		process.wait()
		print process.returncode
	else:
		print "we dont run BA search as we are aware of this result"


#Need to change the logic here, if results has one flight knonwn, the entire message will not be sent, not what we want
def shouldIgnore(flightResult):

	if '12/12' in flightResult['time'] and '893' in flightResult['flight']:
		print "we know about this one, dont report"
		return True
	if '12/17' in flightResult['time'] and '873' in flightResult['flight']:
		print "we know about this one, dont report"
		return True
	if '12/17' in flightResult['time'] and '879' in flightResult['flight']:
		print "we know about this one, dont report"
		return True
	if '12/17' in flightResult['time'] and '893' in flightResult['flight']:
		print "we know about this one, dont report"
		return True
	# if '892' in flightResult['flight'] and '08/23' in flightResult['time']:
	# 	print "we know about this one, dont report"
	# 	return True
	# if '870' in flightResult['flight'] and '08/21' in flightResult['time']:
	# 	print "we know about this one, dont report"
	# 	return True
	return False

def parseHTML(html, departDate, pageDepartDate):
	with open('testHTML3', 'r') as myfile:
		data = myfile.read()
		data = html
		# if html:
		# 	data = html
		soup = BeautifulSoup(data, "html.parser")
		divs = soup.find_all('div', id=re.compile("^flight-0"))
		results = []
		for div in divs:
			flightResult = {}
			print "\n"
			print div.text
			flightNameID = "data-flight-name"
			flightNumber = div[flightNameID]
			if '_' in flightNumber:
				continue
			if 'waitlist' in div.text.lower() or 'full' in div.text.lower():
				continue
			rowInfo = div.text
			origins = div.find_all("div", class_="flight-origin")
			location = origins[0].text
			departureTimes = div.find_all("span", class_=re.compile("^depart-time"))
			departureTime = departureTimes[0].text

			flightResult['status'] = "Business available"
			flightResult['flight'] = flightNumber
			flightResult['location'] = location
			flightResult['time'] = pageDepartDate + "_" + departureTime
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
		if shouldIgnore(result):
			continue
		finalMassege += "From CX search: " + result['time'] + '#' + result['location'] + "#" + result['flight'] + "#" + result['status'] + " "
	print finalMassege
	if finalMassege == "":
		return
	textMessage(finalMassege)


def checkTicket(browser, departDate):
	resultsID = 'flightlistDept'
	if browser.find_elements_by_css_selector('#{0}'.format(resultsID)):
		element = browser.find_element_by_id(resultsID)
		html = element.get_attribute('outerHTML')
		pageDateClass = "date-card available ng-scope"
		pageDateXpath = '//*[contains(@class, "{}")]'.format(pageDateClass)
		results = browser.find_elements_by_xpath(pageDateXpath)
		pageDepartDate = departDate
		for result in results:
			if 'active' in result.get_attribute("class"):
				pageDepartDate = result.text
				print "we have pageDepartDate {} search departDate {}".format(pageDepartDate, departDate)
				break;
		#pageDepartDateNumber = re.sub("[^0-9]", "", pageDepartDate)
		compressedText = ''.join(element.text.split())
		if 'businessstandard' in compressedText.lower():
			#we trust search departdate
			parseHTML(html, departDate, departDate)
		else:
			print "we dont have standard awards on this date"
	else:
		print "we dont have anything on this page"
	time.sleep(5)

def research(browser, departDate, offset):
	time.sleep(5)
	date = datetime.datetime.strptime(departDate, "%m/%d/%Y").date()
	newDate = date + datetime.timedelta(days=offset)
	newDateStr = newDate.strftime('%m/%d/%Y')


	startNewSearch(browser)


	# newSearchButtonXPath = "//*[contains(text(), 'New Search')]"
	# WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, newSearchButtonXPath)))
	# buttons = browser.find_elements_by_xpath(newSearchButtonXPath)
	# buttons[0].click()
	time.sleep(2)
	searchOurTicket(browser, 'HKG', 'SFO', newDateStr)
	time.sleep(3)
	checkTicket(browser, newDateStr)


def startNewSearch(browser):
	try:
		newSearchButtonXPath = "//*[contains(text(), 'New search')]"
		buttons = browser.find_elements_by_xpath(newSearchButtonXPath)
		buttons[0].click()
	except Exception, e:
		print "we cannot find the new Search button, try java script way"
		try:
			browser.execute_script("theFacade.submitSearch();")
		except Exception, e:
			print "we cannot find new search button vai javascript, try url"
			browser.get(url)
			browser.execute_script("window.focus();");
		
def checkIfNeedSignIn(browser):	
	signInXPath = "//*[contains(text(), 'Sign into your account')]"
	if browser.find_elements_by_xpath(signInXPath):
		print "somehow we need to sign in again"
		signIn(browser)
		print "we are done sign in"
	else:
		print "we are still signed in"


def loopForTicket(browser, span, departDate):
	newSearchButtonXPath = "//*[contains(text(), 'New search')]"
	if browser.find_elements_by_xpath(newSearchButtonXPath):
		print "we still find new search button in loopForTicket"
		startNewSearch(browser)
	else:
		print "we dont have new search button, carry on"
	time.sleep(5)
	searchOurTicket(browser, 'HKG', 'SFO', departDate)
	checkTicket(browser, departDate)
	time.sleep(2)
	
	for x in xrange(1,span + 1):
		research(browser, departDate, x)
		research(browser, departDate, -x)

	if len(interestedDates) > 0:
		print "we perform additional search on interested Dates"
		for dDate in interestedDates:
			print "additional departDate {0}".format(dDate)
			time.sleep(5)
			startNewSearch(browser)
			time.sleep(2)
			searchOurTicket(browser, 'HKG', 'SFO', dDate)
			checkTicket(browser, dDate)
			time.sleep(2)


def monthConvert(month):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	return months[int(month) - 1]


def handleException(browser, e, message):
	global currentTotalExceptions
	currentTotalExceptions = currentTotalExceptions + 1
	ts = time.time()
	ttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S')
	exceptM = repr(e)
	print "{0} {1}".format(message, exceptM)
	traceback.print_exc()
	finalMassege = "From CX: we got new exception while running, re start the process {0} : {1}".format(message, ttime)
	cmd = 'osascript sendMessage.scpt hwenapple@icloud.com "{0}"'.format(finalMassege)
	os.system(cmd) 
	screenshotName = "{0}/{1}_screenshot.png".format(screenshotDir, ttime)
	try:
		browser.save_screenshot(screenshotName)
	except Exception, e:
		finalMassege= "From CX: we have error saving screenshot"
		textMessage(finalMassege)
	browser.execute_script("window.focus();");
	return checkIfWeNeedToSwitchAccount()


def checkIfWeNeedToSwitchAccount():
	global currentTotalExceptions
	global accountIndex
	if currentTotalExceptions >= 14:
		finalMassege = "we are over the limit for current exception count, notify author and sleep for one hour"
		print finalMassege
		textMessage(finalMassege)
		currentTotalExceptions = 0
		time.sleep(3600)
		# accountIndex = accountIndex + 1
		# if accountIndex == len(accounts):
		# 	accountIndex = 0
		return True
	return False

def triggerQanta():
	dates = ",".join(interestedDates)
	cmd = "python queryQantas.py --interestedDates '{0}'".format(dates)
	print cmd
	os.system(cmd)
	print "Finished querying via qanta"

def signIn(browser):
	#signInURL = 'https://www.cathaypacific.com/cx/en_US.html'
	browser.get(url)
	browser.execute_script("window.focus();");
	time.sleep(5)
	getToSearchPage(browser)



def singleSearch(browser, ori, dest, departDate):
	browser.get(url)
	browser.execute_script("window.focus();");
	print "checking {} {} {}".format(ori, dest, departDate)
	searchOurTicket(browser, ori, dest, departDate)	
	checkTicket(browser, departDate)

def start():
	global shouldSignIn, browser, interationStart
	browser = None
	if useChrome:
		browser = webdriver.Chrome('/usr/local/bin/chromedriver')
	else:
		browser = webdriver.Firefox()

	shouldSignIn = True
	while True:
		print "\n----------------------------we are trying the infinite search CX------------------------------\n"
		interationStart = time.time()
		try:
			#sign in 
			if shouldSignIn:
				signIn(browser)

			numOfDatesToQuery = len(interestedDates)
			exceptionCount = 0
			threshHold = numOfDatesToQuery - 1
			shoudRestart = False
			#start isolated search
			triggerQ = False
			for departDate in interestedDates:
				checkIfNeedSignIn(browser)
				try:
					print "We are now querying {0}".format(departDate)
					printCurrentTime()
					if devTest:
						# singleSearch(browser, 'HKG', 'TLV', departDate)
						# singleSearch(browser, 'TLV', 'HKG', departDate)
						singleSearch(browser, 'SFO', 'HKG', departDate)
						singleSearch(browser, 'HKG', 'SFO', departDate)

					else:							
						departDateNumber = re.sub("[^0-9]", "", departDate)
						departDateNumber = int(departDateNumber)
						singleSearch(browser, 'SFO', 'HKG', departDate)
					print "we have finished querying {0}".format(departDate)
					checkIfNeedSignIn(browser)
				except Exception as e:
					message = "we have exception when query {0} we continue with next one".format(departDate)
					triggerQ = handleException(browser, e, message)
					exceptionCount = exceptionCount + 1
					if exceptionCount >= threshHold or triggerQ == True:
						shouldSignIn = True
						shoudRestart = True
						break
			if shoudRestart:
				print "we have too many exceptions in this loop, we restart"
				time.sleep(5)
				browser.get(url)
				browser.close()
				browser = None
				# if triggerQ:
				# 	triggerQanta()
				if useChrome:
					browser = webdriver.Chrome('/usr/local/bin/chromedriver')
				else:
					browser = webdriver.Firefox()
				continue
		except Exception as e:
			triggerQ = handleException(browser, e, "we have unexpected exceptions, we retry url")
			time.sleep(5)
			browser.get(url)
			# browser.close()
			# browser = None
			# if useChrome:
			# 	browser = webdriver.Chrome('/usr/local/bin/chromedriver')
			# else:
			# 	browser = webdriver.Firefox()
			shouldSignIn = True
			continue
		print "\n-----------------------------------We have finised one loop, contine with another----------------------\n"
		print "we now wait for 90s before next search"
		shouldSignIn = False
		getInterestedDates()
		#getTimeDiff()
		time.sleep(90)

def getInterestedDates():
	return
	global interestedDates, devTest
	devTest = True
	newDates = []
	startDate = datetime.datetime.today()
	startDate += datetime.timedelta(days=1)
	for x in xrange(1,150):
		startDate += datetime.timedelta(days=1)
		strDate = startDate.strftime('%m/%d/%Y')
		newDates.append(strDate)
	print newDates
	interestedDates = newDates


def checkForNewURL():
	global url
	url = "https://proxy.hidemyass.com/proxy/en-us/aHR0cHM6Ly93d3cuYXNpYW1pbGVzLmNvbS9lbi9sb2dpbi5odG1sP3JlZGlyZWN0VXJsPWh0dHBzJTNBJTJGJTJGcHJveHkuaGlkZW15YXNzLmNvbSUyRnByb3h5JTJGZW4tdXMlMkZhSFIwY0hNNkx5OTNkM2N1WVhOcFlXMXBiR1Z6TG1OdmJTOWxiaTl5WldSbFpXMHRZWGRoY21SekwyWnNhV2RvZEMxaGQyRnlaSE12Wm1GallXUmxMbWgwYld3"
	# vpnURL = getVPNLink('google.com')
	# print vpnUR

def compensateTime():
	now = time.time()
	difference = now - previousCheckTime
	print "current interation diff {}".format(difference)
	if difference < 300:
		print "its less thn 5 minutes, we wait a bit"
		time.sleep(120)

# def getTimeDiff():
# 	global previousCheckTime, shouldSignIn, browser
# 	if not previousCheckTime:
# 		previousCheckTime = time.time()
# 		return
# 	now = time.time()
# 	difference = now - previousCheckTime
# 	print "current time diff {}".format(difference)
# 	if difference < 300:
# 		print "its less thn 5 minutes, we wait a bit"
# 		time.sleep(120)
# 	if difference > 14400:
# 		print "we have quried for over 4 hour now, we wait half hour and restart browser"
# 		previousCheckTime = now
# 		time.sleep(10)
# 		browser.close()
# 		browser = None
# 		browser = webdriver.Chrome('/usr/local/bin/chromedriver')
		shouldSignIn = True

def printCurrentTime():
	currentTime = time.time()
	strTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(currentTime))
	print "current query time {}".format(strTime)

if __name__ == '__main__':
	printCurrentTime()
	getInterestedDates()
	if not os.path.exists(screenshotDir):
		os.makedirs(screenshotDir)
	while True:
		try:
			start()
		except Exception as e:
			continue


