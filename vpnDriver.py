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
from selenium.webdriver.chrome.options import Options


options = Options()


user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'

#options = webdriver.ChromeOptions()
# specify headless mode
#options.add_argument('headless')
# specify the desired user agent
options.add_argument('user-agent={0}'.format(user_agent))

options.add_argument('--proxy-server=218.205.72.199:80')
browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', chrome_options=options)

browser.get('https://www.cathaypacific.com/cx/sc_CN/book-a-trip/redeem-flights/facade.html')





