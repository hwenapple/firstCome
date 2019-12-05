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


def reloadHeaderAndCookie():
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path, {'port':9999})

    time.sleep(1)
    proxy = server.create_proxy()
    time.sleep(1)


reloadHeaderAndCookie()


