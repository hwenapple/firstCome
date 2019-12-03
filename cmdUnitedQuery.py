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

# results matching predicates
e1 = {"Price": 35000, "Type": "Economy"}
b1 = {"Price": 80000, "Type": "Business"}
# Japan to USA 110k, china to USA 120k
f1 = {"Price": 110000, "Type": "First"}

flightQuerys = []


def getDefaultQuery():
    data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SFO","Destination":"NRT","DepartDate":"Sep 16, 2020","DepartDateBasicFormat":"2020-09-16","ReturnDate":"Sep 16, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Sep 16, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"NRT","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Sep 16, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"ACD33A44-E39F-46C9-8A03-68F7F4460A32","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":1,"cabinSelection":"BUSINESS","awardCabinType":2,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"a34b34b1-0519-4908-82f2-66add950bad4","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"San Francisco, CA, US (SFO - All Airports)","Destination":"Tokyo, JP (TYO - All Airports)","DepartDate":"Oct 15, 2020","DepartDateBasicFormat":"2020-10-15","ReturnDate":"Oct 15, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Oct 15, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"TYO","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Thu, Oct 15, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":true,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"2186999E-4328-42B7-ACBD-E12F708C69E0","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"ECONOMY","awardCabinType":0,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"a34b34b1-0519-4908-82f2-66add950bad4","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'

    jsonData = json.loads(data)
    return jsonData


def analyzeQueryData(data):
    tripIndex = 0
    flightCandidates = []
    for tripIndex, trip in enumerate(data['data']['Trips']):
        for flightIndex, flight in enumerate(trip['Flights']):
            if flight['StopsandConnections'] >= 1:
                continue
            validFlight = {}
            validFlight['flightNumber'] = flight['OperatingCarrier'] + flight['FlightNumber']
            validFlight['Origin'] = flight['Origin']
            validFlight['Destination'] = flight['Destination']
            validFlight['DepartTime'] = flight['DepartDateFormat'] + "," + flight['DepartTimeFormat']
            validFlight['BookingClassAvailList'] = flight['BookingClassAvailList']
            validFlight['tickets'] = []
            isValid = False
            for product in flight['Products']:
                if product['BookingCount'] > 0:
                    ticket = {}
                    ticket['Type'] = product['ProductTypeDescription']
                    ticket['numberOfSeats'] = product['BookingCode'] + str(product['BookingCount'])
                    if product['Prices']:
                        ticket['Price'] = int(product['Prices'][0]['Amount'])
                        validFlight['tickets'].append(ticket)
                        isValid = True
            if isValid:
                flightCandidates.append(validFlight)
    print(flightCandidates)
    return flightCandidates

    # print(flight)
    # print("\n\n")


def parseHarObjects(original):
    newObj = {}
    for item in original:
        newObj[item['name']] = item['value']
    return newObj

def formattedCityName(airportName):
    matchStrs = {'SFO': "San Francisco, CA, US (SFO - All Airports)", "NRT": "Tokyo, JP (TYO - All Airports)"}
    return matchStrs.get(airportName, airportName)

