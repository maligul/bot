from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime

excel = pd.read_excel('../info.xlsx', engine='openpyxl')
print(str(excel['Where-to'][0]))
print(excel['Date-to'][0].strftime('%Y-%m-%d'))
print(int
      (excel['Adults'][0]))
print(datetime.today().strftime('%d %m %Y'))
excel.to_csv(datetime.today().strftime('%d %m %Y') + ".csv")








"""
url = 'https://www.booking.com/searchresults.tr.html?label=gen173nr-1FCAEoggI46AdIKFgEaOQBiAEBmAEouAEXyAEP2AEB6AEB-AECiAIBqAIDuALWx_yiBsACAdICJDU4YzA5MjJjLTA5MjctNGY2NS04ZDI2LWQ0MWZiYWU4ZTVkMNgCBeACAQ&aid=304142&ss=New+York%2C+New+York+State%2C+ABD&efdco=1&lang=tr&dest_id=20088325&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=tr&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=06a0286ba45d010b&ac_meta=GhAwNmEwMjg2YmE0NWQwMTBiIAAoATICdHI6CE5ldyBZb3JrQABKAFAA&checkin=2023-06-10&checkout=2023-06-11&group_adults=1&no_rooms=1&group_children=0&sb_travel_purpose=leisure&nflt=class%3D3%3Bclass%3D4&order=price'
driver = webdriver.Firefox()
driver.get(url)

table = driver.find_element(By.ID, "search_results_table")
points = table.find_elements(By.CSS_SELECTOR,".a826ba81c4.fe821aea6c.fa2f36ad22.afd256fc79.d08f526e0d.ed11e24d01.ef9845d4b3.da89aeb942")
for point in points:
    try:
        value= point.find_element(By.CSS_SELECTOR, 'div[aria-label^="Puanı"]').get_attribute('innerHTML').strip()
        print(value)
    except Exception as E:
        print('No point in ')
        pass

"""

'''

    
    
    
print(points[1].get_attribute('innerHTML'))
puan = points[1].find_element(By.CSS_SELECTOR,'div[aria-label^="Puanı"]').get_attribute('innerHTML').strip()
print(puan)
'''
