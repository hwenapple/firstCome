import requests
import json
import calendar
import traceback
import os
from selenium import webdriver
from browsermobproxy import Server
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
import re
import io
from subprocess import DEVNULL, STDOUT, check_call
import sys
from subprocess import Popen, PIPE

flightQuerys = []

b1 = {"Type": "Business", "flightNumber": "NH"}

f1 = {"Type": "First", "flightNumber": "NH"}



def checkIfAtSignInPage(browser):
    signInXPath = "//*[contains(text(), 'Bienvenido')]"
    if browser.find_elements_by_xpath(signInXPath):
        print("we are at sign in page")
        time.sleep(2)
    else:
        print("we are not at signed in page")
        browser.refresh()
        time.sleep(5)


def checkForAlerts(brwoser):
    path = '//*[@id="cookies"]/div/a'
    if brwoser.find_element_by_xpath(path).is_displayed():
        brwoser.find_element_by_xpath(path).click()


# https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/select-itinerary.aspx
# https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/login.aspx
def signIn(browser):
    url1 = "https://www.lifemiles.com/sign-in"
    browser.get(url1)
    browser.execute_script("window.focus();")
    time.sleep(2)
    #checkForAlerts(browser)
    browser.refresh()
    time.sleep(5)
   #checkForAlerts(browser)
    checkIfAtSignInPage(browser)
    browser.execute_script("window.focus();")


    rememberMeID = "softLogin"
    resultElement = browser.find_element_by_id(rememberMeID)
    browser.execute_script("arguments[0].click()", resultElement)
    time.sleep(2)

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
    # keepLoginID = "softLogin"
    # # browser.execute_script("document.getElementsByName('remember_me').setAttribute('value', 'true');")

    # resultElement = browser.find_element_by_id(keepLoginID)
    # resultElement.click()
    # time.sleep(2)


    loginID = "Login-confirm"
    resultElement = browser.find_element_by_id(loginID)
    browser.execute_script("arguments[0].click()", resultElement)

    # while True:
    #     try:
    #         browser.execute_script("return of_login()")
    #         break
    #     except Exception as e:
    #         print("we have error login button, we repeat", e)
    #         loginInXPath = "//*[contains(text(), 'LOGIN')]"
    #         # if browser.find_element_by_xpath(loginInXPath).is_displayed:
    #         browser.find_element_by_xpath(loginInXPath).click()
    #         time.sleep(2)

    # print(browser.execute_script("return myFunction2()"))
    time.sleep(10)

#click all buttons class contains "AirRedemptionCalendarMonth_day"
def fakeSearch(browser):
    url = "https://www.lifemiles.com/fly/find"
    browser.get(url)
    time.sleep(5)
    print("we stared fake search")
    # oneWayID = "MainContent_rb_OneWay"
    # browser.find_element_by_id(oneWayID).click()
    oneWayClass = "Booker_nonMobileTripTypeButton__2zLie"
    oneWayButtons = browser.find_elements_by_class_name(oneWayClass)
    for b in oneWayButtons:
        print(b.text, "oneWayButtons")
        if "Ida" in b.text:
            browser.execute_script("arguments[0].click()", b)
            break
    time.sleep(2)

    depCityID = "ar_bkr_fromairport"
    resultElement = browser.find_element_by_id(depCityID)
    resultElement.send_keys('NRT')
    time.sleep(2)
    fullCity = browser.find_element_by_css_selector("button[class^='AirportsDropdown_airportsDropdownButton']")
    browser.execute_script("arguments[0].click()", fullCity)
    time.sleep(2)


    arrCityID = "ar_bkr_toairport"
    resultElement = browser.find_element_by_id(arrCityID)
    resultElement.send_keys('SFO')
    time.sleep(2)
    fullCity = browser.find_element_by_css_selector("button[class^='AirportsDropdown_airportsDropdownButton']")
    browser.execute_script("arguments[0].click()", fullCity)
    time.sleep(2)


    searchButton = browser.find_element_by_css_selector("button[class^='Booker_bookerActionButtonLarge']")
    browser.execute_script("arguments[0].click()", searchButton)
    time.sleep(7)

    dayButtons = browser.find_elements_by_css_selector("button[class^='AirRedemptionCalendarMonth_day']")
    count = 0
    for day in dayButtons:
        className = day.get_attribute("class")
        if "pastDay" not in className:
            if count == 4:
                browser.execute_script("arguments[0].click()", day)
                break
            count += 1

    startCharlesSession()
    time.sleep(15)
    stopAndSaveSession()



