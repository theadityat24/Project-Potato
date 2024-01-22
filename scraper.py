from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

service = webdriver.ChromeService(executable_path=r'C:\Program Files\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = 'https://dining.purdue.edu/menus/Earhart/2024/1/21'

driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'meal'))
)


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')


