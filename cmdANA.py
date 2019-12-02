import requests
from datetime import datetime
import time
cookies = {
    's_fid': '182C1EF41920CF0D-2040B5402112C255',
    'aam_uuid': '77359604772488005661242121410719017305',
    '_ga': 'GA1.3.117410607.1572902141',
    '_fbp': 'fb.2.1572902162935.1343786938',
    '__lt__cid': 'c17e5cb8-5bbc-443e-ac72-60c85c7eef3f',
    '_gcl_au': '1.1.1880874484.1572902175',
    '_gid': 'GA1.3.1093973935.1575173534',
    'last': 'OK',
    'unique': 'userId_4398608223:K:8:3:R',
    'PersonalCookie5': 'q6F+J1Nx99QEWsdDNlkBOga+pQ7A0YEBDNawFcCdENvmvx8fK5XCw6hqzIo3YxcBZ9d/7yItbng=',
    'apoHistory': 'SJC-HND,SFO-HND,NRT-SFO,NRT-SFO-SFO-NRT,SFO-NRT,SFO-NRT-NRT-SFO',
    'A_STATUS': '1',
    'PersonalCookie6': 'pEcQthFcMnzRu09LELbY4FaBnQ8lFjDfPyoDhH9dJo4tWBovFJnCj5v7TK+0pT9JbF5N9A0XPII0ycfo7XZFslGCmKru40/8Ji5aDQC8770b9kDw3p/ZCG2GrSm4VegIov8xbiwlyQLZFlvAOW3vlU+4lr4kXbL9697Ehmg7WO3RELYToo0toH10Cxk6qMf+cQ7+yDJzaTI=',
    'PersonalCookie4': 'pEcQthFcMnzRu09LELbY4GgKxhNrk90ZYr82M+N9u6X289L9RLFJIhQ8BwFcFWFx4eTFzGDJuLihv7H6T/mbvj78dAD/xUHbqQPmy9OtYVcTCEOH0HorWw==',
    'amcglobal': 'us%2Fen',
    'w_no': '1',
    'bm_sz': 'A7ABBFA7D123F98FAF464662CEF9A5BF~YAAQRQwRYFq9vnNuAQAAdZLzxwWIOx4pOoHpnrMECNU2lFxhSUfZbDIaiMTDg29kCIhdt1DdYIPT60/I8XAvJZQiR+vyXyJZjzZwi3FqGV3TzokDh8MRslGPB95zm5APWeaWcvoo0buzYWnN5HaRcSl+Hks+SvKcnS3pRc4L3izv6xidB9V62asfQGPgzwc=',
    's_fv': 'flash%20not%20detected',
    's_cc': 'true',
    '__utmc': '204229440',
    '__utmz': '204229440.1575312673.16.3.utmcsr=ana.co.jp|utmccn=(referral)|utmcmd=referral|utmcct=/en/us/',
    'srchclntkey': '8154407458ffcf7d7efb797b64b6222090db08594d4e8aa4c604a5776a4bac17',
    '__utma': '204229440.117410607.1572902141.1575312673.1575325540.17',
    '__utmt_UA-43246109-1': '1',
    'ak_bmsc': '356A4B4DE4CADD1E3EF334E843BFD0BF60110C45526A0000618FE55D248CD571~plnST34g7aSXzE7LGMhleJuFD9EvZvddOpDo5m0rH47rKozSH/bkjzk9J8P8RycoEJT6R0R7gRR48ZoM2zMteL01cW2tG4bbqYlZiz4Gm7lLYQw+w+uzT9skhTXj/ysX17oVrlUEcirIibAv5uph1B8i+yohMFkjxIhDXr/o0xpjZLsp8ps9xnWF8WPm6DId1BR693F5pNY9ZsdJKjPGEnyHYZLmfixhV8j9y+DBZTyyg4TCPfuFn2qb6JYjeu76G0',
    '_td': 'b7a31b08-fbb5-4b1b-85a3-3add1ca7d691',
    'JSESSIONID': 'NMfIuCdvLlkGqPUhwqPk2c_HaLTS4mYg3VTezFKp9WC8chFEAM52!2104324575',
    '__lt__sid': 'dbb42167-a7fd3546',
    'real': 'q6F+J1Nx99QEWsdDNlkBOghUftr3kHtmd0ZoMhNTdXf9Zho5SXG3ij6+LHcCv3H8i80svYn4HdgjYiZuq+FsS3xdcfRce/2EISEj/MF1U8s=',
    'personal': 'q6F+J1Nx99QEWsdDNlkBOsG/By2Vz/e1EEhtEdlvjhr6eDwsdUwT2e/mhwNQF/Iy8fqcAV56u4jj3es/6u/LA0ce5hAqRLIhGAs+UYhYgliVSkW+O7Ne0q69x8VUSLL6JK9kjQkOV4GzFXwkLg7yTNh85NppbGKiQte6826jvFa7L6q4PRAAs0/VomYHPT93GPPd0FtfKiDvaBlMHAmyp4+CutvIDzZyz5v6qOCo4LgADqYTPYPUeVkTb/Q4RrVqH8FjcjFRERFlB2n3TNLXDJDMDyFC+ub3iDiAPFqZRBR9qzHVtsoXQffTl+lfqU7Bd0ZoMhNTdXdsBWTc32ujdl3i0ViqMlXbwofXo/EFob+ltSrWuCWWpW5m6PkPxxYgfwbZkQ2Ug8hXjKy658OaV2DpDhvNtnibHP0uiKzW9jBZAV+WCGVEt2TZEqU82kvXuiGX0Libq7N+g7qG7Tqy7S70uD5opkACzEZkyVtwxAQyh6mEmzmILLuOztOCL9WWLONzHc10brHLSEog9RuvJsNYbByXdf3Vy9tCbNH7yMk5KRfn1BA9hTO3W37xrqznBQYTjb28r2TDIzYkfcxd93sxl8e6qwbQ5fTdZZQzfBoCiDHm5id1NXDyM3hMlPcRa2SkV3Fgc9+XH61/0C/HLOmc8WrX1JSQY+w/xlseb0XoWT46VCtZoUyPqfR7Xm6g5/n5deMcpNFyVNL++m5Vh3lhKYoVDu2lCuwJw9wed70iXVFyrZqdzfd2vT2yvte16GHCID173jMPZqgNP+P/2NoDxzni115zA8f5bfQ/hsa752MWsQC+eESA6HQo4FOaajOajHluJWYjcFNJOxC2b/WM1y6ZTpJPr5RrOZHha4i1/0ffg/Cgtwka9fi0T6UNdvdXOo4Z2085SXP9r4hBygJzMF2gQSiIEErhwe0dNuLDznXUdlryYXdWek0AU6BP3h6k+KfmKIUwfbV16Xo6PL1KYqXXcvQzrR4jdF5KQeVHl5Vu73sHXYDBK//Kizx8X1kqAt9ep+Q313Z21U8HUS/GJ9/WYpODISjmjU0IEw+W8c1SbbJtgVQy+oOKxF+shLLNZDWdf+Uutpq/fOKr0Y7gewtM7LyTQSN2ufzIW6foCv6S88GVWC/GJ9/WYpODRgaMy8j9pGGW8c1SbbJtga9+6GBAdU5QhLLNZDWdf+X9oYnIQJxXZ47gewtM7LyTQSN2ufzIW6dLCt6kC52QvC/GJ9/WYpODpgFTTrZ2Pc2W8c1SbbJtgYukSBdzYrzU2+iHL8fIeViGIhM4NAt2hx9DTD907RnY4NZy0g7XxUC13pmCSG0gx1OyabvIVawQ0WrV45ZrDG6ILqOteZWFAOlwG+asClcG3hOFVQSHYxyP3sFPK+KvkDgtWj5Xom1xwPrhqDDOkMz/QwKvThLkAEeKyD6f+9H0xe4HXGnwihP2AYglgPdzMKr1RFX5ztN8CybvMsf01FYU2oRSXYSni9s58UbuJPrk2RWKqWMf1T2y6JF47MgvTHYYGVPrqzuD',
    'mbox': 'PC#1572902135105-235921.30_19#1609021734|session#1575325538281-140505#1575327594',
    'utag_main': 'v_id:016e384607a60002c3eea6e50a2003078001c07000838$_sn:17$_ss:0$_st:1575327533890$dc_visit:17$ses_id:1575325540028%3Bexp-session$_pn:10%3Bexp-session$dc_event:10%3Bexp-session$dc_region:us-east-1%3Bexp-session',
    '__utmb': '204229440.10.10.1575325540',
    's_sq': 'anaglobal%3D%2526c.%2526a.%2526activitymap.%2526page%253DGLOBAL_BE_AWARD_E_A02Award%252520Search%252520Flights%252520%252528Complex%252529_P02Award%252520Availability%252520Results%252520%252528Complex%252529%2526link%253DSearch%2526region%253DsearchForm%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DGLOBAL_BE_AWARD_E_A02Award%252520Search%252520Flights%252520%252528Complex%252529_P02Award%252520Availability%252520Results%252520%252528Complex%252529%2526pidt%253D1%2526oid%253Dfunctiononclick%252528event%252529%25257BreturnAsw.LoadingWindow.open%252528%252522PROMOTION%252522%25252Cevent%252529%25257D%2526oidt%253D2%2526ot%253DSUBMIT',
    '__utmli': 'searchForm',
    'bm_sv': '9173C84AE94270B915C0B060D57D5D83~HoNNBHnas2CvQjfDePB5nOG1oauNb0j+ZG7qWNDJATTfeTxbn8JBscyI6ZftDMMLWGb08b0vA6I+ehZ6yBLofGjuLJ6zLdA+CPNFMlBkz7/tWxybvMvJdgw/Zpwpuatxnh1UqCzU/Kbf8jwg5O2yWstC6z0V9gvCW75Ha9PENgk=',
    '_abck': '0F2819697608A69CCE2100FE106309CD~-1~YAAQkxiujBNdfMduAQAAZAq8yALt4u1uL43rDVHlS9pYlFl0WzIkL2bBpLaJG37jGxOM7KUTJhQcd3JTT6hh8Hvfcqz8gfEdZKPp0/vgOBMVaX1ZgYQxg32iilScPm5pNmSsd5744LeLivxFDY0SRwe8zSbx3zH0PvPihPSlea4mjTxo1jAE2Jy3bAv4LwTXnJdfOtNgdWyHtIDrqajp+DFg0enYe0k3lDb1Xo5Cd64zGDcsSq163xdE2gqdHcSHg889ipynVXJ0OxjEy8EgkaeXjKPeVY0h2bwIKiVoj0Hi7GNYpdRVw5aL7slszMY1nh47sXK2~0~-1~-1',
}

