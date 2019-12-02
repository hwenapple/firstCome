import os
import selenium

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
import json

#from seleniumwire import webdriver
from selenium import webdriver

from Mobilenium.mobilenium import mobidriver
from pprint import pprint
from browsermobproxy import Server


browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
server = Server(browsermob_path)

proxy = server.create_proxy()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
browser = webdriver.Chrome(options=chrome_options)
url2 = "https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1"
url1 = "https://www.united.com/en/us"

options = {'captureHeaders': True, 'captureCookies': True}
proxy.new_har("united", options=options)
browser.get(url1)
time.sleep(5)
server.start()
time.sleep(2)
browser.get(url2)

newH = proxy.har # returns a HAR JSON blob
with open('dataU.json', 'w') as outfile:
    json.dump(newH, outfile)
server.stop()
browser.quit()

#
# url2 = "https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1"
# url1 = "https://www.united.com"
# browser = mobidriver.chrome('/usr/local/bin/chromedriver', browsermob_binary=browsermob_path)
#
# browser.get("https://www.google.com")
# print(browser.headers['Content-Type'])
# browser.quit()

# browser.get(url1)
# time.sleep(5)
# browser.get(url2)



#
# browser.get('https://www.google.com')


# har = json.loads(browser.get_log('har')[0]['message']) # get the log
# print('headers: ', har['log']['entries'][0]['request']['headers'])
# for request in browser.requests:
#     if request.response:
#         print(
#             request.path,
#             request.response.status_code,
#             request.response.headers
#         )
