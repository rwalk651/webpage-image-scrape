"""Get wallpaper urls from Elder Scrolls Online official site"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        button = driver.find_element(By.CSS_SELECTOR, 'button.btn-gate')
        button.click()

    image_urls = set()
    # fetch 2 urls at a time, program does not remember place
    link_max = 2
    image_count = 0
    results_start = 0
    while image_count < link_max:
        scroll_to_end(driver)

        # get image thumbnail results
        # thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'img[class="img-responsive"]')
        thumbnail_results = driver.find_elements(By.CSS_SELECTOR, 'img.img-responsive')
        number_results = len(thumbnail_results)

        print(f'Found: {number_results} results. Extracting links from {results_start}:{number_results}.')

        for thumb in thumbnail_results:

            try:
                WebDriverWait(driver, sleep_between_interactions).until(EC.element_to_be_clickable(thumb)).click()
                time.sleep(sleep_between_interactions)
            except Exception:
                print('unable to click')
                time.sleep(sleep_between_interactions)
                break

            # images = driver.find_elements(By.XPATH, '//a[contains(text(), "1920x1080")]')
            # images = driver.find_elements(By.CSS_SELECTOR, 'a.gl-link-checked')
            if driver.find_element(By.LINK_TEXT, '1920x1080'):
                images = driver.find_elements(By.LINK_TEXT, '1920x1080')
            elif driver.find_element(By.PARTIAL_LINK_TEXT, '1920'):
                images = driver.find_elements(By.PARTIAL_LINK_TEXT, '1920')
            else:
                print('No Element')
                break

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
