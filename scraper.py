from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

service = webdriver.ChromeService(executable_path=r'C:\Program Files\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service)

import pandas as pd


url = 'https://dining.purdue.edu/menus/Earhart/2024/1/21'

driver.get(url)

# time for the page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'meal'))
)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

driver.close()

stations = soup.find(class_='meal').find_all(class_='station')



class FoodItem:
    def __init__(self, station, name, tags=[]):
        self.station = station
        self.name = name
        self.tags = tags

    def to_dict(self):
        return {
            'station': self.station,
            'name': self.name,
            'tags': self.tags
        }
    
    def __str__(self):
        return f'{self.station}: {self.name}'

food = []

for station in stations:
    station_name = station.find(class_='station-name').text
    print(station_name)

    for item in station.find(class_='station-items').find_all('div', recursive=False):
        item_detail = item.find(class_='station-item').find(class_='station-item-details')
        item_name = item_detail.find(class_='station-item-text').text
    
        food_item = FoodItem(
            station=station_name,
            name=item_name,
        )

        item_tags_imgs = item_detail.find_all('img')
     
        tags = [img['title'] for img in item_tags_imgs]
        food_item.tags = tags

        food.append(food_item)

    