# original date 2020-09-15, formatted date Sep 16, 2020
def getQueryData(origin, destination, departDate):
    origin = formattedCityName(origin)
    destination = formattedCityName(destination)
    year = departDate.split('-')[0]
    month = int(departDate.split('-')[1])
    day = departDate.split('-')[2]
    monthName = calendar.month_abbr[month]
    formattedDate = "{0} {1}, {2}".format(monthName, day, year)

    headers = {}
    cookies = {}
    data = httpArchive
    with open('latestUnitedAuth.json') as json_file:
        data = json.load(json_file)
    for entry in data['log']['entries']:
        if 'getflightresults' in entry['request']['url']:
            headers = entry['request']['headers']
            cookies = entry['request']['cookies']
            break
    headers = parseHarObjects(headers)
    cookies = parseHarObjects(cookies)
    jsonQuery = getDefaultQuery()

    #"Origin":"San Francisco, CA, US (SFO - All Airports)","Destination":"Tokyo, JP (TYO - All Airports)"
    jsonQuery['Origin'] = origin
    jsonQuery['Destination'] = destination
    jsonQuery['DepartDateBasicFormat'] = departDate
    jsonQuery.pop('DepartDate', None)
    jsonQuery.pop('ReturnDate', None)
    jsonQuery.pop('CartId', None)
    # "DepartDate": "Sep 16, 2020"
    for trip in jsonQuery['Trips']:
        trip.pop('FormatedDepartDate', None)
        trip['DepartDate'] = formattedDate
        trip['Origin'] = origin
        trip['Destination'] = destination
    data = json.dumps(jsonQuery)

    cookies.pop('SearchInput', None)
    cookies.pop('CachedSearchInput', None)
    # print("headers", headers)
    # print("cookies", cookies)
    # print("querydata", data)
    # data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SFO","Destination":"NRT","DepartDate":"Sep 16, 2020","DepartDateBasicFormat":"2020-09-16","ReturnDate":"Sep 16, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Sep 16, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"NRT","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Sep 16, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"ACD33A44-E39F-46C9-8A03-68F7F4460A32","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":1,"cabinSelection":"BUSINESS","awardCabinType":2,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"a34b34b1-0519-4908-82f2-66add950bad4","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    response = requests.post(
        'https://www.united.com/ual/en/us/flight-search/book-a-flight/flightshopping/getflightresults/awd',
        headers=headers, cookies=cookies, data=data)
    print("flight query status", response.status_code)
    # print("flight query result", response.content)
    searchResult = response.content
    my_json = searchResult.decode('utf8').replace("'", '"')

    my_jsonResult = json.loads(my_json)
    return my_jsonResult


def reloadHeaderAndCookie():
    global httpArchive
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path)

    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    browser = webdriver.Chrome(options=chrome_options)
    url1 = "https://www.united.com/en/us"
    url2 = "https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1"

    options = {'captureHeaders': True, 'captureCookies': True}
    proxy.new_har("united", options=options)
    browser.get(url1)
    time.sleep(5)
    server.start()
    time.sleep(2)
    browser.get(url2)

    newH = proxy.har  # returns a HAR JSON blob
    with open('latestUnitedAuth.json', 'w') as outfile:
        json.dump(newH, outfile)
    server.stop()
    browser.quit()
    httpArchive = newH


def ticketMatchPredicates(ticket, predicates):
    for predicate in predicates:
        if predicate['Type'] in ticket['Type']:
            if ticket['Price'] <= predicate['Price']:
                return True
    return False


def checkForTextAlerts(flights, query):
    for flight in flights:
        textM = flight['flightNumber'] + " " + flight['Origin'] + "-" + flight['Destination'] + " " + flight[
            'DepartTime'] + " "
        for ticket in flight['tickets']:
            if ticketMatchPredicates(ticket, query['Predicates']):
                textM += ticket['Type'] + " " + ticket['numberOfSeats'] + " available |"
        if 'available' in textM:
            print("finalTextMessage", textM)



def start():
    setFlightQuery()
    while True:
        for flightQuery in flightQuerys:
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================Query Started {}============================================".format(
                dt_string))
            print("flightQuery", flightQuery)
            data = {}
            # with open('unitedResult.json') as json_file:
            #     data = json.load(json_file)
            try:
                data = getQueryData(flightQuery['Origin'], flightQuery['Destination'], flightQuery['DepartDate'])
            except Exception as e:
                print("We have error query the flight result", e)
                traceback.print_exc()
                print("we now try reload the cookie and header via selenium")
                reloadHeaderAndCookie()
                print("we have reloaded cookie and header")
            if 'status' in data:
                if data['status'] == 'success':
                    flightCadidates = analyzeQueryData(data)
                    checkForTextAlerts(flightCadidates, flightQuery)
                else:
                    print("flight query result is not expected ", data)
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print("===============================Query Ended {}============================================".format(
                dt_string))
            print("sleep 30 seconds between flight query")
            time.sleep(30)


def setFlightQuery():
    global flightQuerys
    # for predicate in predicates array, as long as we have a match, we alert the result
    #flightQuerys.append({"Origin": "SFO", "Destination": "NRT", "DepartDate": "2020-10-19", "Predicates": [b1, f1]})
    flightQuerys.append({"Origin": "SFO", "Destination": "NRT", "DepartDate": "2020-10-18", "Predicates": [e1, b1, f1]})


if __name__ == '__main__':
    start()
