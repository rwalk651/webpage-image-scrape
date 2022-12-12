"""Get image urls from search query"""


from selenium import webdriver
import time


# query will be search term, max links will be the number of links the program collects
def get_image_urls(query: str, max_urls: int, driver: webdriver, sleep_between_interactions: int = 1):

    def scroll_to_end(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleep_between_interactions)

    # build url query for desired site
    search_url = 'https://unsplash.com/s/photos/{s}'

    # load the page
    driver.get(search_url.format(s=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_urls:
        scroll_to_end(driver)




