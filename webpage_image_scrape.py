# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import requests
import pandas as pd
import get_image_links as gil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def search_and_download(search_term, number_images):
    res = gil.get_image_urls(search_term, number_images)


def get_user_data():
    user_search = str(input('Enter your search query: '))
    img_amount = int(input('How many images to download? '))
    search_and_download(user_search, img_amount)


get_user_data()
