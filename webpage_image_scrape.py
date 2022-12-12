# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

# test Selenium with Firefox GeckoDriver
driver = webdriver.Firefox()
driver.get('http://www.google.com')
query = driver.find_element(By.CSS_SELECTOR, '[name="q"]')
query.send_keys('Cat')
driver.quit()

