"""
To run this you need chrome driver installed. Change the path below to your installation location.
Also, make sure to install all the libraries below.
"""

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pandas as pd
import datetime

CHROME_DRIVER_PATH = r'C:\Program Files\chromedriver-win64\chromedriver.exe'

service = webdriver.ChromeService(executable_path=CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service)

periods = ['Breakfast', 'Dinner', 'Lunch', 'Late Lunch']
dining_halls = ['Earhart', 'Ford', 'Hillenbrand', 'Wiley', 'Windsor']

today = datetime.date.today()

# dates 10 days into the future
dates = [today + datetime.timedelta(days=i) for i in range(8)]

dining_hall_items = []
food_items = []
nutrition_urls = {}

# TODO: triple loop is ugly, reformat

for dining_hall in dining_halls:
    for date in dates:
        for period in periods:
            # TODO: figure out a better way to go through valid periods
            if period == 'Late Lunch' and dining_hall in ['Earhart', 'Wiley']:
                continue
            if period == 'Breakfast' and dining_hall == 'Hillenbrand':
                period = 'Brunch'
            if period == 'Breakfast' and dining_hall == 'Windsor':
                continue

            url = f'https://dining.purdue.edu/menus/{dining_hall}/{date.year}/{date.month}/{date.day}/{period}'
            print(f'{date} {dining_hall} {period}')

            driver.get(url)

            # TODO: save time by not loading pages for invalid meal times. 

            # time for the page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'meal'))
            )

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            stations = soup.find(class_='meal').find_all(class_='station')

            for station in stations:
                station_name = station.find(class_='station-name').text

                for item in station.find(class_='station-items').find_all('div', recursive=False):
                    item_a = item.find(class_='station-item')
                    item_detail = item_a.find(class_='station-item-details')
                    item_name = item_detail.find(class_='station-item-text').text

                    item_tags_imgs = item_detail.find_all('img')
                    tags = [img['title'] for img in item_tags_imgs]
                    if item_name not in nutrition_urls:
                        nutrition_urls[item_name] = item_a['href']
                        food_items.append({
                            'name': item_name, 
                            'tags': tags,
                            'url': item_a['href']
                        })

                    dining_hall_items.append({
                        'station': station_name,
                        'dining_hall': dining_hall,
                        'date': date,
                        'name': item_name,
                        'period': period
                    })

driver.close()

food_df = pd.DataFrame(food_items)
dining_hall_df = pd.DataFrame(dining_hall_items)

food_df.to_csv('food_items.csv')
dining_hall_df.to_csv('dining_hall_items.csv')



    