def startCharlesSession():
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/recording/start"
    executeCMD(cmd)
    print("charles recording started")


def stopAndSaveSession():
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/recording/stop"
    executeCMD(cmd)
    print("charles recording stopped")
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/session/export-json -o latestLifeMilesAuth.json"
    executeCMD(cmd)
    print("har session recorded")
    time.sleep(2)
    cmd = "killall Charles"
    executeCMD(cmd)
    print("Charles app killed")
    time.sleep(5)


def classMatch(className):
    matching = {"First": "O", "Business": "I", "Economy": "X"}
    return matching[className]


def getQueryData(Origin, Destination, DepartDate):
    headers = {
        'Host': 'www.lifemiles.com',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIzMzAxMjIxOTYwMSIsInVzZXJfbmFtZSI6IjMzMDEyMjE5NjAxIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3OTQ5NTc1MTI5NSwiaWF0IjoxNTc5NDk1NzUxMjk1LCJ0aWQiOiJGRkEzNzkyQzZGQTE3QUI4MDFGNDJERjk0RjBFRjY5RCIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.KYh1JxWbXMLv-8JZAQ2aM5UJ7nJ4Sp9XJAaOmif63cQ',
        'Origin': 'https://www.lifemiles.com',
        'x-dtpc': '1$278418656_596h41vLJGJJFBFJLIIPCCGVNJWGKJVEJGLEAAF',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.lifemiles.com/air-redemption',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    with open('latestLifeMilesAuth.json') as json_file:
        data = json.load(json_file)
    for sessionItem in data:
        if 'exception' in sessionItem.keys():
            continue
        #print(sessionItem['path'])
        if sessionItem['path'] and 'air-redemption-flight' in sessionItem['path']:
            if sessionItem['response']['status'] == 200:
                headersObj = sessionItem['request']['header']['headers']
                for headerObj in headersObj:
                    #print(headerObj['name'])
                    if headerObj['name'] == 'Authorization':
                        #print(headerObj['value'])
                        headers['Authorization'] = headerObj['value']
                        break

    cookies = {}


    # data = '{"internationalization":{"language":"en","country":"jp","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"NRT","dest":"SFO","departingCity":"Tokyo","arrivalCity":"San Francisco","depDate":"2020-12-31","depTime":""},"filter":false,"codPromo":null,"idCoti":"1433100767","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"dTuGOG42eU0qzdNjjcAipoCWVHURLMc6"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"NRT","dest":"SFO","cabin":2}]}'
    #data = '{"internationalization":{"language":"en","country":"usa","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"{0}","dest":"{1}","depDate":"{2}","depTime":""},"filter":false,"codPromo":null,"idCoti":"1433100767","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"dTuGOG42eU0qzdNjjcAipoCWVHURLMc6"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US"}'.format(Origin, Destination, DepartDate)
    data = '{"internationalization":{"language":"en","country":"usa","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"NRT","dest":"SFO","depDate":"2020-12-31","depTime":""},"filter":false,"codPromo":null,"idCoti":"1433100767","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"dTuGOG42eU0qzdNjjcAipoCWVHURLMc6"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US"}'
    
    jsonData = json.loads(data)
    jsonData["od"]['orig'] = Origin
    jsonData["od"]['dest'] = Destination
    jsonData["od"]['depDate'] = DepartDate
    data = json.dumps(jsonData)

    response = requests.post('https://www.lifemiles.com/lifemiles/air-redemption-flight', headers=headers, cookies=cookies, data=data)

    print("flight query status", response.status_code)
    if response.status_code != 200:
        print("we did not get 200 status back from query")
        raise
   

    
    searchResult = response.content
    searchResult = searchResult.decode("utf-8") 
    # with open("lifeMilesResult.json", "w") as my_file:
    #     #json.dump(searchResult, my_file)
    #     my_file.write(searchResult)
    # return searchResultHTML
    #print("flight query result", searchResult)
    searchResult = json.loads(searchResult)
    return searchResult


def startCharles():
    cmd = "open -a Charles"
    executeCMD(cmd)
    print("we launched Charles")
    time.sleep(10)
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/recording/stop"
    executeCMD(cmd)
    print("charles recording stopped")
    time.sleep(2)
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/session/clear"
    executeCMD(cmd)
    print("charles recording session cleared")


def executeCMD(cmd):
    check_call(cmd, stdout=DEVNULL, stderr=STDOUT, shell=True)


def reloadHeaderAndCookie(browser):
    checkIFCharlesIsRunning()

    startCharles()

    signIn(browser)
    fakeSearch(browser)
    browser.quit()


def parseHarObjects(original):
    newObj = {}
    for item in original:
        newObj[item['name']] = item['value']
    return newObj

#{'flightNumber': 'NH8', 'Origin': 'NRT', 'Destination': 'SFO', 'DepartTime': '2020-11-10,17:00', 'tickets': [{'Type': 'First class', 'numberOfSeats': 2, 'flightNumber': 'NH8'}]}
def analyzeQueryData(data):
    tripIndex = 0
    flightCandidates = []
    nonStops = 0
    for tripIndex, trip in enumerate(data['tripsList']):
        if trip['numberOfStops'] > 0:
            continue
        nonStops += 1
        validFlight = {}
        validFlight['flightNumber'] = trip['flightsDetail'][0]['id']
        validFlight['Origin'] = trip['flightsDetail'][0]['departingCityCode']
        validFlight['Destination'] = trip['flightsDetail'][0]['arrivalCityCode']
        validFlight['DepartTime'] = trip['flightsDetail'][0]['departingDate'] + "," + trip['flightsDetail'][0]['departingTime']
        validFlight['tickets'] = []
        for product in trip['products']:
            if not product['soldOut']:
                ticket = {}
                ticket['Type'] = product['cabinName']
                ticket['numberOfSeats'] = product['flights'][0]['remainingSeats']
                ticket['flightNumber'] = validFlight['flightNumber']
                validFlight['tickets'].append(ticket)

        flightCandidates.append(validFlight)
    print("we have got possible number of flights", nonStops)
    #printFlights(flightCandidates)
    return flightCandidates


def printFlights(flights):
    for flight in flights:
        print(flight)
        print("\n")


def ticketMatchPredicates(ticket, predicates):
    for predicate in predicates:
        predicateCheck = True
        for key, value in predicate.items():
            strValue = str(value)
            if key not in ticket or strValue not in str(ticket[key]):
                # print("strValue", strValue)
                # print("ticket[key]", ticket[key])
                predicateCheck = False
                break
        if predicateCheck:
            return True
    return False


def checkForTextAlerts(flights, query):
    for flight in flights:
        textM = flight['flightNumber'] + " " + flight['Origin'] + "-" + flight['Destination'] + " " + flight[
            'DepartTime'] + " "
        for ticket in flight['tickets']:
            if ticketMatchPredicates(ticket, query['Predicates']):
                textM += ticket['Type'] + " " + str(ticket['numberOfSeats']) + " available |"
        if 'available' in textM:
            print("finalTextMessage", textM)
            textMessage(textM)


def textMessage(message):
    cmd = 'osascript sendMessage.scpt 4129808827 "LifeMiles Search Result: {0}"'.format(message)
    os.system(cmd)
    time.sleep(5)


def getCloseANADate():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)
    dt_string = end_date.strftime("%Y%m%d")
    # print("getFurtherANADate", dt_string)
    return dt_string


