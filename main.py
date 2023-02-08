
# Importing relevant info
import pyautogui
import time
import pandas as pd
import lxml
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from openpyxl.workbook import Workbook
from selenium.common.exceptions import NoSuchElementException

# URL for Audi ads
url = 'https://www.autotrader.co.uk/car-search?postcode=cv227xq&make=Volvo&model=V40&include-delivery-option=on&advertising-location=at_cars&page='
car_list = []
ids = []

# loading google chrom and heading over to url then wait 5 seconds
driver = webdriver.Chrome()
ads = driver.find_elements(By.CLASS_NAME,'product-card__inner')
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)


def get_pages():
    pages_ls = driver.find_element(By.CLASS_NAME, 'paginationMini__count')
    pages_txt = pages_ls.text
    pages_lst = pages_txt.split()
    return int(pages_lst[3])


# custom funtion to get elements from web page and save as CSV
def get_ads():
    for page in range(1, get_pages()+1):
        page_url = url + str(page)
        driver.get(page_url)
        elements = driver.find_elements(By.CSS_SELECTOR, ".search-page__result")
        ids = []
        for element in elements:
            ids.append(element.get_attribute("id"))
        ads = driver.find_elements(By.CLASS_NAME, 'product-card__inner')
        for i in range(len(ids)-1): # excluded first and last advertisements on each page
            price = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[1]/div/div'.format(ids[i])).text
            make_model = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/h3'.format(ids[i])).text
            trim = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/p[1]'.format(ids[i])).text
            year = driver.find_element(By.XPATH,'.//*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[1]'.format(ids[i])).text
            body = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[2]'.format(ids[i])).text
            mileage = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[3]'.format(ids[i])).text
            engine_size = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[4]'.format(ids[i])).text
            horsepower = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[5]'.format(ids[i])).text
            try:
                fuel_type = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[1]/section[2]/ul/li[7]'.format(ids[i])).text
            except NoSuchElementException:
                fuel_type = ''
            try:
                dlrship = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[2]/div[1]/div/h3'.format(ids[i])).text
            except NoSuchElementException:
                dlrship = ''
            try:
                location = driver.find_element(By.XPATH, './/*[@id="{}"]/article/div/div/div[2]/div[1]/ul/li[2]/span'.format(ids[i])).text
            except NoSuchElementException:
                location = ''

            car_list.append([make_model, trim, year, mileage, body, engine_size, horsepower,fuel_type,
                             price, dlrship, location])
    df = pd.DataFrame(car_list)
    df.to_csv('test.csv', index=False)
get_ads()