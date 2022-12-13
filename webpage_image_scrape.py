# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import requests
import pandas as pd
import get_eso_official_links as eso
import get_unsplash_links as splash
from download_images import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from pathlib import Path


choice = int(input('1 for ESO, 2 for Unsplash: '))


def main(website):
    target_folder = Path('C:/Users/Perseus/Pictures/Saved Pictures/image_scrape')
    if not target_folder.exists():
        target_folder.mkdir(parents=True, exist_ok=True)

    if website == 1:
        urls_set = eso.main()
        for url in urls_set:
            download_images(target_folder, url)

    else:
        urls_set = splash.main()
        for url in urls_set:
            download_images(target_folder, url)


main(choice)