headers = {
    'Host': 'aswbe-i.ana.co.jp',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Referer': 'https://aswbe-i.ana.co.jp/rei12g/international_asw/pages/award/search/complex/award_complex_search_result.xhtml?aswcid=1&rand=20191203072844NMfIuCdvLl&rdtk=eUfmM5dwYhWJDQ1zxuwJlRtuoZebFw6qZbJlaSZkP7c%3D',
    'Accept-Language': 'en-US,en;q=0.9',
}

params = (
    ('aswcid', '1'),
    ('rand', '20191203072956NMfIuCdvLl'),
    ('rdtk', 'eUfmM5dwYhWJDQ1zxuwJlRtuoZebFw6qZbJlaSZkP7c='),
)

while True:
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print("date and time =", dt_string)
    response = requests.get('https://aswbe-i.ana.co.jp/rei12g/international_asw/pages/award/search/complex/award_complex_search_result.xhtml', headers=headers, params=params, cookies=cookies)

    print(response.status_code)
    time.sleep(30)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://aswbe-i.ana.co.jp/rei12g/international_asw/pages/award/search/complex/award_complex_search_result.xhtml?aswcid=1&rand=20191203072956NMfIuCdvLl&rdtk=eUfmM5dwYhWJDQ1zxuwJlRtuoZebFw6qZbJlaSZkP7c%3D', headers=headers, cookies=cookies)
