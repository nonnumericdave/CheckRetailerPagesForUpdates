import check_pages_for_updates
import discord_webhook
import os
import random
import selenium.webdriver
import sys
import time

pages = [
    # Amazon
    check_pages_for_updates.Page(
        'Amazon',
        'https://www.amazon.com/gp/product/B0883NZC43', 
        [
            '//title'
        ], 
        2.0),

    # Newegg
    check_pages_for_updates.Page(
        'Newegg',
        'https://www.newegg.com/intel-core-i9-10900k-core-i9-10th-gen/p/N82E16819118122', 
        [
            '//*[@id="landingpage-cart"]/div/div/button/span'
        ], 
        2.0),

    # Best Buy
    check_pages_for_updates.Page(
        'Best Buy',
        'https://www.bestbuy.com/site/searchpage.jsp?st=10900k', 
        [
            '//*[@id="search-header-1"]/div/div/div[2]'
        ], 
        2.0),

    # B&H Photo
    check_pages_for_updates.Page(
        'B&H Photo',
        'https://www.bhphotovideo.com/c/product/1558668-REG/intel_bx8070110900k_core_i9_10900k_processor_20m.html', 
        [
            '//*[@id="bh-app"]/section/div/div[1]/div[4]/div/div[2]/div/div/div[5]/div[1]/div[1]/div/button'
        ], 
        2.0)
]

chrome_webdriver_path = '/Users/username/ChromeWebdriver/chromedriver'

inter_page_delay_range = range(1, 10, 1)

primer_urls = [
    'http://www.foxnews.com',
    'http://www.cnn.com',
    'http://www.msnbc.com',
    'http://www.huffpost.com/',
    'http://www.usatoday.com/',
    'http://www.reuters.com/',
    'http://news.yahoo.com/'
]

say_message = 'Page has Updates'
say_message_repeat_count = 5

discord_webhook_url = 'https://discordapp.com/api/webhooks/user_webhook_identifier'

discord_webhook_retry_count = 10

def get_callback(page, content_datetime, content_list):
    content_datetime_string = content_datetime.strftime('%c')

    print(f'ContentGet: {content_datetime_string} : {page.url}')

    for xpath, content in zip(page.xpath_list, content_list):
        print(f'    Xpath: {xpath}')
        print(f'    Content: {str(content).strip()}')

        print('')

def update_callback(page, content_datetime, xpath, cached_content, content):
    content_datetime_string = content_datetime.strftime('%c')

    print(f'ContentUpdate: {content_datetime_string} : {page.url}')

    print(f'    Xpath: {xpath}')
    print(f'    CachedContent: {str(cached_content).strip()}')
    print(f'    Content: {str(content).strip()}')

    webhook = discord_webhook.DiscordWebhook(url = discord_webhook_url)

    embed = discord_webhook.DiscordEmbed(title = page.name, url = page.url)
    embed.add_embed_field(name = 'Time', value = content_datetime_string)
    webhook.add_embed(embed)

    for _ in range(discord_webhook_retry_count):
        try:
            response = webhook.execute()
            if response.status_code in [200, 204]:
                print(f'    DiscordWebhookSuccess: {response.status_code}')
                break
            else:
                print(f'    DiscordWebhookFailure')
        except:
            exception = sys.exc_info()[0]
            print(f'    DiscordWebhookException: {exception}')
    
        time.sleep(random.choice(inter_page_delay_range))

    for _ in range(say_message_repeat_count):
        os.system(f'say "{say_message}"')

    print('')

check_pages_for_updates.check_pages_for_updates(
    pages,
    lambda: selenium.webdriver.Chrome(executable_path=chrome_webdriver_path),
    inter_page_delay_range,
    get_callback,
    update_callback,
    primer_urls)
