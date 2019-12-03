import requests

cookies = {
    '_cls_v': 'c070be71-5483-4d37-aa3a-00e9b81ecd23',
    'FARE_DEALS_LISTING_COOKIE': 'false',
    'AKAMAI_SAA_COUNTRY_COOKIE': 'US',
    'AKAMAI_SAA_LOCALE_COOKIE': 'en_UK',
    'insUserIsNew': 'false',
    'D_SID': '73.189.39.42:a9deI5CQx8udGsOP+TMupS6nzeyTMi4As3wR8VqFVd8',
    '_gcl_au': '1.1.917426071.1572818846',
    '_ga': 'GA1.2.1209880829.1572818847',
    '_fbp': 'fb.1.1572818847400.975275267',
    '__qca': 'P0-2075696789-1572818847428',
    'insKfStatus': 'Y',
    'AKAMAI_HOME_PAGE_ACCESSED': 'true',
    'AKAMAI_SAA_AIRPORT_COOKIE': 'SIN',
    'LOGIN_POPUP_COOKIE': 'false',
    'RU_LOGIN_COOKIE': 'false',
    'SQCLOGIN_COOKIE': 'false',
    'AKAMAI_SAA_KF_TIER_COOKIE': 'K',
    'insUserLastOrigin': 'SFO',
    'insUserLastDestination': 'NRT',
    'insUserLastPointOfSale': 'US',
    'ins-product-id': 'www.singaporeair.com%2Fbooking-sfo-to-nrt',
    'AKA_A2': 'A',
    'D_ZID': 'FBF51E95-217D-3DB5-965C-11038C23F236',
    'D_ZUID': '54CAF61A-5275-3CAC-A894-5FB9E2C06F4C',
    'D_HID': '8D43961A-4277-3A71-8E16-0EE941A79376',
    'HSESSIONID': 'ioymyfFUyTD17ui_WbTt_czFCqtJ5R69FGTCrbUj.saa-home-41-g168k',
    'saadevice': 'desktop',
    'e62be4a5a17e1043370f85d6e7b65187': '9dc853bb4f1718403cf0f6e0e4b8f682',
    'rxVisitor': '1575346632556HEDUQL0AASN0BGPOVMK79DFA87SKB7OP',
    '_cls_s': '73d735bd-11eb-4f68-9362-3d6402c95204:1',
    'cookieStateSet': 'hybridState',
    'hvsc': 'true',
    'JSESSIONID': 'gkLJ-fznhsQBy_iv06uHpk9JSoGlZzDhGkdSevhm4lRjgTxZfX1H!502597937',
    'AKAMAI_SAA_DEVICE_COOKIE': 'desktop',
    'AWSELB': '6B2711F916135C6D194DDDD5C58287B7F754C0C98418C83B34583C6B416ABCC1EAA7150783026A9CF44BFCBBE129D68858D39971CA7828B720452F191B9793B1F7C67B463ECD88EF7DA2DE977C0687B643D6120BEF7F1F927CA6313BEC91B8F1147CDEE0A6',
    'insUserLastSeenAsDay': '1',
    'ins-gaSSId': 'ea51e1e4-4e22-aeb1-e8f3-d6fbe1e239d1_1575346634',
    'LOGIN_COOKIE': 'true',
    'VSUUID': '36643b7f45e2979ef941373a99f6f1597c6375199bf0e1d2ab112685087524ea.saa-home-41-g168k.1575346641309',
    'kfMagic': 'K_86d6d1240c2ef1e3b46b2e424506c256',
    '_gid': 'GA1.2.260559233.1575346664',
    'scs': '1',
    'current-currency': '%2B',
    'gtk': 'exp=1575346786~acl=%2f*~hmac=5d995dbc5a4693aa750fa90e4d73705387b2e7f37f0828747c7d6088f22a26e5',
    'insdrSV': '38',
    'D_IID': 'B6E0317F-F6B7-3B29-8C3E-4B8ABD6D03DB',
    'D_UID': '5F4F738C-13EF-3D27-9FE9-F6C954DF7470',
    'dtLatC': '1',
    '__gtm_pageLoadTimes': '{"ORB_ChooseFlight":1575346842664}',
    '_gat_UA-17015991-1': '1',
    'dtPC': '5$346830144_105h-vCMLIBKPODMNDKLCOPKHMHFAIMKHBECAK',
    'rxvt': '1575348701106|1575346632559',
    'dtSa': 'true%7CC%7C-1%7Cupdate%7C-%7C1575346901810%7C346830144_105%7Chttps%3A%2F%2Fwww.singaporeair.com%2Fbooking-flow.form%3Fexecution%3De1s4%7CSelect%20Flight%20-%20Redemption%20Booking%7C1575346901108%7C',
    'RT': 'dm=singaporeair.com&si=787a92cd-de13-4cf9-a583-3f9070730cbe&ss=1575346629897&sl=7&tt=93552&obo=0&sh=1575346831120%3D7%3A0%3A93552%2C1575346786728%3D6%3A0%3A73369%2C1575346754693%3D5%3A0%3A65572%2C1575346695763%3D4%3A0%3A37106%2C1575346648497%3D3%3A0%3A12158&bcn=%2F%2F173e2545.akstat.io%2F&nu=&cl=1575346901935&r=https%3A%2F%2Fwww.singaporeair.com%2Fbooking-flow.form%3F238daf9aa12fa1527318b4247a44dde7&ul=1575346901982',
    'dtCookie': '5$3ADE2FA80F862B79B93B162EA264373F|7bacf3aecd29efdf|1',
    'AWSALB': '0HYdOvPUvHcYDenE60QRH5BDqPRqy0rePAZWIfKfVAUaQa97E2A0uMoKZTfmQegPUPgzSXAI1KFHNXW0gT6ozIhKOVoCUZTVN42c0G6WDPmhi+u8qd28iF4paZAe',
    'RSS': 'IN:1~O:SFO~D:NRT~R:0~CC:J~A:1~C:0~I:0~DD:18~DDS:18/11/2020~DM:112020~RD:~RDS:~RM:null~PT:ORB~TT:One Way~#IN:2~O:SFO~D:NRT~R:0~CC:J~A:1~C:0~I:0~DD:19~DDS:19/11/2020~DM:112020~RD:~RDS:~RM:null~PT:ORB~TT:One Way~#IN:3~O:SFO~D:NRT~R:0~CC:F~A:1~C:0~I:0~DD:17~DDS:17/11/2020~DM:112020~RD:~RDS:~RM:null~PT:ORB~TT:One Way~#IN:4~O:SFO~D:NRT~R:0~CC:F~A:1~C:0~I:0~DD:18~DDS:18/10/2020~DM:102020~RD:~RDS:~RM:null~PT:ORB~TT:One Way~#IN:5~O:SFO~D:NRT~R:0~CC:F~A:1~C:0~I:0~DD:15~DDS:15/10/2020~DM:102020~RD:~RDS:~RM:null~PT:ORB~TT:One Way~#',
}

headers = {
    'Host': 'www.singaporeair.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'referer': 'https://www.singaporeair.com/booking-flow.form?execution=e1s4',
    'accept-language': 'en-US,en;q=0.9',
}

params = (
    ('execution', 'e1s5'),
)

response = requests.get('https://www.singaporeair.com/booking-flow.form', headers=headers, params=params, cookies=cookies)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.singaporeair.com/booking-flow.form?execution=e1s5', headers=headers, cookies=cookies)
