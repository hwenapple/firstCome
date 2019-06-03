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


startImmediately = True
usePreDefinedProductID = True






productIDs = {'B0582':'2a05A01f-a6f6-47d4-9916-b0740cf43e8a', 'B0584':'260eA1c1-4646-4548-b9ee-1634c586e1d0', 'B0585':'291bA26d-130c-4f3d-b9db-4fa19fc78897','B0586':'2bf1A334-1d86-4bc3-9da8-ef8b6acda951'}



injected_javascript = ''
with open('/Users/hwen/firstCome/myTest.js', 'r') as f:
	injected_javascript = f.read()
	print injected_javascript


# injected_javascript = (
#     'myFunction2 = function () { return "quite" };'
#     'const callback = arguments[0];'
#     'const handleDocumentLoaded = () => {'
#     '  document.getElementById("description").innerHTML = "abcd";'
#     '  callback();'
#     '};'
#     'if (document.readyState === "loading") {'
#     '  document.addEventListener("DOMContentLoaded", handleDocumentLoaded);'
#     '} else {'
#     '  handleDocumentLoaded();'
#     '}'
# )








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


def inPaymentPage(browser, offerID):
	print "checkIfInPayment {}".format(browser.current_url)
	if 'CreditCard' in browser.current_url or 'Your Information' in browser.page_source or 'Loyalty' in browser.current_url or offerID not in browser.current_url:
		print "we got to payment page"
		return True
	return False

def newGetPage(url, startTime):
	offerID = url.split('/')[-1]
	print "we get to the item url to get ready {}".format(url)
	browser = webdriver.Chrome()
	browser.get(url)

	#browser.execute_async_script(injected_javascript)
	browser.execute_script(injected_javascript)

	time.sleep(3)
	print "make sure we have succefully injected {}".format(browser.execute_script("return myFunction2()"))
	#print "function results2 {}".format(browser.execute_script("return EcomRedirect2('229fB10a-afe6-4ddd-9edd-1f0e6213b9c9','B0555')"))

	if not startImmediately:
		holdClickTillTime(startTime)
	print "we start requests to get the product ID"
	productID = getProductID(url, browser)

	print "we start infinete redirect on click"

	while True:
		if inPaymentPage(browser, offerID):
			return True
		try:
			browser.execute_script("return EcomRedirect2('{0}', '{1}')".format(productID, offerID))
		except Exception as e:
			print "we did not execute the EcomRedirect2 {0} we continue".format(e)
		

def sanitizeProductID(offerID, content):
	result = re.search('EcomRedirect(.*){}'.format(offerID), content)
	resultStr = result.group(1)
	resultStr = ''.join(resultStr.split())
	resultStr = resultStr.replace(',','')
	resultStr = resultStr.replace('(','')
	resultStr = resultStr.replace("'",'')
	print "we have product id {}".format(resultStr)
	return resultStr


def getEcomRedirectStr(content):
	result = re.search('EcomRedirect(.*);', content)
	resultStr = result.group(1)
	resultStr = ''.join(resultStr.split())
	print resultStr
	return resultStr
	

def getProductID(url, browser):
	offerID = url.split('/')[-1]
	productID = ''
	if usePreDefinedProductID:
		productID = browser.find_element_by_id("ExternalLink").get_attribute('value')
		#productID = productIDs[offerID]
		print "we use predifined product ID {}".format(productID)
		return productID
	while True:
		try:
			response = requests.get(url)
			if response.status_code == 200:
				#print response.content
				if 'EcomRedirect' in response.content:
					productID = sanitizeProductID(offerID, response.content)
					#getEcomRedirectStr(response.content)
					print response.content
					break
				else:
					print "No EcomRedirect yet, continue"
			else:
				print "bad response, re try {}".format(response.status_code)
		except Exception as e:
			print "we did not find the product id {0} we continue".format(e)
	return productID

def oldGetPage(browser, actualURL):
	oldGetPage(actualURL, startTime)

	browser = webdriver.Chrome()
	browser.get(actualURL)

	if not startImmediately:
		holdClickTillTime(startTime)
	#browser.get(hyatt30k)	
	while(True):
		if getPage(browser):
			break
		print "we re try it"	

if __name__ == '__main__':

	parser = OptionParser(usage="python firstComeFirstGet.py --start YES")
	parser.add_option("--start", dest="start", help="YES for start the program immediately")
	parser.add_option("--urlOption", dest="urlOption", help="urlOption")
	parser.add_option("--usePDs", dest="usePDs", help="usePDs")
	(options, args) = parser.parse_args()
	startTime = "Mon Jun 03 10:00:00 2019"
	if not options.usePDs:
		usePreDefinedProductID = False
	#Looks like we can always use predefined productID
	usePreDefinedProductID = True
	urls = ["https://dailygetaways.ustravel.org/Home/Offer/B0582", "https://dailygetaways.ustravel.org/Home/Offer/B0584", "https://dailygetaways.ustravel.org/Home/Offer/B0585", "https://dailygetaways.ustravel.org/Home/Offer/B0586"]
	if options.urlOption:
		index = int(options.urlOption)
		actualURL = urls[index]
	else:
		actualURL = urls[0]
	
	# testurl = "https://dailygetaways.ustravel.org/Home/Offer/B0555"
	# actualURL = testurl

	print "actualURL %s" % actualURL

	if not options.start:
		waitTillWeAreMinuteAway(startTime)
		startImmediately = False


	newGetPage(actualURL, startTime)

	#oldGetPage(actualURL, startTime)

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




