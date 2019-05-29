import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.select import Select
import time
from optparse import OptionParser
import traceback
import re


checkInURL = "https://www.southwest.com/air/check-in/index.html"

class wait_for_page_load(object):

	def __init__(self, browser):
		self.browser = browser
		
	def __enter__(self):
		self.old_page = self.browser.find_element_by_tag_name('html')
		
	def page_has_loaded(self):
		new_page = self.browser.find_element_by_tag_name('html')
		return new_page.id != self.old_page.id
		
	def __exit__(self, *_):
		wait_for(self.page_has_loaded)



def wait_for(condition_function):
	start_time = time.time() 
	while time.time() < start_time + 10: 
		if condition_function(): 
			return True 
		else: 
			time.sleep(0.005) 
	raise Exception('Timeout waiting for condition_function')

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



def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script('return jQuery.active') == 0)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    except Exception as e:
        pass

def getPage(browser, price, numerOfTicket):

	priceXpath = "//span[contains(text(), '{}')]".format(price)
	results = browser.find_elements_by_xpath(priceXpath)
	# with wait_for_page_load(browser):
	# 	resultE.click()	
	for element in results:
		try:
			print "price element {}".format(element.get_attribute('innerHTML'))
			li = element.find_element_by_xpath('../..')
			liClass = li.get_attribute('class')
			print 'liClass {}'.format(liClass)
			if 'selected' not in liClass:
				element.click()
				wait_for_ajax(browser)
			#time.sleep(300)
		except Exception as e:
			print "cant click price element {}".format(e)


	try:
		selectXPath = "//*[contains(text(), 'Quantity')]"
		selectCSS = "div[class^='Label QuantityInput']"
		outStockCSS = "div[class^='OutOfStock']"
		outofstockStyle = browser.find_element_by_css_selector(outStockCSS).get_attribute('style')
		notAvaibleCSS = "div[class='OutOfStockMessage']"
		index = 0
		while not browser.find_element_by_css_selector(selectCSS).is_displayed():
			# if index >= 5:
			# 	print "we have waited enough, we refresh"
			# 	browser.refresh()
			# 	return False
			print "somehow select quantity not displayed"
			if 'none' in outofstockStyle:
				print "out of stock, we refresh"
				browser.refresh()
				return False
			body = browser.find_element_by_tag_name('body').text.encode('utf-8')
			if 'is currently unavailable' in body:
				print "current item is not available, we refresh"
				browser.refresh()
				return False
			index += 1
		wait_for_ajax(browser)
		browser.find_element_by_xpath("//select[contains(@id, 'qty')]/option[text()='{}']".format(numerOfTicket)).click()
#<input type="submit" value="Add to cart" class="AddCartButton bigBtn" style="display: ;">
		css = "input[value^='Add to cart']"
		browser.find_element_by_css_selector(css).click()
		wait_for_ajax(browser)
		checkoutCSS = "a[href^='https://www.iemshowplace.com/checkout.php']"
		while True:
			try:
				checkoutElement = browser.find_element_by_css_selector(checkoutCSS)
				break;
			except Exception as e:
				print "proceed to checkout not found"
			if 'have enough' in browser.find_element_by_tag_name('body').text.encode('utf-8'):
				print "we dont have enough ticket, we refresh"
				browser.refresh()
				return False
		# cartXPath = "//*[contains(@value, 'Add to cart')]"
		# WebDriverWait(browser, 10).until(AnyEc(EC.presence_of_element_located((By.XPATH, cartXPath)))) 
		# time.sleep(2)
		# results = browser.find_elements_by_xpath(cartXPath)
		# for element in results:
		# 	element.click()
		checkoutURL = "https://www.iemshowplace.com/checkout.php"
		browser.get(checkoutURL)
	except Exception as e:
		print "we did not find the wanted button {0}".format(e)
		traceback.print_exc()
		browser.refresh()
		return False
	print "we got the buy page"
	return True

def waitTillWeAreHalfMinuteAway():
	start_time = "Thu Apr 4 16:24:50 2019"
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


def typeInfo(browser, number, firstName, lastName):
	confirmationID = "confirmationNumber"
	result = browser.find_element_by_id(confirmationID);
	result.send_keys(number);	

	firstNameID = "passengerFirstName"
	result = browser.find_element_by_id(firstNameID);
	result.send_keys(firstName);
	

	lastNameID = "passengerLastName"
	result = browser.find_element_by_id(lastNameID);
	result.send_keys(lastName);

	checkINID = "form-mixin--submit-button"
	result = browser.find_element_by_id(checkINID);
	result.click()


def checkStatus(browser):
	wait_for_ajax(browser)
	element = browser.find_element_by_id('form-mixin--submit-button') #this element is visible
	if element.is_displayed():
		print "still not open for checkin yet retry"
		return True
	return False


def checkSecondStatus(browser):
	buttons = browser.find_elements_by_tag_name("button")
	for button in buttons:
		print "button {}".format(button)
		if button.get_attribute("aria-label"):
			if 'Check' in button.get_attribute("aria-label"):
				print 'thats stage 2 check in button, we proceed'
				button.click()
				break


def endlessCheckIn(browser):
	checkINID = "form-mixin--submit-button"
	while checkStatus(browser):
		time.sleep(0.02)
		print "check in now"
		if not checkStatus(browser):
			print "looks like we passed, we proceed"
			break;
		resultElement = None
		try:
			resultElement = browser.find_element_by_id(checkINID);
		except Exception as e:
			print "check in button is not available now, we proceed"
			break	
		try:
			resultElement.click()
		except Exception as e:
			time.sleep(2)
			checkINCSS = "button[id^='{}']".format(checkINID)
			try:
				checkInElement = browser.find_element_by_css_selector(checkINCSS)
			except Exception as e:
				print "check in button is gone, we proceed"
				break
			browser.execute_script("document.querySelector('#{0}').click()".format(checkINID))
	wait_for_ajax(browser)
	checkSecondStatus(browser)	

if __name__ == '__main__':
	parser = OptionParser(usage="python southwest.py --start YES -l lastName -f firstName -c confirmationNumber")
	parser.add_option("--start", dest="start", help="YES for start the program immediately")
	parser.add_option("-l", dest="lastName", help="lastName")
	parser.add_option("-f", dest="firstName", help="firstName")
	parser.add_option("-c", dest="number", help="confirmationNumber")
	(options, args) = parser.parse_args()
	if not options.start:
		waitTillWeAreHalfMinuteAway()
	browser = webdriver.Chrome()
	browser.get(checkInURL)

	typeInfo(browser, options.number, options.firstName, options.lastName)
	endlessCheckIn(browser)




