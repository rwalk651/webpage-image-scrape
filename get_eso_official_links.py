"""Get wallpaper urls from Elder Scrolls Online official site"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from download_images import *
import time

sleep_between_interactions: int = 1


def main():
    driver = webdriver.Firefox()

    # url for desired site
    url = 'https://www.elderscrollsonline.com/en-us/media/category/wallpapers/'

    # load the page
    driver.get(url)
    time.sleep(sleep_between_interactions)

    # fill input to get through age gate
    if url != driver.current_url:
        fill_age_gate(driver)

    # get image thumbnail results
    thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'a.zl-link.gl-link-checked')
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

            image_count = len(image_urls)
            print(image_count)

            if len(image_urls) >= links:
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
        results_start = len(image_urls)

    return image_urls


def add_img(images, urls):
    for img in images:
        # extract image urls and add to set
        if img.get_attribute('href') and 'http' in img.get_attribute('href'):
            urls.add(img.get_attribute('href'))
            # print(img.get_attribute('href'))
            return urls


def click_thumbnail(thumb, wd):
    # click thumbnail for pop-up
    try:
        wd.execute_script('arguments[0].click();', thumb)
        time.sleep(sleep_between_interactions)
        images = choose_size(wd)
        return images
    except Exception as e:
        print(f'unable to click - {e}')
        time.sleep(sleep_between_interactions)
        return


def choose_size(wd):
    # select image size - either 1920x1080 or 1920 by any size
    try:
        wd.find_element(By.LINK_TEXT, '1920x1080')
        images = wd.find_elements(By.LINK_TEXT, '1920x1080')
        return images
    except Exception as e:
        print(f'No Element {e}')

    try:
        wd.find_element(By.PARTIAL_LINK_TEXT, '1920')
        images = wd.find_elements(By.PARTIAL_LINK_TEXT, '1920')
        return images
    except Exception as e:
        print(f'No Element {e}')
        return


def link_amount():
    links = int(input('How many images to save? '))
    return links


def fill_age_gate(wd):
    mon = wd.find_element(By.ID, 'month')
    mon.send_keys('01')
    time.sleep(1)

    day = wd.find_element(By.ID, 'day')
    day.send_keys('01')
    time.sleep(1)

    year = wd.find_element(By.ID, 'year')
    year.send_keys('1980')
    time.sleep(1)

    button = wd.find_element(By.CSS_SELECTOR, 'button.btn-gate')
    button.click()


def scroll_to_end(wd):
    wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(sleep_between_interactions)


if __name__ == '__main__':
    main()
