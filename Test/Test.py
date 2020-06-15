from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep

# driver = webdriver.Ie()
# driver.maximize_window()
# driver.get("https://hotels.ctrip.com/hotel/16100.html")
# html = driver.execute_script("return document.documentElement.outerHTML")

# response = requests.get("https://hotels.ctrip.com/hotel/16101.html")
# soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
# hotelName = soup.select(".cn_n")
# hotelName = str(hotelName)
# hotelName = hotelName[1:-6]
# print(hotelName.find(">"), len(hotelName)-1)

# data = driver.find_element_by_class_name("comment_detail_list")
# print(data)
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Ie()
sleep(3)
driver.get("https://hotels.ctrip.com/hotel/13000.html")
wait = WebDriverWait(driver, 10)
