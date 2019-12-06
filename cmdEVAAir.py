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

flightQuerys = []

p1 = {"flightNumber": "NH"}
p2 = {"flightNumber": "SQ"}
injected_javascript = ''
with open('/Users/hwen/firstCome/eva.js', 'r') as f:
    injected_javascript = f.read()


def getDefaultQuery():
    data = 'QueryDate=20201019&QueryDateReturn=&DepartureLocation=SJC&ArrivalLocation=HND&serviceClass=I&CardNo=3336439805&TicketType=1&Name=YIJUN%2FZHANG&CHD=0&FunctionName=staralliance-award-ticket&DepCarrier=STAR'
    jsonData = json.loads(data)
    return jsonData


def checkIfAtSignInPage(browser):
    signInXPath = "//*[contains(text(), 'Forgot Membership Number')]"
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
    url1 = "https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/login.aspx"
    browser.get(url1)
    browser.execute_script("window.focus();")
    time.sleep(2)
    checkForAlerts(browser)
    browser.refresh()
    time.sleep(5)
    checkForAlerts(browser)
    checkIfAtSignInPage(browser)
    browser.execute_script("window.focus();")
    userID = 'txt_Member'
    userName = 'yingjiewen1962@gmail.com'
    result = browser.find_element_by_id(userID);
    result.send_keys(userName);
    time.sleep(1)
    pin = "Hw19891228!"
    pinID = 'txt_Password'
    result = browser.find_element_by_id(pinID)
    result.send_keys(pin)
    time.sleep(2)
    keepLoginID = "Chk_RmbrMbrID"
    # browser.execute_script("document.getElementsByName('remember_me').setAttribute('value', 'true');")

    resultElement = browser.find_element_by_id(keepLoginID)
    resultElement.click()
    time.sleep(2)

    while True:
        try:
            browser.execute_script("return of_login()")
            break
        except Exception as e:
            print("we have error login button, we repeat", e)
            loginInXPath = "//*[contains(text(), 'LOGIN')]"
            # if browser.find_element_by_xpath(loginInXPath).is_displayed:
            browser.find_element_by_xpath(loginInXPath).click()
            time.sleep(2)

    # print(browser.execute_script("return myFunction2()"))
    time.sleep(10)


def fakeSearch(browser):
    # url = "https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/select-itinerary.aspx"
    # browser.get(url)
    # time.sleep(5)
    print("we stared fake search")
    # oneWayID = "MainContent_rb_OneWay"
    # browser.find_element_by_id(oneWayID).click()
    time.sleep(2)

    depCityID = "MainContent_hid_DepCity"
    resultElement = browser.find_element_by_id(depCityID)
    browser.execute_script("arguments[0].value = 'SFO'", resultElement)

    arrCityID = "MainContent_hid_ArrCity"
    resultElement = browser.find_element_by_id(arrCityID)
    browser.execute_script("arguments[0].value = 'NRT'", resultElement)
    time.sleep(2)

    calendarValueID = "MainContent_hid_tbGoYYYYMM"
    resultElement = browser.find_element_by_id(calendarValueID)
    browser.execute_script("arguments[0].value = '2020/10/11'", resultElement)
    time.sleep(2)

    browser.execute_script(injected_javascript)

    browser.execute_script("return fakeSearch()")
    startCharlesSession()
    time.sleep(15)
    stopAndSaveSession()
    # searchID = "MainContent_lit_ok"
    # browser.find_element_by_id(searchID).click()
    # time.sleep(200)


def startCharlesSession():
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/recording/start"
    executeCMD(cmd)
    print("charles recording started")


def stopAndSaveSession():
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/recording/stop"
    executeCMD(cmd)
    print("charles recording stopped")
    cmd = "curl -v -x http://127.0.0.1:8888 http://control.charles/session/export-json -o latestEVAAuth.json"
    executeCMD(cmd)
    print("har session recorded")
    cmd = "killall Charles"
    executeCMD(cmd)
    print("Charles app killed")
    time.sleep(5)


def classMatch(className):
    matching = {"First": "O", "Business": "I", "Economy": "X"}
    return matching[className]


