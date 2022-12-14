# Refresh on Python with a new little project

"""
This program will scrape a webpage for images using a search term and download them.
"""

import get_eso_official_links as eso
import get_unsplash_links as splash
import uesp
from download_images import *
from bs4 import BeautifulSoup
from selenium import webdriver as driver
from selenium.webdriver.common.by import By
from pathlib import Path


choice = int(input('1 for ESO, 2 for UESP, 3 for Unsplash: '))


def main(website):

    if website == 1:
        urls_set = eso.main()
        elder_scrolls = 'eso_wallpaper'
        for index, url in enumerate(urls_set):
            download_images(elder_scrolls, url, index)

    elif website == 2:
        urls_set = uesp.main()
        elder_scrolls = 'uesp_wallpaper'
        for index, url in enumerate(urls_set):
            download_images(elder_scrolls, url, index)

    else:
        urls_set = splash.main()
        unsplash = 'unsplash'
        for index, url in enumerate(urls_set):
            download_images(unsplash, url, index)


main(choice)

