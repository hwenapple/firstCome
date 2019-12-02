import requests
import browsercookie
cookies = {
    '_ga': 'GA1.2.1799542677.1558501176',
    'QuantumMetricUserID': 'b97eebfe031cb99aaf593bbfc25605b0',
    'LPVID': 'NiZDA1ZDc4MTA3MDM0MGJl',
    'TLTUID': '7D720B7D491C5C3CC50BC9A3285C3DA0',
    '_gcl_au': '1.1.38493150.1558501301',
    'v1st': 'CAAC6D50E70220BB',
    'Locale': 'POS=US&Lang=en&UMID=e8383a97-6c79-4299-b7b1-a81cc632494e&POSCODE=L',
    '_fbp': 'fb.1.1562183395199.1251713961',
    'IsRemembered': 'True',
    'Device': 'Num=2BC7T0EL85A9KL1VTFkglifAzGpxdc509iDMXk3+9+LIm6/zgsozWhrkZcQJYXGg',
    '_up': '1.2.1183273955.1574467902',
    'optimizely_id': '1574571407.56260001',
    'oo_inv_percent': '0',
    'TLTSID': '2341AF6347288B1C0425378D98D2DD2C',
    'uasession': 'UASessionId=b74cdf17-8d56-4cb5-91b4-28d9d32ff9f2&TabId=2ebe93b0-3743-4bab-b213-53c880468af9',
    'AuthCookie': 'c68326cf1928efff0f07908e4ff8737735c1860c88518c40e212f7c2aaf54d841a9e2d4d689f3085d63f39272d6a75e1',
    'User': 'RememberID=PzABH39SU2F126XNwVkTp4jYotlXIwUi7llpOJZ4cTs%3D&LoyaltyID=%2FWmnAgEphDsp4FJrS%2BRYwydBS%2F59aSobfCfaYiKlihY%3D&SecondID=bzERhfN5%2B9g5pZ5nweEP62b4%2FEZj2OWMvazyGMpN49o%3D&FName=haoran&CustomerId=iZQQeDC1fTXDCmwCUNdGjbuOQ7XxkSLTxoMTx7o3h0I%3D&CurrentELiteLevel=5QPkvpwk%2B0V5OQFMvNQ2lnDQLbsTedBUvpbhAD7jhFY%3D',
    '_gid': 'GA1.2.878322604.1575172824',
    'QuantumMetricSessionID': 'efffa18e2c0b17e4f19209786283ddda',
    'LPSID-84608747': 'k0ssfPN0So23GfLISK_5cQ',
    'SearchInput': '{"Origin":"SFO","Destination":"NRT","Trips":null,"DepartDate":"Sep 16, 2020","ReturnDate":"","searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","awardTravel":"True","cabinType":"econ","awardCabinType":"awardBusinessFirst","numOfAdults":"1","numOfSeniors":"0","numOfChildren04":"0","numOfChildren03":"0","numOfChildren02":"0","numOfChildren01":"0","numOfInfants":"0","numOfLapInfants":"0","numberOfTravelers":"1","isFlexible":false,"FlexibleDays":0,"FlexibleDate":"Sep 16, 2020","isNonStop":false,"Cached":{"UaSessionId":"b74cdf17-8d56-4cb5-91b4-28d9d32ff9f2","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":true,"TwoPlusStop":true,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]}}',
    'CachedSearchInput': '{"UaSessionId":"b74cdf17-8d56-4cb5-91b4-28d9d32ff9f2","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":true,"TwoPlusStop":true,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]}',
    'newHP': 'true',
    'oo_OODynamicRewrite_weight': '0',
    'oo_inv_hit': '12',
    'Session': 'AuthToken=IpzAQjRXoaxGyh7nVWvuXKojnaMEFJvy5BFfLXNmdNzsAqmcCIS8A1MfYbxMCiWIb4ObvPKcU%2BoMopYhqnyoaA%3D%3D',
    'mmcore.tst': '0.928',
    'mmapi.store.p.0': '%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221606789032348%7C%5C%22368766851%7CfQEAAApVAwDu9nkGrBHl0gABEgABQgCr81PbLQDUVmC%2FzXbXSIe4OVdy3tZIAAAAAP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAAZEaXJlY3QBbRIFAAQAAgAAAAAANhcAADYXAAA2FwAABACzpgAAaKrCFHVlEgAdigAABScSZRL%2F%2FwIAAAH13a9PAdt%2FAQBmSQIAATYXAAAWAAAAsAMBALQA6BnSJxIA%2F%2F%2F%2F%2FwEnEmUS%2F%2F8DAAABAAAAAAEYXAIA7ZUDAAE2FwAARgAAAEEMAQDIj3aNmmUSAGzJAAAFZRJlEv%2F%2FAgAAAQAAAAABsnICAJK0AwABNhcAACIAAABADAEABOlukDplEgD%2F%2F%2F%2F%2FAWUSZRL%2F%2FwIAAAEAAAAAAbFyAgCKtAMAATYXAAAcAAAAAAAAAAABRQ%3D%3D%5C%22%22%2C%22bid%22%3A%221575253631971%7C%5C%22lvsvwcgus05%5C%22%22%2C%22srv%22%3A%221606789032361%7C%5C%22lvsvwcgus05%5C%22%22%7D%2C%22BookingPath_International%20Baggage%22%3A%7B%7D%2C%22BookingPath_Relocate%20RTI%22%3A%7B%7D%2C%22BookingPath_Lowest_Price_On_RTI%22%3A%7B%7D%2C%22Relative%20Pricing%20on%20FSR%22%3A%7B%7D%2C%22CTA%20Alignment%22%3A%7B%7D%2C%22Fare_Header_UI_on_FSR%22%3A%7B%7D%7D',
    'mmapi.store.s.0': '%7B%22mmparams.p%22%3A%7B%7D%2C%22mmparams.d%22%3A%7B%7D%7D',
    'mmcore.bid': 'lvsvwcgus05',
    'utag_main': 'v_id:016c130eae81001378c5e129d87303079006707100838$_sn:46$_se:56$_ss:0$_st:1575254833175$ses_id:1575248898662%3Bexp-session$_pn:7%3Bexp-session',
    'flightSearchSession': '1191111817132410.7114601793432831',
    '_gat': '1',
    '_derived_epik': 'dj0yJnU9cUlrUVFySFRCY3NJdWVSalZtc2Q5T2hZV2pyajd0YnEmbj1mQ2VEZmxRSEZSVU12M1l6el9WRUtnJm09NyZ0PUFBQUFBRjNrZEN3',
    '_abck': 'A58EBC3BD38EED5D935D259804544A6F~-1~YAAQRZbfF8lj9JJuAQAALdVlxAK7jGn7PS87QhA8Mjcreuud3GSJD62I7B8IWGMhs6zqLMSUqcL2iRlolj8DzoHTeaKRGjlBQEIEPyrKF/SiegjrVKJAxedSlmS6e4PlSYESuLeMcB3t6Oo+HlCPYHyQRwLRTtQ5K+PYw2JEVWlcB/qV96SM9T9KNjvphMGi48T3qzefZyguVhZa/ozHWYu+YGjheRichDLCI9wOSokeSTAZOjfnmbcQIUnnCtqBPVaCEEK2q1U01Q98NOYzaYF1BT8Tfe8hIcEzvHWmjAKNDIQs683alpKRozz3zTluda7qVuu4HnrbTNw/l9C3Zlkd+MZWn3I+93Ps~-1~-1~-1',
    '_gat_gtag_UA_93174402_1': '1',
    'akavpau_ualwww': '1575253644~id=53eaabdec98191477ada179241d94c55',
    'RT': 'sl=9&ss=1575248897309&tt=30802&obo=0&sh=1575253035458%3D9%3A0%3A30802%2C1575253033838%3D8%3A0%3A25608%2C1575251807804%3D7%3A0%3A21641%2C1575250994634%3D6%3A0%3A16548%2C1575250974103%3D5%3A0%3A13923&dm=united.com&si=ce79c1e9-84af-4a55-9d5f-f71f699d4d46&bcn=%2F%2F17d98a5e.akstat.io%2F&ld=1575253035459&r=https%3A%2F%2Fwww.united.com%2Fual%2Fen%2FUS%2Fflight-search%2Fbook-a-flight%2Fresults%2Fawd%3F00e6249650469b04e151900366b9d34b&ul=1575253059384&hd=1575253059441',
}

