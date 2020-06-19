import dataclasses
import datetime
import random
import selenium.webdriver
import time

@dataclasses.dataclass
class Page:
    name: str
    url: str
    xpath_list: list
    load_wait_time: float

@dataclasses.dataclass
class PageUpdate:
    page: Page
    webdriver: selenium.webdriver.remote.webdriver.WebDriver
    xpath_content_list: list

def get_page_for_url(webdriver, url):
    while True:
        try:
            webdriver.get(url)
            break
        except:
            pass

def content_for_xpath(webdriver, xpath):
    try:
        return webdriver.find_element_by_xpath(xpath).get_attribute('textContent')
    except:
        return None

def check_pages_for_updates(pages, webdriver_factory, inter_page_delay_range, get_callback, update_callback, primer_urls = []):
    page_update_list = list(map(lambda page: PageUpdate(page, webdriver_factory(), list()), pages))

    for page_update in page_update_list:
        if primer_urls:
            get_page_for_url(page_update.webdriver, random.choice(primer_urls))

        get_page_for_url(page_update.webdriver, page_update.page.url)

        content_datetime = datetime.datetime.now()

        time.sleep(page_update.page.load_wait_time)
        
        page_update.xpath_content_list = list(map(lambda xpath: content_for_xpath(page_update.webdriver, xpath), page_update.page.xpath_list))

        get_callback(page_update.page, content_datetime, page_update.xpath_content_list)

    while True:
        for page_update in page_update_list:
            if primer_urls:
                get_page_for_url(page_update.webdriver, random.choice(primer_urls))

            get_page_for_url(page_update.webdriver, page_update.page.url)
        
            content_datetime = datetime.datetime.now()

            time.sleep(page_update.page.load_wait_time)

            xpath_content_list = list(map(lambda xpath: content_for_xpath(page_update.webdriver, xpath), page_update.page.xpath_list))

            get_callback(page_update.page, content_datetime, xpath_content_list)

            for xpath, cached_content, content in zip(page_update.page.xpath_list, page_update.xpath_content_list, xpath_content_list):
                if cached_content != content:
                    update_callback(page_update.page, content_datetime, xpath, cached_content, content)

            page_update.xpath_content_list = list(xpath_content_list)

            time.sleep(random.choice(inter_page_delay_range))
