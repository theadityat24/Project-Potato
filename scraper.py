from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
from fake_useragent import UserAgent
user_agent = UserAgent()


url = 'https://dining.purdue.edu/menus/Earhart/2024/1/21'

html = requests.get(url, headers={
    'User-Agent': user_agent.chrome,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer':  'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
})
soup = BeautifulSoup(html.text, 'html.parser')