import requests

cookies = {
    'rxVisitor': '1564886709815HR09DU83P9M2V4KR9E7AUR41NC1LRJ4E',
    '_gcl_au': '1.1.780471324.1579306717',
    '_ga': 'GA1.2.1232935497.1579306717',
    '_fbp': 'fb.1.1579306717804.323937263',
    'cookiePolicyAccepted': 'true',
    'defConf': '%7B%22language%22%3A%22en%22%2C%22country%22%3A%22jp%22%2C%22currency%22%3A%22usd%22%7D',
    'userInfo': '33012219601',
    'statusInfo': 'LifeMiles',
    'sgn_kml': 'false',
    '_gid': 'GA1.2.788441936.1579408019',
    'JSESSIONID': 'DFB105AEB81BA02A0D27FF0667623D3B',
    'dtSa': '-',
    'dra3j': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIzMzAxMjIxOTYwMSIsInVzZXJfbmFtZSI6IjMzMDEyMjE5NjAxIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3OTQ3ODQyMTUyMiwiaWF0IjoxNTc5NDc4NDIxNTIyLCJ0aWQiOiIxMjA2REU5QTUwNDU1NDMxRTBGQjIwRUY3QjBERjBEMSIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.SVp2rTkIqyIMCsG09kjZeRNkIpQESRYUsBONjgZOLyA',
    'lstpge': 'AIR_REDEMPTION_PAGE',
    'dtCookie': 'v_4_srv_1_sn_BD10E291AF0B8371D9FF2BDE6F7F3942_perc_100000_ol_0_mul_1_app-3A93fb5a7425baf99b_1',
    'dtLatC': '1',
    '_gat_UA-21545627-1': '1',
    'dtPC': '1$278418656_596h41vLJGJJFBFJLIIPCCGVNJWGKJVEJGLEAAF',
    'rxvt': '1579480792416|1579478405830',
}

headers = {
    'Host': 'www.lifemiles.com',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIzMzAxMjIxOTYwMSIsInVzZXJfbmFtZSI6IjMzMDEyMjE5NjAxIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3OTU1NDcwMzI2MiwiaWF0IjoxNTc5NTU0NzAzMjYyLCJ0aWQiOiIxNzk4NjMwRkU0ODAwN0M5QUIzMTdGQTdCNjZEMTEyQSIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.I8u0vhWgxwBPd1dHa9D6pRKz7W3sMIFZdIN1K8aKIg0',
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
cookies = {}

data = '{"internationalization":{"language":"en","country":"jp","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"NRT","dest":"SFO","departingCity":"Tokyo","arrivalCity":"San Francisco","depDate":"2020-12-31","depTime":""},"filter":false,"codPromo":null,"idCoti":"1433100767","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"dTuGOG42eU0qzdNjjcAipoCWVHURLMc6"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"NRT","dest":"SFO","cabin":2}]}'
data = '{"internationalization":{"language":"en","country":"usa","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"NRT","dest":"SFO","depDate":"2020-12-31","depTime":""},"filter":false,"codPromo":null,"idCoti":"1433100767","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"dTuGOG42eU0qzdNjjcAipoCWVHURLMc6"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US"}'
response = requests.post('https://www.lifemiles.com/lifemiles/air-redemption-flight', headers=headers, cookies=cookies, data=data)

print response.content