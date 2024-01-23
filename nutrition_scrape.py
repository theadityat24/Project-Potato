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

food_df = pd.read_csv('food_items.csv')

nutrition_urls = list(food_df['url'])
names = list(food_df['name'])



calories_list = {}
ingredients_list = {}
serving_size_list = {}

i = 0

for name, url_dir in list(zip(names, nutrition_urls)):
    print(f'{i} {name}')

    url = f'https://dining.purdue.edu{url_dir}'

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'item-widget-name'))
    )

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    if not soup:
        print(f'    Not found')
        continue

    nutrition_element = soup.find(class_='item-widget')

    if nutrition_element == None:
        print(f'    Not found')
        continue

    ingredients_element = nutrition_element.find(class_='nutrition-ingredient-list')

    # Check if nutrition information isn't available
    if ingredients_element == None:
        print(f'    Not found')
        continue
    
    ingredients_list[name] = ingredients_element.text

    serving_size = nutrition_element.find(class_='nutrition-feature-servingSize-quantity').text
    serving_size_list[name] = serving_size

    calories = int(nutrition_element.find(class_='nutrition-feature-calories-quantity').text)
    calories_list[name] = calories

    nutrition_table = {}

    nutrition_rows = nutrition_element.find(class_='nutrition-table').find_all(class_='nutrition-table-row')
    for row in nutrition_rows:
        label = row.find(class_='table-row-label').text

        value_element = row.find(class_='table-row-labelValue')
        value = None
        if value_element != None:
            value = value_element.text
            # for calcium and iron, there aren't any values listed

        # TODO: what do we do about daily value percentage?

        nutrition_table[label] = value

    i += 1

driver.close()

food_df = food_df.merge(
    pd.DataFrame({'name': calories_list.keys(), 'calories': calories_list.values()}),
    on='name'
).merge(
    pd.DataFrame({'name': serving_size_list.keys(), 'serving_size': serving_size_list.values()}),
    on='name'
).merge(
    pd.DataFrame({'name': ingredients_list.keys(), 'ingredients': ingredients_list.values()}),
    on='name'
)

food_df.to_csv('food_items.csv')