def plusDay(originalDay, addDay):
    start_date = datetime.strptime(originalDay, "%Y%m%d")
    end_date = start_date + timedelta(days=addDay)
    dt_string = end_date.strftime("%Y%m%d")
    return dt_string


def setFlightQuery():
    global flightQuerys
    # for predicate in predicates array, as long as we have a match, we alert the result
    ANACloseDay = getCloseANADate()
    ANACloseDay1 = plusDay(ANACloseDay, 1)
    ANACloseDay2 = plusDay(ANACloseDay, 2)
    ANACloseDay3 = plusDay(ANACloseDay, 3)
    # flightQuerys.append(
    #     {"Origin": "SIN", "Destination": "TPE", "DepartDate": "20191217", "Class": "Business", "Predicates": [p2]})

    # Check when ANA will release award ticket

    flightQuerys.append({"Origin": "NRT", "Destination": "SFO", "DepartDate": "2021-01-10", "Predicates": [b1, f1]})
    flightQuerys.append({"Origin": "NRT", "Destination": "SFO", "DepartDate": "2021-01-11", "Predicates": [b1, f1]})


def checkIFCharlesIsRunning():
    while True:
        if checkingCharles():
            time.sleep(30)
        else:
            break


def checkingCharles():
    cmd = "pgrep Charles"
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    output, err = p.communicate()
    if len(output) > 3:
        print("Charles is running, we wait till it close")
        return True
    else:
        print("Charles is closed, we proceed")
        return False



