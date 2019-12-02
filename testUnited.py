import requests

cookies = {
    'bm_sz': '7D9047B0CD93CE9CDF0991D0B37710FE~YAAQX5bfF85yibRuAQAAWkktwAV08j0iiUxA9jwrDxw/iSDsLBvTBjIYGtyrb9eqpVGye54z+FOedYOvqIf05ZQq+0WQTeZsT1wWXzAcIgjPlBKfdSsrnE36s5eFy7btIt3OFAEP0EYNpoBtmVAU8AAcuGHCZ0AoZKvrGZzLgazrbK3fvKLtEz1xWBUFvzDn',
    'optimizely_id': '1575182232.79694586',
    'newHP': 'true',
    '_ga': 'GA1.2.1103758072.1575182233',
    '_gid': 'GA1.2.260192068.1575182233',
    '_gat_tealium_0': '1',
    'Session': 'AuthToken=YZn6jJOW6bWfl7j8lf6vu0mCB1yFNtoFeqvHeW%2fU0ewfZvJManmEVoTS0%2fQdAe0SFrtmRuw6tMgkgOR%2f2P33hQ%3d%3d',
    'QuantumMetricUserID': 'c01da1b4ec8656a6c99d30771325dd66',
    'QuantumMetricSessionID': '6b13df516ac2b029568af426d9adbed3',
    'oo_OODynamicRewrite_weight': '0',
    'oo_inv_percent': '0',
    'oo_inv_hit': '1',
    'LPVID': 'QwMTZmZDJiNDZhMDUwYjY2',
    'LPSID-84608747': 'LT1a4XDQSpuUyLM6ndLVqw',
    'Locale': 'POS=US&Lang=en&UMID=f4770c80-d535-4738-8f30-5e2406284b41&POSCODE=',
    'TLTSID': '074115204A8E3889E247B2B79477A6F2',
    'TLTUID': '074115204A8E3889E247B2B79477A6F2',
    'mmcore.bid': 'lvsvwcgus04',
    'uasession': 'UASessionId=76bf0217-f673-4869-afa6-e917c4bd3763&TabId=10682925-f8bd-417e-b6c7-d338d41db5ec',
    'utag_main': 'v_id:016ec02d6b800044d33799e8893c03079001c07100838$_sn:1$_se:5$_ss:0$_st:1575184042899$ses_id:1575182232450%3Bexp-session$_pn:2%3Bexp-session',
    'flightSearchSession': '11910302237229430.05579542113069724',
    '_gat': '1',
    #'SearchInput': '{"Origin":"SFO","Destination":"NRT","Trips":null,"DepartDate":"Oct 21, 2020","ReturnDate":"","searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","awardTravel":"True","cabinType":"econ","awardCabinType":"awardBusinessFirst","numOfAdults":"1","numOfSeniors":"0","numOfChildren04":"0","numOfChildren03":"0","numOfChildren02":"0","numOfChildren01":"0","numOfInfants":"0","numOfLapInfants":"0","numberOfTravelers":"1","isFlexible":false,"FlexibleDays":0,"FlexibleDate":"Oct 21, 2020","isNonStop":true,"Cached":{"UaSessionId":"76bf0217-f673-4869-afa6-e917c4bd3763","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]}}',
    #'CachedSearchInput': '{"UaSessionId":"76bf0217-f673-4869-afa6-e917c4bd3763","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]}',
    'RT': 'sl=3&ss=1575182231150&tt=9453&obo=0&bcn=%2F%2F17d98a5a.akstat.io%2F&sh=1575182244590%3D3%3A0%3A9453%2C1575182242911%3D2%3A0%3A6083%2C1575182234899%3D1%3A0%3A2713&dm=united.com&si=d9d020f8-1052-4c66-8625-65af8953f684&ld=1575182244591&nu=https%3A%2F%2Fwww.united.com%2Fual%2Fen%2FUS%2Fflight-search%2Fbook-a-flight&cl=1575182257239&r=https%3A%2F%2Fwww.united.com%2Fual%2Fen%2FUS%2Fflight-search%2Fbook-a-flight&ul=1575182283278&hd=1575182285142',
    'mmcore.tst': '0.319',
    'mmapi.store.p.0': '%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%22pd%22%3A%221606718285478%7C%5C%22-95240467%7CAgAAAApVAwCuQTWBbRJ1PQABEgABQgA9FTcDAQAq1McFKXbXSN%2Fny%2BsodtdIAAAAAP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FAA53d3cudW5pdGVkLmNvbQJtEgEAAAAAAAAAAAA2FwAANhcAAP%2F%2F%2F%2F8AAAAAAAAAAUU%3D%5C%22%22%2C%22bid%22%3A%221575182885100%7C%5C%22lvsvwcgus04%5C%22%22%2C%22srv%22%3A%221606718285489%7C%5C%22lvsvwcgus04%5C%22%22%7D%7D',
    'mmapi.store.s.0': '%7B%22mmparams.d%22%3A%7B%7D%2C%22mmparams.p%22%3A%7B%7D%7D',
    'akavpau_ualwww': '1575182886~id=d85fd4ea9851a0d07328e74419e7be42',
    '_abck': '779639A91EE861B530B613E626E7B72C~-1~YAAQX5bfF+qBibRuAQAAwT0uwAKQUddhMR4E3se8gs6nxx8EexijUy3hrLVaa0VZI86H2XnkXYOPU9ZFYA6n4g7i2n3m4eWyMqfJWI/li3YOJp6Iu71QAVXx48567ku2Fx4m36br6j9sAjLbuAFLscSWQvBB9koZqzOh23+Rdo9KH+y0ctNSNkBSu3U70A0z4PDGQG8c2f9ccAgYjIpb3vrCcpvE2xOzNmLkHf+Hrr0MAl6lytqAiIKCfk/9eIN+MIgpglQFnI31okegU5P0JcMIFKN52Pqsirjm5rDpc8hGZZzgWvL9f4ZzjjFyXl4KWqgH032sS4VIqyztob/FzvYP3Cw=~-1~-1~-1',
}

