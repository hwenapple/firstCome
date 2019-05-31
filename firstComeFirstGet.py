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
import sys
import re

import requests




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

def check_visible_id(browser, idName):
	try:
		result = browser.find_element_by_id(idName)
		print "check_visible_id {}".format(result.value_of_css_property("style"))
		if result.is_displayed():
			return True
	except Exception as e:
		print "we have exception in check visibale element exists {0}".format(e)
		return False
	return False

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
	print "current_url {}".format(browser.current_url)
	if 'CreditCard' in browser.current_url or 'Your Information' in browser.page_source:
		print "we got to payment page"
		return True
	try:
		badElement = "redemption"
		goodXpath = "//p[contains(text(), 'Buy Now')]"
		#we check 
		#WebDriverWait(browser, 10).until(AnyEc(EC.presence_of_element_located((By.ID, badElement)), EC.presence_of_element_located((By.ID, goodElement)))) 
		WebDriverWait(browser, 10).until(AnyEc(EC.presence_of_element_located((By.XPATH, goodXpath)), EC.presence_of_element_located((By.ID, badElement)))) 	
		if check_visible_id(browser, "error-onhold-overlay"):
			print "error-onhold-overlay now, we refresh to re try"
			browser.refresh()
			return False			
		if check_exists_xpath(browser, goodXpath):
			print "we got what we want"
			results = browser.find_elements_by_xpath(goodXpath)
			didWeClickButton = False
			for btn in results:
				parent = btn.find_element_by_xpath('../..')
				html = parent.get_attribute('outerHTML')
				#print "clicking the button {0}".format(html)
				try:
					btn.click()
					didWeClickButton = True
					print "we were able to click the button"
					break
				except Exception as e:
					print "we did not find the button to click, try next one {0}".format(e)
					continue
			if not didWeClickButton:
				print "we did not click buy button, we re try without refresh page"
				return False
			if check_visible_id(browser, "error-onhold-overlay"):
				print "error-onhold-overlay now, we refresh to re try"
				browser.refresh()
				return False
			if 'CreditCard' in browser.current_url or 'Your Information' in browser.page_source:
				print "we got to payment page"
				return True
			print "not able to get payment, we re try"
			browser.refresh()
			return False
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


def waitTillWeAreMinuteAway(start_time):
	b = time.mktime(time.strptime(start_time,"%a %b %d %H:%M:%S %Y"))
	print(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(b)) ) 
	a = float(b)-time.time()
	if a <= 60:
		print "we are past minute away set time, fire immediately"
		return
	a = a - 60
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

def holdClickTillTime(start_time):
	b = time.mktime(time.strptime(start_time,"%a %b %d %H:%M:%S %Y"))
	while True:
		a = float(b)-time.time()
		if a <= 10:
			print "we are on fire time now 10 seconds away, we proceed"
			break

def testSessionID():
	browser = webdriver.Chrome()
	#http://127.0.0.1:54461
	url = browser.command_executor._url
	session_id = browser.session_id
	print "url " + url
	#browser.session_id = "id14sf5oq55jpplvhczchtc2"
	actualURL = "https://dailygetawaysbuynow.ustravel.org/Campaigns/USTVL/USTVL_CreditCardEntry.aspx"
	browser.get(actualURL)

#EcomRedirect('2d81698a-c21e-4546-b632-be5f757a644a', 'B0563');
def testOnclick():
	actualURL = "https://dailygetaways.ustravel.org/Home/Offer/B0563"
	browser = webdriver.Chrome()
	browser.get(actualURL)
	html = browser.page_source
	result = re.search('EcomRedirect(.*)B0563', html)
	resultStr = result.group(1)
	resultStr = ''.join(resultStr.split())
	resultStr = resultStr.replace(',','')
	resultStr = resultStr.replace('(','')
	resultStr = resultStr.replace("'",'')
	print resultStr

	for i in range(10):
		print "wrong product id"
		browser.execute_script("return EcomRedirect('', 'B0563')")
		time.sleep(1)
	time.sleep(3)
	print "corrent product id"
	browser.execute_script("return EcomRedirect('{}', 'B0563')".format(resultStr))
	time.sleep(6)
	print "corrent product id 2"
	browser.execute_script("return EcomRedirect('{}', 'B0563')".format(resultStr))
	time.sleep(1000)


def inPaymentPage(browser):
	print "current_url {}".format(browser.current_url)
	if 'CreditCard' in browser.current_url or 'Your Information' in browser.page_source:
		print "we got to payment page"
		return True
	return False

def newGetPage(url, startTime):
	offerID = url.split('/')[-1]
	print "we get to the item url to get ready {}".format(url)
	browser = webdriver.Chrome()
	browser.get(url)

	holdClickTillTime(startTime)
	print "we start requests to get the product ID"
	productID = getProductID(url)

	print "we start infinete redirect on click"

	while True:
		if inPaymentPage(browser):
			return True
		try:
			browser.execute_script("return EcomRedirect('{0}', '{1}')".format(productID, offerID))
		except Exception as e:
			print "we did not execute the EcomRedirect {0} we continue".format(e)
		

def sanitizeProductID(offerID, content):
	result = re.search('EcomRedirect(.*){}'.format(offerID), content)
	resultStr = result.group(1)
	resultStr = ''.join(resultStr.split())
	resultStr = resultStr.replace(',','')
	resultStr = resultStr.replace('(','')
	resultStr = resultStr.replace("'",'')
	print "we have product id {}".format(resultStr)
	return resultStr

def getProductID(url):
	offerID = url.split('/')[-1]
	productID = ''
	while True:
		try:
			response = requests.get(url)
			if response.status_code == 200:
				#print response.content
				if 'EcomRedirect' in response.content:
					productID = sanitizeProductID(offerID, response.content)
					break
				else:
					print "No EcomRedirect yet, continue"
			else:
				print "bad response, re try {}".format(response.status_code)
		except Exception as e:
			print "we did not find the product id {0} we continue".format(e)
	return productID


if __name__ == '__main__':

	parser = OptionParser(usage="python firstComeFirstGet.py --start YES")
	parser.add_option("--start", dest="start", help="YES for start the program immediately")
	parser.add_option("--urlOption", dest="urlOption", help="urlOption")
	(options, args) = parser.parse_args()

	startTime = "Fri May 31 10:00:00 2019"
	if not options.start:
		waitTillWeAreMinuteAway(startTime)
	urls = ["https://dailygetaways.ustravel.org/Home/Offer/B0582", "https://dailygetaways.ustravel.org/Home/Offer/B0584", "https://dailygetaways.ustravel.org/Home/Offer/B0585", "https://dailygetaways.ustravel.org/Home/Offer/B0586"]
	if options.urlOption:
		index = int(options.urlOption)
		actualURL = urls[index]
	
	testurl = "https://dailygetaways.ustravel.org/Home/Offer/B0589"
	actualURL = testurl
	print "actualURL %s" % actualURL


	newGetPage(actualURL, startTime)

	# browser = webdriver.Chrome()
	# browser.get(actualURL)


	# holdClickTillTime(startTime)
	# #browser.get(hyatt30k)	
	# while(True):
	# 	if getPage(browser):
	# 		break
	# 	print "we re try it"




	print "========================================================="
	print "We were able to get into the buy page!!!! please Keep the ternimal open and go through each browser to find the one to enter purchase info"
	print "========================================================="
	time.sleep(500000)




