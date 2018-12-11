from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://m.alaskaair.com")
cookies_list = driver.get_cookies()
cookies_dict = {}
for cookie in cookies_list:
    cookies_dict[cookie['name']] = cookie['value']

print(cookies_dict)