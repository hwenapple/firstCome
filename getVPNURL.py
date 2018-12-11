import requests
import os
import subprocess



def getVPNLink(url):
	cmd = "curl -H 'Host: proxy.hidemyass.com' -H 'Cache-Control: max-age=0' -H 'Origin: https://proxy.hidemyass.com' -H 'Upgrade-Insecure-Requests: 1' -H 'Accept: text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://proxy.hidemyass.com/en-us' -H 'Accept-Language: en-US,en;q=0.9' --data 'form[url]={}&form[dataCenter]=random' --compressed 'https://proxy.hidemyass.com/process/en-us'".format(url)
	result = subprocess.check_output(cmd, shell=True)
	print "our {}".format(result)
	sha = result.split("href=")[-1].split('">')[0].split('/')[-1].rstrip()
	print sha
	step2URL = step2(sha)
	step3URL = step3(step2URL)
	finalURL = "https://proxy.hidemyass.com/proxy/en-us/{}".format(step3URL)
	return finalURL

def step2(url):
	cmd = "curl -H 'Host: proxy.hidemyass.com' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'Accept: text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://proxy.hidemyass.com/en-us' -H 'Accept-Language: en-US,en;q=0.9' --compressed 'https://proxy.hidemyass.com/proxy/en-us/{}'".format(url)
	result = subprocess.check_output(cmd, shell=True)
	print "our second {}".format(result)
	sha = result.split("A HREF=")[-1].split('">')[0].split('/')[-1].rstrip()
	print sha
	return sha

def step3(url):
	cmd = "curl -H 'Host: proxy.hidemyass.com' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' -H 'Accept: text/html,application/xhtml xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' -H 'Referer: https://proxy.hidemyass.com/en-us' -H 'Accept-Language: en-US,en;q=0.9' --compressed 'https://proxy.hidemyass.com/proxy/en-us/{}'".format(url)
	result = subprocess.check_output(cmd, shell=True)
	print "our third {}".format(result)
	sha = result.split("A HREF=")[-1].split('">')[0].split('/')[-1].rstrip()
	print sha
	return sha
