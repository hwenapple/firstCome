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
    'mosvisitor': '1',
    'PHPSESSID': 'e36ca8ue8728jpq6nd306qaabm',
    '__utmc': '125674584',
    '__utmz': '125674584.1548659064.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not provided)',
    '__utmt': '1',
    '__utma': '125674584.902455778.1548659064.1548659064.1548659064.1',
    '__gads': 'ID=b8c33d3131dc2120:T=1548659064:S=ALNI_MYbm3FLUXBHNk3OgzW9BOeij6DV3w',
    'SFChinaRen_f_visit': '3,5',
    'bidkc': '60',
    'trc_cookie_storage': 'taboola%20global%3Auser-id=76873075-8550-44f4-b57d-5d007862884e-tuct310a315',
    '_sctr': '1|1548576000000',
    '_scid': '4b16abc9-4f90-43b0-95a1-36e761fb080f',
    '328058d19e394e305adafb3ef15979fc': '3cb53c2aba70b2d5d4f9457438fa78f0',
    '0cc274c7f3661367c0dd64d26835c266': '7a08fdd08e734f5ac1cd07a3d78a1f25',
    'GED_PLAYLIST_ACTIVITY': 'W3sidSI6IkdOWSsiLCJ0c2wiOjE1NDg2NTk0MDYsIm52IjoxLCJ1cHQiOjE1NDg2NTk0MDIsImx0IjoxNTQ4NjU5NDAyfSx7InUiOiJRUTliIiwidHNsIjoxNTQ4NjU5MzYzLCJudiI6MSwidXB0IjoxNTQ4NjU5MzYwLCJsdCI6MTU0ODY1OTM2MX1d',
    'usercookie[username]': 'harrywenhr1989',
    'usercookie[password]': '051270f8343107eccf3f401a460bec0b',
    'SFChinaRen_data': 'a:2:{s:11:"autologinid"',
    'SFChinaRen_sid': '893f5ff3bbfadcd2a83f201174d5dbce',
    'SFChinaRen_t': 'a:1:{i:215885',
    '__utmb': '125674584.15.10.1548659064',
	}

	headers = {
	    'Host': 'www.chineseinsfbay.com',
	    'cache-control': 'max-age=0',
	    'origin': 'https://www.chineseinsfbay.com',
	    'upgrade-insecure-requests': '1',
	    'content-type': 'application/x-www-form-urlencoded',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	    'accept': 'text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'referer': 'https://www.chineseinsfbay.com/f/page_viewtopic/t_215885.html',
	    'accept-language': 'en-US,en;q=0.9',
	}

	headers1 = {
	    'Host': 'www.chineseinsfbay.com',
	    'cache-control': 'max-age=0',
	    'origin': 'https://www.chineseinsfbay.com',
	    'upgrade-insecure-requests': '1',
	    'content-type': 'application/x-www-form-urlencoded',
	    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
	    'accept': 'text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	    'referer': 'https://www.chineseinsfbay.com/f/page_viewtopic/t_216291.html',
	    'accept-language': 'en-US,en;q=0.9',
	}

	
	randomNumber = random.randint(1,1000000)
	randomString = "One more time {}".format(randomNumber)
	print "randomString {}".format(randomString)

	data = 'quickreply=true&post=true&confirm=true&message=<p>{}</p>&t=215885'.format(randomString)

	data1 = 'quickreply=true&post=true&confirm=true&message=<p>{}</p>&t=216291'.format(randomString)

	response = requests.post('https://www.chineseinsfbay.com/f/page_pppping/f_5/mode_reply.html', headers=headers, cookies=cookies, data=data)
	print response.status_code
	#print response.content
	if response.status_code != 200:
		sendErrorMessage(response.content)

	# print "second thread"
	# response1 = requests.post('https://www.chineseinsfbay.com/f/page_pppping/f_5/mode_reply.html', headers=headers1, cookies=cookies, data=data1)
	# print response1.status_code
	# #print response.content
	# if response1.status_code != 200:
	# 	sendErrorMessage(response1.content)

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
		time.sleep(7200)




if __name__ == '__main__':
	start()


