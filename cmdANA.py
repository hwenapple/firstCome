import requests
from datetime import datetime
import time

import requests

cookies = {
    'rxVisitor': '1564886709815HR09DU83P9M2V4KR9E7AUR41NC1LRJ4E',
    '_ga': 'GA1.2.128761326.1574801828',
    '_fbp': 'fb.1.1574801827940.1177769153',
    'cookiePolicyAccepted': 'true',
    'statusInfo': 'LifeMiles',
    '_gid': 'GA1.2.1646341149.1575345440',
    'defConf': '%7B%22language%22%3A%22en%22%2C%22country%22%3A%22us%22%2C%22currency%22%3A%22usd%22%7D',
    'sgn_kml': 'true',
    'JSESSIONID': '812D5D3C33C1BA77A59BEA4380C7344E',
    'dtSa': '-',
    'dra3j': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIzMzAxMjIxOTYwMSIsInVzZXJfbmFtZSI6IjMzMDEyMjE5NjAxIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3NTM1NjM3NDk5OCwiaWF0IjoxNTc1MzU2Mzc0OTk4LCJ0aWQiOiJBNkNFQUJGQUVDMzNENTA3NEI3RDQxMTUzOUUxNDA3OCIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.eXfVUz2_-E_iPF3eMN_5lJ6BzGxYPL0XQ39ZXNBVKW4',
    'userInfo': '33012219601',
    'dtLatC': '1',
    'lstpge': 'AIR_REDEMPTION_PAGE',
    'dtCookie': '4$C7899AC62FAC90A687CEDE5D7AA30ADC|93fb5a7425baf99b|1',
    'dtPC': '4$356375355_108h30vKCPMKMJPDKPTJBMBNEOPVMBKPJIGHMPO',
    'rxvt': '1575358223900|1575352914682',
}

headers = {
    'Host': 'www.lifemiles.com',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJvYXV0aDItcmVzb3VyY2UiLCJzdWIiOiIzMzAxMjIxOTYwMSIsInVzZXJfbmFtZSI6IjMzMDEyMjE5NjAxIiwic2NvcGUiOlsicmVhZCJdLCJpc3MiOiJMTSIsImV4cCI6MTU3NTM1NjM3NDk5OCwiaWF0IjoxNTc1MzU2Mzc0OTk4LCJ0aWQiOiJBNkNFQUJGQUVDMzNENTA3NEI3RDQxMTUzOUUxNDA3OCIsImNsaWVudF9pZCI6ImxtX3dlYnNpdGUiLCJjaWQiOiJsbV93ZWJzaXRlIn0.eXfVUz2_-E_iPF3eMN_5lJ6BzGxYPL0XQ39ZXNBVKW4',
    'Origin': 'https://www.lifemiles.com',
    'x-dtpc': '4$356375355_108h30vKCPMKMJPDKPTJBMBNEOPVMBKPJIGHMPO',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.lifemiles.com/air-redemption',
    'Accept-Language': 'en-US,en;q=0.9',
}

data = '{"internationalization":{"language":"en","country":"us","currency":"usd"},"currencies":[{"currency":"USD","decimal":2,"rateUsd":1}],"passengers":1,"od":{"orig":"SFO","dest":"NRT","departingCity":"San Francisco","arrivalCity":"Tokyo","depDate":"2020-11-18","depTime":""},"filter":false,"codPromo":null,"idCoti":"777790449","officeId":"","ftNum":"33012219601","discounts":[],"promotionCodes":[],"context":"D","ipAddress":"73.189.39.42","channel":"COM","cabin":"2","itinerary":"OW","odNum":1,"usdTaxValue":"0","getQuickSummary":true,"ods":"","searchType":"SSA","searchTypePrioritized":"SSA","sch":{"schHcfltrc":"NOGz0lxUJj0Brz/mcOMlBq/iMuKYRV3p"},"staticMileageRtX":null,"staticMileageRtI":null,"staticMileageRtF":null,"smpKey":null,"posCountry":"US","odAp":[{"org":"SFO","dest":"NRT","cabin":2}]}'



while True:
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print("date and time =", dt_string)
    response = requests.post('https://www.lifemiles.com/lifemiles/air-redemption-flight', headers=headers, cookies=cookies, data=data)

    print(response.status_code)
    time.sleep(30)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://aswbe-i.ana.co.jp/rei12g/international_asw/pages/award/search/complex/award_complex_search_result.xhtml?aswcid=1&rand=20191203072956NMfIuCdvLl&rdtk=eUfmM5dwYhWJDQ1zxuwJlRtuoZebFw6qZbJlaSZkP7c%3D', headers=headers, cookies=cookies)
