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
import sys
import traceback

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


def getPage(browser):
	try:
		badElement = "redemption"
		goodXpath = "//p[contains(text(), 'Buy Now')]"
		#we check 
		#WebDriverWait(browser, 10).until(AnyEc(EC.presence_of_element_located((By.ID, badElement)), EC.presence_of_element_located((By.ID, goodElement)))) 
		WebDriverWait(browser, 10).until(AnyEc(EC.presence_of_element_located((By.XPATH, goodXpath)), EC.presence_of_element_located((By.ID, badElement)))) 	
		if check_exists_id(browser, "error-onhold-overlay"):
			print "error now"
			browser.refresh()
			return False			
		if check_exists_xpath(browser, goodXpath):
			print "we got what we want"
			results = browser.find_elements_by_xpath(goodXpath)
			for btn in results:
				parent = btn.find_element_by_xpath('../..')
				html = parent.get_attribute('outerHTML')
				print "clicking the button {0}".format(html)
				try:
					btn.click()	
				except Exception as e:
					print "we did not find the button to click, try next one {0}".format(e)
					continue
				print "we were able to click the button"
				break
			return True
		if check_exists_id(browser, badElement):
			#we still get the bad element
			print "we still get the badXpath refresh page"
			browser.refresh()
			return False
		print "we didnt find any element"
		return False
	except Exception as e:
		print "we did not find the wanted button {0}".format(e)
		#browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
		browser.refresh()
		return False


def waitTillWeAreHalfMinuteAway():
	start_time = "Tue May 08 09:59:30 2018"
	b = time.mktime(time.strptime(start_time,"%a %b %d %H:%M:%S %Y"))
	print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(b)) ) 
	a = float(b)-time.time()
	if a <= 0:
		print "we are past set time, fire immediately"
		return
	print "we will wait {0} seconds to start".format(a)
	loopCount = int(a / 30)
	remain = int(a % 30)
	for x in xrange(0,loopCount):
		time.sleep(30)
		a = a - 30
		print "we will wait {0} seconds to start".format(a)
	time.sleep(remain)
	b = time.mktime(time.strptime(start_time,"%a %b %d %H:%M:%S %Y"))
	print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(b)) ) 
	print "Its time now lets do this!!!"


def getToSearchPage(browser):
	loginID = "loginid"
	#loginID = "membershipNumber"
	WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, loginID)))
	userName = "harrywenhro@gmail.com"
	inputElement = browser.find_element_by_id(loginID)
	inputElement.clear()
	inputElement.send_keys(userName);
	#remeCheckBoxID = 'remcheck'
	#browser.find_element_by_id(remeCheckBoxID).click()
	password ="Hw19891228!"
	inputElement = browser.find_element_by_id("password")
	inputElement.clear()
	inputElement.send_keys(password);
	time.sleep(2)
	logInPath = "//button[contains(text(), 'Log in')]"
	#logInPath = '//*[@id="navLoginForm"]/div[3]/div/button'
	results = browser.find_elements_by_xpath(logInPath);
	results[0].click()


def searchOurTicket(browser, ori, dest, departDate):
	oneWayID = "oneWay"
	originID = "departurePoint"
	destID = "destinationPoint"

	# inputElement = browser.find_element_by_id(oneWayID)
	# inputElement.click()
	time.sleep(1)
	inputElement = browser.find_element_by_id(originID)
	inputElement.clear()
	inputElement.send_keys(ori);
	time.sleep(1)

	inputElement = browser.find_element_by_id(destID)
	inputElement.clear()
	inputElement.send_keys(dest);
	time.sleep(1)
	navigateDatePicker(browser, departDate)
	time.sleep(2)

	inputElement = browser.find_element_by_id(oneWayID)	
	if not inputElement.is_selected():
		inputElement.send_keys(Keys.SPACE)
	time.sleep(1)

	browser.find_element_by_xpath('//*[@id="cabin"]/option[text()="Business/Club"]').click()
	time.sleep(3)

	
	browser.find_element_by_xpath('//*[@id="submitBtn"]').click()
	time.sleep(5)

	if checkIfValidation(browser):
		print "we got validation problem, waiting for human"
		ts = time.time()
		sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
		finalMassege = "we got validation problem {0}".format(sttime)
		cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
		os.system(cmd) 
		sys.exit()



def checkIfValidation(browser):
	src = browser.page_source
	text_found = re.search(r'Validation', src)
	if text_found:
		return True
	return False

def navigateDatePicker(browser, departDate):
	print "navigateDatePicker {0}".format(departDate)
	month = departDate.split("/")[0]
	monthString = monthConvert(month)
	locatorString = monthString + "20" + departDate.split("/")[-1]
	departDateID = "departInputDate"
	inputElement = browser.find_element_by_id(departDateID)
	inputElement.click()
	pickerXpath ='//*[@id="departInputDate_root"]/div/div/div/div'
	for x in xrange(0,6):
		results = browser.find_elements_by_xpath(pickerXpath);
		pickerText = results[0].text
		if locatorString in pickerText:
			print "we found our month calendar, pick date now"
			dateXpath = '//div[@aria-label="{0}"]'.format(departDate)
			results = browser.find_elements_by_xpath(dateXpath)
			for r in results:
				try:
					r.click()
					break
				except Exception, e:
					continue
			break
		time.sleep(2)
		nextMonthXpath = '//div[@title="Next month"]'
		results = browser.find_elements_by_xpath(nextMonthXpath)
		results[0].click()

