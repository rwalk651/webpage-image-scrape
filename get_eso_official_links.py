"""Get wallpaper urls from Elder Scrolls Online official site"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import *
import time

driver = webdriver.Firefox()


def get_image_urls(sleep_between_interactions: float = 5):

    def scroll_to_end(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleep_between_interactions)

    # url for desired site
    url = 'https://www.elderscrollsonline.com/en-us/media/category/wallpapers/'

    # load the page
    driver.get(url)

    image_urls = set()
    # fetch 5 urls at a time, program does not remember place
    link_max = 5
    image_count = 0
    results_start = 0
    while image_count < link_max:
        scroll_to_end(driver)

        # get image thumbnail results
        thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'img.img-responsive')
        number_results = len(thumbnail_results)

        print(f'Found: {number_results} results. Extracting links from {results_start}:{number_results}.')

        for img in thumbnail_results[results_start:number_results]:

            try:
                img.click()
                time.sleep(sleep_between_interactions)


            # extract image urls
            if img.get_attribute('src') and 'http' in img.get_attribute('src'):
                image_urls.add(img.get_attribute('src'))
                print(img.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_urls:
                print(f'Found {len(image_urls)} image links, done.')
                break

        else:
            print('Found: ', len(image_urls), ' image links, looking for more.')
            time.sleep(30)
            return
            load_more = driver.find_elements(By.CSS_SELECTOR, '.CwMIr')
            if load_more:
                driver.execute_script('document.querySelector(".CwMIr").click();')

        # move the result startpoint down
        results_start = len(image_results)

    return image_urls

