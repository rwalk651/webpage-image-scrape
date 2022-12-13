"""Get image urls from search query in Unsplash"""


from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def main():
    user_search = str(input('Enter your search query: '))
    img_amount = int(input('How many images to download? '))
    get_image_urls(user_search, img_amount)


# query will be search term, max links will be the number of links the program collects
def get_image_urls(query: str, max_urls: int, sleep_between_interactions: float = 3):
    driver = webdriver.Firefox()

    def scroll_to_end(wd):
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(sleep_between_interactions)

    # build url query for desired site
    search_url = f'https://unsplash.com/s/photos/{query}'

    # load the page
    driver.get(search_url)

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_urls:
        scroll_to_end(driver)

        # get image thumbnail results
        image_results = driver.find_elements(By.CSS_SELECTOR, 'img.YVj9w:not(.ht4YT)')
        number_results = len(image_results)

        print(f'Found: {number_results} search results. Extracting links from {results_start}:{number_results}.')

        for img in image_results:

            # extract image urls
            if img.get_attribute('src') and 'plus' in img.get_attribute('src'):
                continue    # avoid paid images
            else:
                img.get_attribute('src') and 'http' in img.get_attribute('src')
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


if __name__ == '__main__':
    main()
