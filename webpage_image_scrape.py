# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import requests
import pandas as pd
import get_eso_official_links as eso
import get_unsplash_links as splash
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


choice = int(input('1 for ESO, 2 for Unsplash: '))


def main(website):
    if website == 1:
        eso.get_image_urls()
    else:
        splash.main()


main(choice)

