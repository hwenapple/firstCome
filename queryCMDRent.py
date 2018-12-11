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
import random

home = expanduser("~")
screenshotDir = "{0}/Desktop/screenshots".format(home)
errorCount = 0


def sendErrorMessage(errorStr):
	global errorCount
	errorCount = errorCount + 1
	if not errorCount > 30:
		print "we are not over error message threshHold yet, dont report {}".format(errorStr)
		return
	errorStr += " from cmd Rent"
	errorStr = ' '.join(errorStr.split())
	errorStr = re.sub('[^0-9a-zA-Z]+', ' ', errorStr)
	if len(errorStr) > 155:
		errorStr = errorStr[:155]
	if errorCount > 40:
		errorStr = "we are over the error limit for qanta search, we abort the program and wait for update"
	print "sendErrorMessage {}".format(errorStr)
	cmd = 'osascript sendMessage.scpt 4129808827 "{0}"'.format(errorStr)
	os.system(cmd)
	if errorCount > 40:
		sys.exit(1)

def rentUp():

	cookies = {
	    '__gads': 'ID=8fa535f6c368d336:T=1535489418:S=ALNI_MY9VzPOp1miRJJhLGke8AfLHyByMA',
	    'trc_cookie_storage': 'taboola%20global%3Auser-id=4add3874-df3d-4b8e-8d54-0944618028fb-tuct11785a7',
	    'PHPSESSID': 'hqgj832phvs91kcru8fumscs37',
	    'mosvisitor': '1',
	    '__utmc': '125674584',
	    '__utmz': '125674584.1538689187.15.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided)',
	    '_ga': 'GA1.2.579884844.1535489418',
	    '_gid': 'GA1.2.702387644.1538689193',
	    'SFChinaRen_f_visit': '5',
	    '__utma': '125674584.579884844.1535489418.1538689187.1538696124.16',
	    'username': '00722d5013e03931a8395d6de45e050d5dfb',
	    'password': '20446e1b52ae6d6ff07a038ba964',
	    '__utmt': '1',
	    '328058d19e394e305adafb3ef15979fc': '1979fdb25e3b4775d080076e1b6a0e06',
	    '0cc274c7f3661367c0dd64d26835c266': 'e9dadd0f4187bf93b9af31e68819e1bf',
	    'usercookie[username]': '9562harrywenhr',
	    'usercookie[password]': '57d39b9d15b783fa31b7deb888857abd',
	    'SFChinaRen_data': 'a:2:{s:11:"autologinid"',
	    'SFChinaRen_sid': '60846e8f537486f84f7101e177c15a7d',
	    'bidks': '460',
	    'bidkc': '460',
	    'SFChinaRen_t': 'a:6:{i:198590',
	    '__utmb': '125674584.28.10.1538696128',
	    'GED_PLAYLIST_ACTIVITY': 'W3sidSI6IkF4R3QiLCJ0c2wiOjE1Mzg2OTgxNjEsIm52IjoxLCJ1cHQiOjE1Mzg2OTgxNDAsImx0IjoxNTM4Njk4MTYwfSx7InUiOiJ4ZU1zIiwidHNsIjoxNTM4Njk4MTI4LCJudiI6MSwidXB0IjoxNTM4Njk4MTIzLCJsdCI6MTUzODY5ODEyN30seyJ1IjoiNnRiciIsInRzbCI6MTUzODY5ODAzOCwibnYiOjAsInVwdCI6MTUzODY5ODAyNywibHQiOjE1Mzg2OTgwMjd9XQ..',
	}

	headers = {
	    'Host': 'www.chineseinsfbay.com',
	    'cache-control': 'max-age=0',
	    'origin': 'https://www.chineseinsfbay.com',
	    'upgrade-insecure-requests': '1',
	    'content-type': 'application/x-www-form-urlencoded',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	    'accept': 'text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'referer': 'https://www.chineseinsfbay.com/f/page_viewtopic/t_200625.html',
	    'accept-language': 'en-US,en;q=0.9',
	}
	#data = 'quickreply=true&post=true&confirm=true&message=<p>quick support\xA0</p>&t=200625'

	randomNumber = random.randint(1,1000000)
	randomString = "One more time {}".format(randomNumber)
	print "randomString {}".format(randomString)

	data = 'quickreply=true&post=true&confirm=true&message=<p>{}</p>&t=200625'.format(randomString)

	response = requests.post('https://www.chineseinsfbay.com/f/page_pppping/f_5/mode_reply.html', headers=headers, cookies=cookies, data=data)
	print response.status_code
	print response.content
	if response.status_code != 200:
		sendErrorMessage(response.content)

def start():
	print "we started our rent up query now !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	while True:
		print "\n----------------------------we are trying the infinite rent up query ------------------------------\n"
		try:
			rentUp()
		except Exception as e:
			message = "We have exception {}".format(e)
			print message
			sendErrorMessage(message)
			traceback.print_exc()
		print "\n-----------------------------------We have finised one loop, contine with another----------------------\n"
		print "we have finished rent up, sleep for one hour"
		time.sleep(3600)




if __name__ == '__main__':
	start()


