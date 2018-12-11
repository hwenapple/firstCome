import requests
import browsercookie
cj = browsercookie.chrome()
for cookie in cj:
	if 'ffp.hnair.com' in cookie.domain:
		dic = {cookie.name, cookie.value}
		print dic
# r = requests.get('http://m.alaskaair.com', cookies=cj)
# print r.content
# print r.status_code