def executeQuery(flightQuery):
    print("flightQuery", flightQuery)
    data = {}
    try:
        checkIFCharlesIsRunning()
        data = getQueryData(flightQuery['Origin'], flightQuery['Destination'], flightQuery['DepartDate'])
    except Exception as e:
        print("We have error query the flight result", e)
        traceback.print_exc()
        print("we now try reload the cookie and header via selenium")
        try:
            browser = webdriver.Chrome()
            reloadHeaderAndCookie(browser)
            print("we have reloaded cookie and header")
        except Exception as e:
            print("we have error reload cookie", e)
            browser.quit()
        return False
    if 'status' in data:
        if data['status'] == 'success':
            flightCandidates = analyzeQueryData(data)
            checkForTextAlerts(flightCandidates, flightQuery)
            return True
        else:
            print("flight query result is not expected ", data)
            return False
    print("query result dont have valid status")
    return False


def start():
    setFlightQuery()
    while True:
        for index in range(0, len(flightQuerys)):
            flightQuery = flightQuerys[index]
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================United Query Started {}============================================".format(
                dt_string))
            data = {}
            # with open('unitedResult.json') as json_file:
            #     data = json.load(json_file)
            # we keep trying the current query until we have a valid result
            while True:
                status = executeQuery(flightQuery)
                if status:
                    break
                time.sleep(5)
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================Query Ended {}============================================".format(
                dt_string))
            print("sleep 30 seconds between flight query")
            time.sleep(30)
        print("*******************************************We finished one loop on query sleep for 10s ********************************\n\n\n\n")
        time.sleep(10)


def parseHar():
    with open('latestLifeMilesAuth.json') as json_file:
        data = json.load(json_file)
    for sessionItem in data:
        if 'exception' in sessionItem.keys():
            continue
        #print(sessionItem['path'])
        if sessionItem['path'] and 'air-redemption-flight' in sessionItem['path']:
            if sessionItem['response']['status'] == 200:
                headersObj = sessionItem['request']['header']['headers']
                for headerObj in headersObj:
                    #print(headerObj['name'])
                    if headerObj['name'] == 'Authorization':
                        print(headerObj['value'])
                        break


if __name__ == '__main__':
    start()
    
    # # getQueryData("NRT", "SFO", "2020-04-01")
    # with open('lifeMilesResult_1.json') as json_file:
    #     data = json.load(json_file)
    # analyzeQueryData(data)
    # browser = webdriver.Chrome()
    # signIn(browser)