headers = {
    'Host': 'www.united.com',
    'UASessionTabId': '10682925-f8bd-417e-b6c7-d338d41db5ec',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'https://www.united.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/json; charset=UTF-8',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.united.com/ual/en/us/flight-search/book-a-flight/results/awd?f=SFO&t=NRT&d=2020-10-21&tt=1&st=bestmatches&at=1&rm=1&act=2&cbm=-1&cbm2=-1&sc=1&px=1&taxng=1&idx=1',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = '{"Revise":false,"UnaccompaniedMinorDisclamer":false,"IsManualUpsellFromBasicEconomy":false,"StartFlightRecommendation":false,"FareWheelOrCalendarCall":false,"RelocateRti":false,"ConfirmationID":null,"searchTypeMain":"oneWay","realSearchTypeMain":"oneWay","Origin":"SFO","Destination":"NRT","DepartDate":"Oct 21, 2020","DepartDateBasicFormat":"2020-10-21","ReturnDate":"Oct 21, 2020","ReturnDateBasicFormat":null,"awardTravel":true,"MaxTrips":null,"numberOfTravelers":1,"numOfAdults":1,"numOfSeniors":0,"numOfChildren04":0,"numOfChildren03":0,"numOfChildren02":0,"numOfChildren01":0,"numOfInfants":0,"numOfLapInfants":0,"travelerCount":1,"revisedTravelerKeys":null,"revisedTravelers":null,"OriginalReservation":null,"RiskFreePolicy":null,"EmployeeDiscountId":null,"IsUnAccompaniedMinor":false,"MilitaryTravelType":null,"MilitaryOrGovernmentPersonnelStateCode":null,"tripLength":0,"MultiCityTripLength":null,"IsParallelFareWheelCallEnabled":false,"flexMonth":null,"flexMonth2":null,"SortType":"bestmatches","SortTypeV2":null,"cboMiles":"-1","cboMiles2":"-1","Trips":[{"BBXCellIdSelected":null,"BBXSession":null,"BBXSolutionSetId":null,"DestinationAll":false,"returnARC":null,"connections":null,"nonStopOnly":true,"nonStop":true,"oneStop":false,"twoPlusStop":false,"ChangeType":0,"DepartDate":"Oct 21, 2020","ReturnDate":null,"PetIsTraveling":false,"PreferredTime":"","PreferredTimeReturn":null,"Destination":"NRT","Index":1,"Origin":"SFO","Selected":false,"NonStopMarket":false,"FormatedDepartDate":"Wed, Oct 21, 2020","OriginCorrection":null,"DestinationCorrection":null,"OriginAll":false,"Flights":null,"SelectedFlights":null,"OriginTriggeredAirport":false,"DestinationTriggeredAirport":false,"StopCount":0,"HasNonStopFlights":false,"Ignored":false,"Sequence":0,"IsDomesticUS":false,"ClearAllFilters":false}],"nonStopOnly":1,"CalendarOnly":false,"Matrix3day":false,"InitialShop":true,"IsSearchInjection":false,"CartId":"C8B504FA-CF93-4044-849A-567C55B43941","CellIdSelected":null,"BBXSession":null,"SolutionSetId":null,"SimpleSearch":true,"RequeryForUpsell":false,"RequeryForPOSChange":false,"YBMAlternateService":false,"ShowClassOfServiceListPreference":false,"SelectableUpgradesOriginal":null,"RegionalPremierUpgradeBalance":0,"GlobalPremierUpgradeBalance":0,"RegionalPremierUpgrades":null,"GlobalPremierUpgrades":null,"FormattedAccountBalance":null,"GovType":null,"TripTypes":1,"RealTripTypes":1,"flexible":false,"flexibleAward":false,"FlexibleDaysAfter":0,"FlexibleDaysBefore":0,"hiddenPreferredConn":null,"hiddenUnpreferredConn":null,"carrierPref":0,"chkFltOpt":0,"portOx":0,"travelwPet":0,"NumberOfPets":0,"cabinType":0,"cabinSelection":"BUSINESS","awardCabinType":2,"FareTypes":0,"FareWheelOnly":false,"EditSearch":false,"buyUpgrade":0,"offerCode":null,"IsPromo":false,"TVAOfferCodeLastName":null,"ClassofService":null,"UpgradeType":null,"AdditionalUpgradeIds":null,"BillingAddressCountryCode":null,"BillingAddressCountryDescription":null,"IsPassPlusFlex":false,"IsPassPlusSecure":false,"IsOffer":false,"IsMeetingWorks":false,"IsValidPromotion":false,"IsCorporate":0,"CalendarDateChange":null,"CoolAwardSpecials":false,"LastResultId":null,"IncludeLmx":false,"NGRP":true,"calendarStops":0,"IsAwardNonStopDisabled":false,"IsWeeklyAwardCalendarEnabled":true,"IsMonthlyAwardCalendarEnabled":true,"AwardCalendarType":0,"IsAwardCalendarEnabled":true,"IsAwardCalendarNonstop":false,"corporateBooking":false,"IsCorporateLeisure":false,"CorporateDiscountCode":"","IsAutoUpsellFromBasicEconomy":false,"CurrencyDescription":"International POS Cuurency","CurrentTripIndex":0,"LowestNonStopEconomyFare":0,"FromFlexibleCalendar":false,"TripIndex":0,"Cached":{"UaSessionId":"76bf0217-f673-4869-afa6-e917c4bd3763","CarrierPref":0,"PreferredConn":null,"UnpreferredConn":null,"HiddenPreferredConn":null,"HiddenUnpreferredConn":null,"Trips":[{"NonStop":true,"OneStop":false,"TwoPlusStop":false,"PreferredTime":"","PreferredTimeReturn":null,"ClearAllFilters":false}]},"isReshopPath":false}'

response = requests.post('https://www.united.com/ual/en/us/flight-search/book-a-flight/flightshopping/getflightresults/awd', headers=headers, cookies=cookies, data=data)
print response.content