headers = {
    'Host': 'www.united.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = (
    ('f', 'SFO'),
    ('t', 'NRT'),
    ('d', '2020-09-16'),
    ('tt', '1'),
    ('at', '1'),
    ('sc', '7'),
    ('act', '2'),
    ('px', '1'),
    ('taxng', '1'),
    ('newHP', 'True'),
    ('idx', '1'),
)


cj = browsercookie.chrome()


# session = requests.Session()
# session.get('https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd', headers=headers, params=params)
# print session.cookies.get_dict()
#
response = requests.get('https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd', headers=headers, params=params, cookies=cj)
print response

#
# data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SFO","Destination":"NRT","DepartDate":"Sep 16, 2020","DepartDateBasicFormat":"2020-09-16","ReturnDate":"Sep 16, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":null,"SortTypeV2":null,"cboMiles":null,"cboMiles2":null,"Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":false,"nonStop":true,"oneStop":true,"twoPlusStop":true,"ChangeType":0,"DepartDate":"Sep 16, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"NRT","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Sep 16, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":0,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"63AA1D8E-32FA-414E-A064-A174FD50F1BA","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"BUSINESS","awardCabinType":2,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":4,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"b74cdf17-8d56-4cb5-91b4-28d9d32ff9f2","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":true,"TwoPlusStop":true,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'
#
#
#
# headers = {
#     'Host': 'www.united.com',
#     'UASessionTabId': '2ebe93b0-3743-4bab-b213-53c880468af9',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Origin': 'https://www.united.com',
#     'X-Requested-With': 'XMLHttpRequest',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
#     'Content-Type': 'application/json; charset=UTF-8',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Referer': 'https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1',
#     'Accept-Language': 'en-US,en;q=0.9',
# }
#
# response = requests.post('https://www.united.com/ual/en/us/flight-search/book-a-flight/flightshopping/getflightresults/awd', headers=headers, cookies=cj, data=data)
#
# print response.content
#print response.content
# file = open("newUnited.html","w")
# file.write(response.content)
#
# file.close()


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.united.com/ual/en/US/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-09-16&tt=1&at=1&sc=7&act=2&px=1&taxng=1&newHP=True&idx=1', headers=headers, cookies=cookies)
