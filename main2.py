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
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
        
class amazonebot:
    def __init__(self):
        self.driver = webdriver.Chrome(service=s, options=options)
        # sleep(5)
        wait = WebDriverWait(self.driver, 5)
    
    def amazonedata(self):
        url = "https://www.amazon.in/"
        self.driver.maximize_window()
        self.driver.get(url)
        # sleep(5)
        # wait for page to load
        wait = WebDriverWait(self.driver, 10)
        
        try:
            # # Perform actions on the Amazon site here using the driver instance.
            search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
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
            ifpagination = True
            page_count = 1
            while ifpagination and page_count <= 3:
                
                items = WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
                total_items = len(items)
                print("total_items",total_items)
                for item in items:
                    products_dict = {}  
                        # # Scroll the link into view
                    self.driver.execute_script("arguments[0].scrollIntoView();", item)
                    
                    name = item.find_element(By.XPATH, './/span[@class="a-size-medium a-color-base a-text-normal"]')
                    
                    data_asin = item.get_attribute("data-asin")
                    # Amazon Standard Identification Number (ASIN)
                    products_dict["data_asin"] = data_asin
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
                    df.to_csv('amazon_AC_data2.csv')
                    sleep(1)
                    
                if page_count == 3:
                    ifpagination = False    
                
                else:
                    # next_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")))
                    next_link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.s-pagination-next")))
                    next_link.click()
                    sleep(5)
                    page_count += 1
                # page_link2 = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div[29]/div/div/span/a[1]")))
                # page_link2.click()
                # if page_link2:
                #     ifpagination = True
                
                # else:
                #     ifpagination = False        

                # page_link3 = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[1]/div/span[1]/div[1]/div[28]/div/div/span/a[2]")))
                # if page_link3:
                #     page_link3.click()
                #     ifpagination = True
                # else:
                #     ifpagination = False 
                # sleep(5)
                # if page_link3:
                #     ifpagination = True
                # else:
                #     ifpagination = False   
                
        except:
            print("No available proxies.")
            
amazonebots = amazonebot()
amazonebots.amazonedata()

