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

# results matching predicates
e1 = {"Price": 35000, "Type": "Economy"}
b1 = {"Type": "Business Saver", "flightNumber": "NH"}
b2 = {"Type": "Business Saver", "flightNumber": "SQ"}
# Japan to USA 110k, china to USA 120k
f1 = {"Type": "First", "flightNumber": "NH"}

flightQuerys = []
browser = None


def getDefaultQuery():
    data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"San Francisco, CA, US (SFO - All Airports)","Destination":"Tokyo, JP (TYO - All Airports)","DepartDate":"Oct 15, 2020","DepartDateBasicFormat":"2020-10-15","ReturnDate":"Oct 15, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Oct 15, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"TYO","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Thu, Oct 15, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":true,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"2186999E-4328-42B7-ACBD-E12F708C69E0","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"ECONOMY","awardCabinType":0,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"a34b34b1-0519-4908-82f2-66add950bad4","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    # data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SIN","Destination":"TPE","DepartDate":"Jan 15, 2020","DepartDateBasicFormat":"2020-01-15","ReturnDate":"Jan 15, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Jan 15, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"TPE","Index":1,"Origin":"SIN","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Jan 15, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"8A5EF7DE-3AAC-4946-9A72-C8062577C758","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"ShowAvailableOnlyUpgrades":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"AvailablePlusPoints":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"RealUpgradePath":false,"UpgradePath":false,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"ECONOMY","awardCabinType":0,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"SelectedUpgradePrices":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"657d2857-f7cc-429a-99e5-4feab6dfd53f","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    jsonData = json.loads(data)
    return jsonData


def analyzeQueryData(data):
    tripIndex = 0
    flightCandidates = []
    for tripIndex, trip in enumerate(data['data']['Trips']):
        nonStops = 0
        for flightIndex, flight in enumerate(trip['Flights']):
            if flight['StopsandConnections'] >= 1:
                continue
            nonStops += 1
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
                        ticket['flightNumber'] = validFlight['flightNumber']
                        validFlight['tickets'].append(ticket)
                        isValid = True
            if isValid:
                flightCandidates.append(validFlight)
        print("we have got possible number of flights", nonStops)
    #print(flightCandidates)
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
    OriginAll = False
    if len(origin) > 4 or len(destination) > 4:
        OriginAll = True
    year = departDate.split('-')[0]
    month = int(departDate.split('-')[1])
    day = departDate.split('-')[2]
    monthName = calendar.month_abbr[month]
    formattedDate = "{0} {1}, {2}".format(monthName, day, year)

    headers = {}
    cookies = {}
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

    # "Origin":"San Francisco, CA, US (SFO - All Airports)","Destination":"Tokyo, JP (TYO - All Airports)"
    jsonQuery['Origin'] = origin
    jsonQuery['Destination'] = destination
    jsonQuery['DepartDateBasicFormat'] = departDate

    jsonQuery.pop('DepartDate', None)
    jsonQuery.pop('ReturnDate', None)
    jsonQuery.pop('CartId', None)
    jsonQuery.pop('Cached', None)
    # "DepartDate": "Sep 16, 2020"
    for trip in jsonQuery['Trips']:
        trip.pop('FormatedDepartDate', None)
        trip['DepartDate'] = formattedDate
        trip['Origin'] = origin
        trip['Destination'] = destination
        trip['OriginAll'] = OriginAll
    data = json.dumps(jsonQuery)

    cookies.pop('SearchInput', None)
    cookies.pop('CachedSearchInput', None)
    # print("headers", headers)
    # print("cookies", cookies)
    # print("querydata", data)
    # data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SFO","Destination":"NRT","DepartDate":"Sep 16, 2020","DepartDateBasicFormat":"2020-09-16","ReturnDate":"Sep 16, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Sep 16, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"NRT","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Sep 16, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"ACD33A44-E39F-46C9-8A03-68F7F4460A32","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":1,"cabinSelection":"BUSINESS","awardCabinType":2,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"a34b34b1-0519-4908-82f2-66add950bad4","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    # data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SIN","Destination":"TPE","DepartDate":"Jan 15, 2020","DepartDateBasicFormat":"2020-01-15","ReturnDate":"Jan 15, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Jan 15, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"TPE","Index":1,"Origin":"SIN","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Jan 15, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"8A5EF7DE-3AAC-4946-9A72-C8062577C758","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"ShowAvailableOnlyUpgrades":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"AvailablePlusPoints":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"RealUpgradePath":false,"UpgradePath":false,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"ECONOMY","awardCabinType":0,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"SelectedUpgradePrices":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"657d2857-f7cc-429a-99e5-4feab6dfd53f","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
    response = queryRequest(headers, cookies, data)
    print("flight query status", response.status_code)
    # print("flight query result", response.content)
    searchResult = response.content
    my_json = searchResult.decode('utf8').replace("'", '"')

    my_jsonResult = json.loads(my_json)
    return my_jsonResult


