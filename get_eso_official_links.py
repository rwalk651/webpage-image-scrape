"""Get wallpaper urls from Elder Scrolls Online official site"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import *
import time


def get_image_urls(sleep_between_interactions: float = 5):
    driver = webdriver.Firefox()

    def scroll_to_end(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleep_between_interactions)

    # url for desired site
    url = 'https://www.elderscrollsonline.com/en-us/media/category/wallpapers/'

    # load the page
    driver.get(url)
    time.sleep(sleep_between_interactions)

    if url != driver.current_url:
        mon = driver.find_element(By.ID, 'month')
        mon.send_keys('01')
        time.sleep(1)

        day = driver.find_element(By.ID, 'day')
        day.send_keys('01')
        time.sleep(1)

        year = driver.find_element(By.ID, 'year')
        year.send_keys('1980')
        time.sleep(1)

    image_urls = set()
    # fetch 5 urls at a time, program does not remember place
    link_max = 2
    image_count = 0
    results_start = 0
    while image_count < link_max:
        scroll_to_end(driver)

        # get image thumbnail results
        thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'img.img-responsive')
        number_results = len(thumbnail_results)

        print(f'Found: {number_results} results. Extracting links from {results_start}:{number_results}.')

        for thumb in thumbnail_results[results_start:number_results]:

            try:
                thumb.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            images = driver.find_elements(By.XPATH, '// a[contains(text(), "1920x1080")]')

            for img in images:
                # extract image urls
                if img.get_attribute('href') and 'http' in img.get_attribute('href'):
                    image_urls.add(img.get_attribute('href'))
                    print(img.get_attribute('href'))

            image_count = len(image_urls)

            if len(image_urls) >= link_max:
                print(f'Found {len(image_urls)} image links, done.')
                break

        else:
            print('Found: ', len(image_urls), ' image links, looking for more.')
            time.sleep(30)
            return
            # load_more = driver.find_elements(By.CSS_SELECTOR, '.CwMIr')
            # if load_more:
            # driver.execute_script('document.querySelector(".CwMIr").click();')

        # move the result start point down
        results_start = len(thumbnail_results)

    return image_urls


if __name__ == '__main__':
    get_image_urls()
