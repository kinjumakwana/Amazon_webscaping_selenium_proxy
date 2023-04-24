from urllib import request
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.db import IntegrityError
from selenium.webdriver.common.action_chains import ActionChains
import re 
import pandas as pd
import csv

s = Service(r"D:\Kinjal\chromedriver_win32\chromedriver.exe")
def get_free_proxies():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--headless")
    # create a webdriver instance
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get("https://free-proxy-list.net/")
    # get the table rows
    rows = driver.find_elements(By.CSS_SELECTOR,"table.table-striped tbody tr")
    # print(rows)
    # to store proxies
    proxies = []
    for row in rows[1:]:
        tds = row.find_elements(By.CSS_SELECTOR,"td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
            # print(proxies)
            df = pd.DataFrame(proxies)
            df.columns = ['IP Address']
            df.to_csv('proxylist.csv')
        except IndexError:
            continue
    driver.quit()
    return proxies
    
class amazonebot:
    def amazonedata(self):
        # url = "http://httpbin.org/ip"
        url = "https://www.amazon.in/"
        proxies = get_free_proxies()

        for proxy in proxies:
            print(f"Trying {proxy}")
            options = webdriver.ChromeOptions()
            options.add_argument('--proxy-server=%s' % proxy)
            driver = webdriver.Chrome(options=options)
            driver.maximize_window()
            try:
                driver.get(url)
                sleep(5)
                # WebDriverWait(self.driver, 5)
                print("Opened Amazon with proxy: " + proxy)
                
                # # Perform actions on the Amazon site here using the driver instance.
                search_box = driver.find_element(By.ID, "twotabsearchtextbox")
                search_box.send_keys("Air Conditioners")
                search_box.send_keys(Keys.RETURN)
                sleep(1)
                
                prices = driver.find_elements(By.CLASS_NAME,"a-price-whole")
                for price in prices:    
                    # Scroll the link into view
                    self.driver.execute_script("arguments[0].scrollIntoView();", price)
                    print(price.text)
                
                # WebDriverWait(self.driver, 5)
                driver.quit()
                return proxy
            except:
                print(f"Proxy {proxy} not available.")
                driver.quit()
        print("No available proxies.")
        return None
    
amazonebots = amazonebot()
amazonebots.amazonedata()

