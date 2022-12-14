"""Get wallpaper urls from The Unofficial Elder Scrolls Pages (uesp) site"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

sleep_between_interactions: int = 1
webpage_delay = 10  # seconds


def main():
    driver = webdriver.Firefox()

    # url for desired site
    url = 'https://en.uesp.net/wiki/Online:Loading_Screens'

    # load the page
    driver.get(url)
    driver_wait(driver)

    # get image thumbnail results
    thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'a.image')
    number_results = len(thumbnail_results)
    print(f'Found: {number_results} results.')

    # ask how many links to grab
    link_max = link_amount()

    # construct url collection
    results_start = 0
    img_urls = get_img_urls(link_max, number_results, thumbnail_results, results_start, driver)

    # ask user to continue
    results_start = len(img_urls)
    urls_set = add_more_urls(img_urls, number_results, thumbnail_results, results_start, driver)

    return urls_set


def add_more_urls(urls, num_results, thumb_results, results_start, wd):
    answer = None
    while answer not in ('yes', 'no'):
        answer = input('Save more thumbnails? Yes or No ')
        if answer.lower() == 'yes':
            link_max = link_amount()
            expanded_urls = urls.union(
                get_img_urls(link_max, num_results, thumb_results, results_start, wd))
            return expanded_urls
        elif answer.lower() == 'no':
            return urls
        else:
            print('Please enter yes or no')


def get_img_urls(links, num_results, thumb_results, results_start, wd):
    image_urls = set()
    image_count = 0

    while image_count < links:
        scroll_to_end(wd)
        print(f'Extracting links from {results_start}:{num_results}.')

        # click thumbnail and add image url to url set
        for thumb in thumb_results[results_start:num_results]:
            images = click_thumbnail(thumb, wd)
            add_img(images, image_urls)

            wd.back()
            driver_wait(wd)

            image_count = len(image_urls)
            print(image_count)

            if len(image_urls) >= links:
                print(f'Found {len(image_urls)} image links, done.')
                break

        else:
            print('Found: ', len(image_urls), ' image links, looking for more.')
            time.sleep(30)
            return

        # move the result start point down
        results_start = len(image_urls)

    return image_urls


def add_img(images, urls):
    for img in images:
        # extract image urls and add to set
        if img.get_attribute('href') and 'http' in img.get_attribute('href'):
            urls.add(img.get_attribute('href'))
            print(img.get_attribute('href'))
            return urls


def click_thumbnail(thumb, wd):
    # click thumbnail for next page
    try:
        wd.execute_script('arguments[0].click();', thumb)
        driver_wait(wd)
        images = image_src(wd)
        return images
    except Exception as e:
        print(f'unable to click - {e}')
        time.sleep(sleep_between_interactions)
        return


def image_src(wd):
    # select image source
    try:
        images = wd.find_elements(By.CSS_SELECTOR, 'a.href')
        return images
    except Exception as e:
        print(f'No Element {e}')
        return


def link_amount():
    links = int(input('How many images to save? '))
    return links


def scroll_to_end(wd):
    wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(sleep_between_interactions)


def driver_wait(wd):
    try:
        my_elem = EC.presence_of_element_located((By.ID, 'element_id'))
        WebDriverWait(wd, webpage_delay).until(my_elem)
    except TimeoutException:
        print('Timed out waiting for page to load')


if __name__ == '__main__':
    main()
