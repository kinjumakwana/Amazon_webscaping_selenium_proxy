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

def check_proxy_availability(proxy):
        try:
            response = requests.get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200 and response.json()["origin"] == proxy.split(":")[0]:
                return True
        except:
            pass
        return False
        
class amazonebot:
   
    def amazonedata(self):
        # url = "http://httpbin.org/ip"
        url = "https://www.amazon.in/"
        proxies = get_free_proxies()

        for proxy in proxies:
            print(f"Trying {proxy}")
            
            if check_proxy_availability(proxy):
                
                options = webdriver.ChromeOptions()
                options.add_argument('--proxy-server=%s' % proxy)
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()
                try:
                    driver.get(url)
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
                    print("Opened Amazon with proxy: " + proxy)
                    
                    # # Perform actions on the Amazon site here using the driver instance.
                    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
                    search_box.send_keys("Air Conditioners")
                    search_box.send_keys(Keys.RETURN)
                    # sleep(1)
                    
                    # prices = driver.find_elements(By.CLASS_NAME,"a-price-whole")
                    # for price in prices:    
                    #     print(price.text)
                    
                    # WebDriverWait(self.driver, 5)
                    products_data = []
                    products_dict = {}  
                    # product_name = []
                    # product_asin = []
                    # product_price = []
                    # product_ratings = []
                    # product_ratings_num =[]
                    # product_link = []
                    items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
                    total_items = len(items)
                    print("total_items",total_items)
                    for item in items:
                        try: 
                            name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
                            
                            data_asin = item.get_attribute("data-asin")
                            # product_asin.append(data_asin)
                            products_dict["product_name"] = name.text
                            
                            whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
                            for price in whole_price:    
                                products_dict["product_price"] = price.text
                            
                            # find a ratings box
                            ratings_box = item.find_elements(By.XPATH,'.//div[@class="a-row a-size-small"]/span')
                            if ratings_box != []:
                                ratings = ratings_box[0].get_attribute('aria-label')
                                ratings_num = ratings_box[1].get_attribute('aria-label')
                            else:
                                ratings, ratings_num = 0, 0
                            
                            products_dict["product_ratings"] = ratings  
                            products_dict["product_ratings_num"] = ratings_num  
                            
                            # find link
                            link = item.find_element(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]').get_attribute("href")
                            products_dict["product_link"] = link  
                            
                            products_data.append(products_dict)
                            print(products_data)
                            
                            df = pd.DataFrame(products_data)
                            print(df)
                            
                            print("\n")
                            df.to_csv('amazon_AC_data.csv')
                        
                        except:
                            print("Problem to load data")
                        
                        page_link = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div[22]/div/div/span/a[3]')))
                        page_link.click()
                        sleep(2)

                    driver.quit()
                    return proxy
                except:
                    print(f"Failed to load Amazon with proxy: {proxy}")
                    driver.quit()
        print("No available proxies.")
        return None
    
amazonebots = amazonebot()
amazonebots.amazonedata()