@timeout(60, os.strerror(errno.ETIMEDOUT))
def queryRequest(headers, cookies, data):
    response = requests.post(
        'https://www.united.com/ual/en/us/flight-search/book-a-flight/flightshopping/getflightresults/awd',
        headers=headers, cookies=cookies, data=data)
    return response


def reloadHeaderAndCookie():
    global browser
    browsermob_path = '/usr/local/browsermob-proxy-2.1.4/bin/browsermob-proxy'
    server = Server(browsermob_path, {'port':8090})
    server.start()
    time.sleep(1)
    proxy = server.create_proxy()
    time.sleep(1)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    browser = webdriver.Chrome(options=chrome_options)
    url1 = "https://www.united.com/en/us"
    url2 = "https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1"

    options = {'captureHeaders': True, 'captureCookies': True}
    proxy.new_har("united", options=options)
    browser.get(url1)
    time.sleep(5)

    browser.get(url2)

    newH = proxy.har  # returns a HAR JSON blob
    with open('latestUnitedAuth.json', 'w') as outfile:
        json.dump(newH, outfile)
    time.sleep(10)
    server.stop()
    browser.quit()

# reloadHeaderAndCookie()
# sys.exit(0)

# testTicket = [{'Type': 'Economy (lowest award)', 'numberOfSeats': 'X3', 'Price': 35000}, {'Type': 'Business Saver Award ', 'numberOfSeats': 'I2', 'Price': 80000}, {'Type': 'Business Everyday Award ', 'numberOfSeats': 'I2', 'Price': 175000}]
# testP = [b1, f1]
# any predicate match, we return true
# all key values have to match inside a predicate
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


# print(ticketMatchPredicates(testTicket[1], testP))
# sys.exit(0)

def checkForTextAlerts(flights, query):
    for flight in flights:
        textM = flight['flightNumber'] + " " + flight['Origin'] + "-" + flight['Destination'] + " " + flight[
            'DepartTime'] + " "
        for ticket in flight['tickets']:
            if ticketMatchPredicates(ticket, query['Predicates']):
                textM += ticket['Type'] + " " + ticket['numberOfSeats'] + " available |"
        if 'available' in textM:
            print("finalTextMessage", textM)
            textMessage(textM)


def textMessage(message):
    cmd = 'osascript sendMessage.scpt 4129808827 "United Search Result: {0}"'.format(message)
    os.system(cmd)
    time.sleep(5)


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
            reloadHeaderAndCookie()
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
        print("*******************************************We finished one loop on query********************************\n\n\n\n")


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


def getCloseANADate():
    start_date = datetime.now()
    end_date = start_date + timedelta(days=4)
    dt_string = end_date.strftime("%Y-%m-%d")
    # print("getFurtherANADate", dt_string)
    return dt_string


def plusDay(originalDay, addDay):
    start_date = datetime.strptime(originalDay, "%Y-%m-%d")
    end_date = start_date + timedelta(days=addDay)
    dt_string = end_date.strftime("%Y-%m-%d")
    return dt_string


def setFlightQuery():
    global flightQuerys
    # for predicate in predicates array, as long as we have a match, we alert the result

    ANACloseDay = getCloseANADate()
    flightQuerys.append({"Origin": "SFO", "Destination": "NRT", "DepartDate": ANACloseDay, "Predicates": [f1, b1]})
    for i in range(1, 10):
        testDay = plusDay(ANACloseDay, i)
        flightQuerys.append({"Origin": "SFO", "Destination": "NRT", "DepartDate": testDay, "Predicates": [f1, b1]})
    flightQuerys.append({"Origin": "SIN", "Destination": "TPE", "DepartDate": "2020-01-15", "Predicates": [b2]})
    for i in range(1, 3):
        testDay = plusDay(ANACloseDay, i)
        flightQuerys.append({"Origin": "SIN", "Destination": "TPE", "DepartDate": testDay, "Predicates": [b2]})

#
if __name__ == '__main__':
    start()
