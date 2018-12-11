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

if __name__ == '__main__':
	parser = OptionParser(usage="python firstComeFirstGet.py --start YES")
	parser.add_option("--start", dest="start", help="YES for start the program immediately")
	(options, args) = parser.parse_args()
	if not options.start:
		waitTillWeAreHalfMinuteAway()
	browser = webdriver.Chrome()
	badURL = "https://dailygetaways.ustravel.org/Home/Offer/B0494"
	goodURL = "https://dailygetaways.ustravel.org/Home/Offer/B0466"

	hyatt75k = "https://dailygetaways.ustravel.org/Home/Offer/B0494"
	hyatt40k = "https://dailygetaways.ustravel.org/Home/Offer/B0493"
	hyatt30k = "https://dailygetaways.ustravel.org/Home/Offer/B0492"
	browser.get("https://dailygetaways.ustravel.org/Home/Offer/B0473")
	#browser.get(hyatt30k)	
	while(True):
		if getPage(browser):
			break
		print "we re try it"
		time.sleep(0.1)
	print "========================================================="
	print "We were able to get into the buy page!!!! please Keep the ternimal open and go through each browser to find the one to enter purchase info"
	print "========================================================="
	time.sleep(500000)




