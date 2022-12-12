# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import requests
import pandas as pd
import get_unsplash_links as splash
import get_eso_official_links as eso
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


def search_and_download(search_term, number_images):
    res = splash.get_image_urls(search_term, number_images)


def get_user_data():
    user_search = str(input('Enter your search query: '))
    img_amount = int(input('How many images to download? '))
    search_and_download(user_search, img_amount)


def main(website):
    if website == 1:
        eso.get_image_urls()
    else:
        get_user_data()


choice = int(input('1 for ESO, 2 for unsplash: '))

main(choice)