def getQueryData(Origin, Destination, DepartDate, flightClass):
    flightClass = classMatch(flightClass)
    headers = {
        'Host': 'booking.evaair.com',
        'cache-control': 'max-age=0',
        'origin': 'https://booking.evaair.com',
        'upgrade-insecure-requests': '1',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'referer': 'https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/select-itinerary.aspx',
        'accept-language': 'en-US,en;q=0.9',
    }
    cookies = {}
    with open('latestEVAAuth.json') as json_file:
        data = json.load(json_file)
    for sessionItem in data:
        if 'select-first-journey.aspx' in sessionItem['path']:
            headersObj = sessionItem['request']['header']['headers']
            for headerObj in headersObj:
                if headerObj['name'] == 'cookie':
                    cookieName = headerObj['value'].split('=')[0]
                    cookieValue = headerObj['value'].split('=')[1]
                    cookies[cookieName] = cookieValue
            break
    # print("cookies", cookies)
    data = 'QueryDate={2}&QueryDateReturn=&DepartureLocation={0}&ArrivalLocation={1}&serviceClass={' \
           '3}&CardNo=3336649050&TicketType=1&Name=YINGJIE%2FWEN&CHD=0&FunctionName=staralliance-award-ticket' \
           '&DepCarrier=STAR'.format(Origin, Destination, DepartDate, flightClass)
    response = requests.post(
        'https://booking.evaair.com/flyeva/EVA/B2C/plan-your-journey/online-reservation/staralliance-award-ticket/select-first-journey.aspx',
        headers=headers, cookies=cookies, data=data)

    print("flight query status", response.status_code)
    if response.status_code != 200:
        print("we did not get 200 status back from query")
        raise
    # print("flight query result", response.content)
    searchResultHTML = response.content
    with open("validEVA.html", "w") as my_file:
        my_file.write(response.text)
    return searchResultHTML


def startCharles():
    cmd = "open -a Charles"
    executeCMD(cmd)
    print("we launched Charles")
    time.sleep(15)
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
    startCharles()

    signIn(browser)
    fakeSearch(browser)
    browser.quit()


def parseHarObjects(original):
    newObj = {}
    for item in original:
        newObj[item['name']] = item['value']
    return newObj


def analyzeQueryData(queryData, originalQuery):
    # with io.open('validEVA.html', 'r', encoding="utf-8") as myfile:
    #     queryData = myfile.read()
    soup = BeautifulSoup(queryData, "html.parser")
    flightScrollBox = soup.find('div', {"class": "newcard-row"}).parent
    # print("flightScrollBox", str(flightScrollBox))
    flightOptions = flightScrollBox.find_all('div', {"class": "newcard-row"})
    validFlights = []
    nonStops = 0
    for flightOption in flightOptions:
        validFlight = {}
        validFlight['Origin'] = originalQuery['Origin']
        validFlight['Destination'] = originalQuery['Destination']
        validFlight['Class'] = originalQuery['Class']

        flightNumberTable = flightOption.find("div", {"class": "card-end"})
        flightInfoRows = flightNumberTable.find_all("tr")
        flightNumber = flightInfoRows[0].find("td").text.strip()
        stopInfo = int(flightInfoRows[4].find("td").text.strip())
        flightNumber = flightInfoRows[0].find("td").text.strip()
        flightNumber = flightInfoRows[0].find("td").text.strip()
        DepartureInfo = flightOption.find("div", {"class": "card-left"})
        DepartureTime = DepartureInfo.find("span").text.strip()
        if stopInfo > 0:
            continue
        nonStops += 1
        validFlight['flightNumber'] = flightNumber
        validFlight['DepartTime'] = DepartureTime
        validFlights.append(validFlight)
    print("we have got possible number of flights", nonStops)
    return validFlights


def ticketMatchPredicates(flight, predicates):
    for predicate in predicates:
        predicateCheck = True
        for key, value in predicate.items():
            strValue = str(value)
            if key not in flight or strValue not in str(flight[key]):
                predicateCheck = False
                break
        if predicateCheck:
            return True
    return False


