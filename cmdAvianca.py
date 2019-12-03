import requests

cookies = {
    'rxVisitor': '1564886709815HR09DU83P9M2V4KR9E7AUR41NC1LRJ4E',
    '_ga': 'GA1.2.128761326.1574801828',
    '_fbp': 'fb.1.1574801827940.1177769153',
    'cookiePolicyAccepted': 'true',
    'statusInfo': 'LifeMiles',
    'userInfo': '04070320505',
    '_gid': 'GA1.2.1646341149.1575345440',
    'defConf': '%7B%22language%22%3A%22en%22%2C%22country%22%3A%22us%22%2C%22currency%22%3A%22usd%22%7D',
    'sgn_kml': 'false',
    'lstpge': 'AIR_REDEMPTION_PAGE',
    '_gat_UA-21545627-1': '1',
    'JSESSIONID': '2732CA646FF87D76B30F732F54CD2253',
    'dtSa': '-',
    'dra3j': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIwNDA3MDMyMDUwNSIsInVzZXJfbmFtZSI6IjA0MDcwMzIwNTA1Iiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3NTM0Nzg3MTMzOCwiaWF0IjoxNTc1MzQ3ODcxMzM4LCJ0aWQiOiI0NjVCRjRFQzk1MTVGQTREMUQ5NDQ1OUNFODg1MjU5QyIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.YCZ8u7N2pGMfzez-AGWkrDP0GHob2su_YsEkf3wNBvA',
    'dtLatC': '2',
    'dtCookie': '4$C7899AC62FAC90A687CEDE5D7AA30ADC|93fb5a7425baf99b|1',
    'dtPC': '4$347871685_337h21vKCPMKNOCGOKMIBMBNEPIIJFPAIIGHMPP',
    'rxvt': '1575349715594|1575345440372',
}

headers = {
    'Host': 'www.lifemiles.com',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIwNDA3MDMyMDUwNSIsInVzZXJfbmFtZSI6IjA0MDcwMzIwNTA1Iiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3NTM0Nzg3MTMzOCwiaWF0IjoxNTc1MzQ3ODcxMzM4LCJ0aWQiOiI0NjVCRjRFQzk1MTVGQTREMUQ5NDQ1OUNFODg1MjU5QyIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.YCZ8u7N2pGMfzez-AGWkrDP0GHob2su_YsEkf3wNBvA',
    'Origin': 'https://www.lifemiles.com',
    'x-dtpc': '4$347871685_337h21vKCPMKNOCGOKMIBMBNEPIIJFPAIIGHMPP',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.lifemiles.com/air-redemption',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = '{"internationalization":{"language":"en","country":"us","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"SFO","dest":"NRT","departingCity":"San Francisco","arrivalCity":"Tokyo","depDate":"2020-11-11","depTime":""},"filter":false,"codPromo":null,"idCoti":"1371862959","officeId":"","ftNum":"04070320505","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"NH","searchTypePrioritized":"NH","sch":{"schHcfltrc":"dTuGOG42eU31aSGSPp4cKmhzIIpywQri"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"SFO","dest":"NRT","cabin":2}]}'

response = requests.post('https://www.lifemiles.com/lifemiles/air-redemption-flight', headers=headers, cookies=cookies, data=data)
