import requests
import json
import calendar
import traceback
import os
from selenium import webdriver
from browsermobproxy import Server
from datetime import datetime
import time

httpArchive = {}


def getDefaultQuery():
    data = '{"internationalization":{"language":"en","country":"us","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"SFO","dest":"NRT","departingCity":"San Francisco","arrivalCity":"Tokyo","depDate":"2020-11-11","depTime":""},"filter":false,"codPromo":null,"idCoti":"1371862959","officeId":"","ftNum":"04070320505","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"NH","searchTypePrioritized":"NH","sch":{"schHcfltrc":"dTuGOG42eU31aSGSPp4cKmhzIIpywQri"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"SFO","dest":"NRT","cabin":2}]}'
    jsonData = json.loads(data)
    return jsonData


def checkIfAtSignInPage(browser):
    signInXPath = "//*[contains(text(), 'Mantener')]"
    if browser.find_elements_by_xpath(signInXPath):
        print("we are at sign in page")
    else:
        print("we are not at signed in page")
        browser.refresh()
        time.sleep(5)


def signIn(browser):
    url1 = "https://www.lifemiles.com/sign-in"
    browser.get(url1)
    browser.execute_script("window.focus();")
    time.sleep(5)
    browser.refresh()
    time.sleep(5)
    checkIfAtSignInPage(browser)
    userID = 'username'
    userName = '33012219601'
    result = browser.find_element_by_id(userID);
    result.send_keys(userName);
    time.sleep(1)
    pin = "Hw19891228#"
    pinID = 'password'
    result = browser.find_element_by_id(pinID)
    result.send_keys(pin)
    time.sleep(2)
    keepLoginName = "remember_me"
    # browser.execute_script("document.getElementsByName('remember_me').setAttribute('value', 'true');")

    resultElement = browser.find_element_by_name(keepLoginName)
    browser.execute_script("arguments[0].value = 'true'", resultElement)
    loginID = "Login-confirm"
    # server.start()
    time.sleep(3)
    try:
        loginElement = browser.find_element_by_id(loginID)
        loginElement.click()
    except Exception, e:
        print("was not able to click login button, try javascript")
        browser.execute_script("document.querySelector('#{0}').click()".format(loginID))
    time.sleep(5)


def reloadHeaderAndCookie():
    global httpArchive
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path)

    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    browser = webdriver.Chrome(options=chrome_options)
    options = {'captureHeaders': True, 'captureCookies': True}

    signIn(browser)
    proxy.new_har("lifemiles", options=options)
    url = "https://www.lifemiles.com/fly/find"

    time.sleep(2)
    browser.get(url)
    time.sleep(5)

    originID = "ar_bkr_fromairport"
    browser.find_element_by_id(originID).send_keys("SFO")
    time.sleep(2)
    destinationID = "ar_bkr_toairport"
    browser.find_element_by_id(destinationID).send_keys("SFO")
    time.sleep(2)

    server.start()
    searchClass = "Booker_bookerActionButtonSmall__3Fh2d"
    try:
        browser.find_element_by_class_name(searchClass).click()
    except Exception, e:
        print("was not able to click search button, try javascript")
        browser.execute_script("document.querySelector('.{0}').click()".format(searchClass))

    time.sleep(10)
    newH = proxy.har  # returns a HAR JSON blob
    with open('latestLifeMilesAuth.json', 'w') as outfile:
        json.dump(newH, outfile)
    server.stop()
    browser.quit()
    httpArchive = newH


def parseHarObjects(original):
    newObj = {}
    for item in original:
        newObj[item['name']] = item['value']
    return newObj


def testQuery():
    headers = {}
    cookies = {}
    # with open('latestLifeMilesAuth.json') as json_file:
    #     data = json.load(json_file)
    data = httpArchive
    for entry in data['log']['entries']:
        if 'www.lifemiles.com/air-redemption' in entry['request']['url']:
            headers = entry['request']['headers']
            cookies = entry['request']['cookies']
            headers = parseHarObjects(headers)
            cookies = parseHarObjects(cookies)
            if 'JSESSIONID' in cookies:
                print("headers", headers)
                print("cookies", cookies)
                break
    jsonQuery = getDefaultQuery()
    jsonQuery.pop('idCoti', None)
    jsonQuery.pop('ftNum', None)
    jsonQuery.pop('sch', None)
    data = json.dumps(jsonQuery)
    # data = '{"internationalization":{"language":"en","country":"us","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"SFO","dest":"NRT","departingCity":"San Francisco","arrivalCity":"Tokyo","depDate":"2020-11-11","depTime":""},"filter":false,"codPromo":null,"idCoti":"1371862959","officeId":"","ftNum":"04070320505","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"NH","searchTypePrioritized":"NH","sch":{"schHcfltrc":"dTuGOG42eU31aSGSPp4cKmhzIIpywQri"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"SFO","dest":"NRT","cabin":2}]}'
    response = requests.post('https://www.lifemiles.com/lifemiles/air-redemption-flight', headers=headers,
                             cookies=cookies, data=data)
    print(response.status_code)
    print(response.content)


def start():
    reloadHeaderAndCookie()
    testQuery()


if __name__ == '__main__':
    start()
