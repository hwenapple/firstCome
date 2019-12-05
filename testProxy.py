import requests
import json
import calendar
import traceback
import os
from selenium import webdriver
from browsermobproxy import Server
from datetime import datetime, timedelta
import time
from timeout import timeout
import errno
from subprocess import Popen, PIPE
import sys


def test():
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path, {'port': 8090})
    server.start()

    time.sleep(1)
    proxy = server.create_proxy()
    time.sleep(1)
    print("we started proxy")



def test2():
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path, {'port':9999})

    time.sleep(1)
    proxy = server.create_proxy()
    time.sleep(1)
test()

# #
# # from selenium import webdriver
# # profile = webdriver.FirefoxProfile()
# # selenium_proxy = proxy.selenium_proxy()
# # profile.set_proxy(selenium_proxy)
# # driver = webdriver.Firefox(firefox_profile=profile)
# #
# #
# # proxy.new_har("google")
# # driver.get("http://www.google.co.uk")
# # print (proxy.har) # returns a HAR JSON blob
#
# server.stop()