def checkForTextAlerts(flights, query):
    for flight in flights:
        textM = flight['flightNumber'] + " " + flight['Origin'] + "-" + flight['Destination'] + " " + flight[
            'DepartTime'] + " "
        if ticketMatchPredicates(flight, query['Predicates']):
            textM += flight['Class'] + " available"
        if 'available' in textM:
            print("finalTextMessage", textM)
            textMessage(textM)


def textMessage(message):
    cmd = 'osascript sendMessage.scpt 4129808827 "EVA Search Result: {0}"'.format(message)
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
    # Check when ANA will release award ticket
    # flightQuerys.append(
    #     {"Origin": "NRT", "Destination": "SFO", "DepartDate": '20201125', "Class": "Business", "Predicates": [p1]})
    # flightQuerys.append(
    #     {"Origin": "SFO", "Destination": "NRT", "DepartDate": "20201125", "Class": "Business", "Predicates": [p1]})
    flightQuerys.append(
        {"Origin": "SFO", "Destination": "NRT", "DepartDate": ANACloseDay, "Class": "First", "Predicates": [p1]})
    flightQuerys.append(
        {"Origin": "SFO", "Destination": "NRT", "DepartDate": ANACloseDay1, "Class": "First", "Predicates": [p1]})
    flightQuerys.append(
        {"Origin": "SFO", "Destination": "NRT", "DepartDate": ANACloseDay2, "Class": "First", "Predicates": [p1]})
    flightQuerys.append(
        {"Origin": "SFO", "Destination": "NRT", "DepartDate": ANACloseDay3, "Class": "First", "Predicates": [p1]})
    flightQuerys.append(
        {"Origin": "SFO", "Destination": "NRT", "DepartDate": '20191218', "Class": "First", "Predicates": [p1]})
    # Check when SQ will release award ticket
    flightQuerys.append(
        {"Origin": "SIN", "Destination": "TPE", "DepartDate": ANACloseDay, "Class": "Business", "Predicates": [p2]})
    flightQuerys.append(
        {"Origin": "SIN", "Destination": "TPE", "DepartDate": ANACloseDay1, "Class": "Business", "Predicates": [p2]})
    flightQuerys.append(
        {"Origin": "SIN", "Destination": "TPE", "DepartDate": ANACloseDay2, "Class": "Business", "Predicates": [p2]})
    flightQuerys.append(
        {"Origin": "SIN", "Destination": "TPE", "DepartDate": ANACloseDay3, "Class": "Business", "Predicates": [p2]})
    # flightQuerys.append(
    #     {"Origin": "SIN", "Destination": "TPE", "DepartDate": "20200115", "Class": "Business", "Predicates": [p2]})


def start():
    setFlightQuery()
    while True:
        for flightQuery in flightQuerys:
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================Query Started {}============================================".format(
                dt_string))
            print("flightQuery", flightQuery)
            htmlData = {}
            # with open('unitedResult.json') as json_file:
            #     data = json.load(json_file)
            try:
                htmlData = getQueryData(flightQuery['Origin'], flightQuery['Destination'], flightQuery['DepartDate'],
                                        flightQuery['Class'])
            except Exception as e:
                print("We have error query the flight result", e)
                traceback.print_exc()
                print("we now try reload the cookie and header via selenium")
                browser = webdriver.Chrome()
                try:
                    reloadHeaderAndCookie(browser)
                except Exception as e:
                    print("we have error reload cookie, we continue", e)
                    browser.quit()
                    continue
                print("we have reloaded cookie and header")
                continue
            try:
                flightCandidates = analyzeQueryData(htmlData, flightQuery)
                checkForTextAlerts(flightCandidates, flightQuery)
            except Exception as e:
                print("we have issue parse the search result, we wait 10 seconds before next one", e)
                time.sleep(10)
                continue

            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================Query Ended {}============================================".format(
                dt_string))
            print("sleep 30 seconds between flight query")
            time.sleep(30)
        print("*******************************************We finished one loop on query********************************\n\n\n\n")


if __name__ == '__main__':
    start()