def insert_space(string, integer):
	return string[0:integer] + ' ' + string[integer:]

def parseHTML(html):
	with open('testHTML', 'r') as myfile:
		data = myfile.read()
		if html:
			data = html
		soup = BeautifulSoup(data, "html.parser")
		tbody = soup.find('tbody')
		trs = tbody.find_all('tr', class_=re.compile("^direct"))
		results = []
		for tr in trs:
			flightResult = {}
			if "data-carrier" in tr.attrs and tr.attrs['data-carrier'] == 'CX':
				#we are inside CX row
				operatorP = tr.find('p', class_=re.compile("^career"))
				flightNumber = operatorP.text
				departureTime = tr.find('div', class_=re.compile("^flight-detail departure"))
				departureTime = departureTime.text
				departureTime = insert_space(departureTime, 5)
				allDivs = tr.find_all('div', {"class": "travel-class-detail"})
				for div in allDivs:
					allSubDivs = div.find_all('div', class_=re.compile("^flightCabin"))
					for subDiv in allSubDivs:
						if 'Business' in subDiv.text:
							if 'Not' not in subDiv.text:
								flightResult['flight'] = flightNumber.split('-')[-1]
								flightResult['status'] = subDiv.text
								flightResult['time'] = departureTime
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
		finalMassege += "From BA search: " + result['time'] + "#" + result['flight'] + "#" + result['status'] + "            "
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
	os.system(cmd) 

def navigateThroughDays(browser, offset):
	tabListPath = '//*[@id="Outbound"]/ul'
	results = browser.find_elements_by_xpath(tabListPath);
	ulist = results[0]
	lists = ulist.find_elements_by_tag_name("li")
	#we will have 9 list items, 7 days and a prev and next item, current item index is 4
	index = 4 + offset
	lists[index].click()
	time.sleep(5)
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, tabListPath)))
	checkTicket(browser)


def checkTicket(browser):
	flightInfoID = 'flightListOutbound0'
	element = browser.find_element_by_id(flightInfoID)
	html = element.get_attribute('outerHTML')
	parseHTML(html)

def loopForTicket(browser, span):
	checkTicket(browser)
	for x in xrange(0,span):
		navigateThroughDays(browser, -1)

	navigateThroughDays(browser, span)

	for x in xrange(0,span):
		navigateThroughDays(browser, 1)
	navigateThroughDays(browser, -span)


def monthConvert(month):
	months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	return months[int(month) - 1]

def startSearch(browser):
	print "We start out search now, and we wont end unitl we close the terminal!!!"
	while True:
		loopForTicket(browser, 2)
		time.sleep(2)
		redoSearch(browser)
		print "we now wait for 5 minutes before next search"
		time.sleep(300)

def redoSearch(browser):
	startAgainXpath = '//a[@title="Start again"]'
	results = browser.find_elements_by_link_text("Start again")
	results[0].send_keys('\n')
	time.sleep(2)
	searchOurTicket(browser, 'HKG', 'SFO', '05/26/18')
	time.sleep(1)


def oneTimeQuery(browser, departDate):
	url = "https://www.britishairways.com/travel/redeem/execclub/_gf/en_us"
	browser.get(url)
	getToSearchPage(browser)
	searchOurTicket(browser, 'HKG', 'SFO', departDate)
	checkTicket(browser)
	time.sleep(3)

if __name__ == '__main__':
	parser = OptionParser(usage="python queryBA.py --departDate departDate")
	parser.add_option("--departDate", dest="departDate", help="departDate")
	(options, args) = parser.parse_args()
	if options.departDate:
		print "we only query one time"
		browser = webdriver.Chrome()
		try:
			modifiedDate = options.departDate.split('/')[0] + "/" + options.departDate.split('/')[1] + "/" + options.departDate.split('/')[2][2:]
			print modifiedDate
			oneTimeQuery(browser, modifiedDate)
			time.sleep(5)
			browser.close()
		except Exception as e:
			print "BA we have exception while running this, close brower {0}".format(repr(e))
			traceback.print_exc()
			browser.close()
	else:
		while True:
			ts = time.time()
			sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M:%S - ')
			print "we are trying the infinite search"
			browser = webdriver.Chrome()
			try:
				url = "https://www.britishairways.com/travel/redeem/execclub/_gf/en_us"
				#url = "https://www.britishairways.com/en-us/home#/"
				browser.get(url)
				getToSearchPage(browser)
				searchOurTicket(browser, 'HKG', 'SFO', '05/26/18')
				# raw_input("Press Enter to start the looping search...")
				startSearch(browser)
			except Exception as e:
				exceptM = repr(e)
				print "we have exception while running this, close brower and re try {0}".format(exceptM)
				traceback.print_exc()
				finalMassege = "we got exception while running, re start the process {0}".format(sttime)
				cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(finalMassege)
				os.system(cmd) 
				browser.close()


