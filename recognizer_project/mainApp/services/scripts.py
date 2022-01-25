import json

from loguru import logger
import dnstwist_fixed
import requests
from ritetag import RiteTagApi
import asyncio
import pyppeteer  # $ pip install pyppeteer
from PIL import Image
from scipy.cluster.vq import whiten
from scipy.cluster.vq import kmeans
import matplotlib.image as img
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# https://github.com/melpnz/rblp/tree/master/horizontal%20(fit)


# https://moluch.ru/archive/318/72550/

def url_generator(domain):
    try:
        logger.info(f'processing {domain}')
        data = dnstwist_fixed.main(registered=True, domain=domain, format=list, ssdeep=True)
        # logger.info(data)
    except Exception as e:
        logger.error(e)
    else:
        return data


#RiteKIt api
def get_logo(domain):
    access_token = '33e0103d166d2fb99b676a7bc2af16cfe9442974e9f1'
    client = RiteTagApi(access_token)
    logo = client.company_logo(domain, True)
    colors = client.brand_colors(domain)
    return logo, colors


def get_logo_clearbit(domain):
    # https://blog.api.rakuten.net/top-5-logo-apis/
    try:
        url = f'https://logo.clearbit.com/{domain}?size=300'
        img_data = requests.get(url).content
        with open(f'{domain}.jpg', 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        logger.error(str(e))
        return 'picture not downloaded'
    else:
        return 'picture downloaded'


def get_screenshot_site(domain):
    try:
        DRIVER = 'chrome/chromedriver'
        driver = webdriver.Chrome(DRIVER)
        driver.get(f'https://www.{domain}')
        driver.save_screenshot(f'{domain}.png')
        driver.quit()
    except Exception as e:
        logger.error(str(e))
    else:
        logger.info('Screenshot saved')


# def get_screenshot_site(domain):
#     try:
#         async def main():
#             browser = await pyppeteer.launch()
#             page = await browser.newPage()
#             await page.goto(f"https://{domain}/")
#             await page.setViewport(dict(width=1000, height=800))
#             await page.screenshot(path=f'{domain}.jpg', fullPage=False)
#             await browser.close()
#
#         asyncio.get_event_loop().run_until_complete(main())
#     except Exception as e:
#         logger.error(f'failed: {str(e)}')
#     else:
#         logger.info('success')


# # https://docs.brandfetch.com/
# # https://www.klazify.com/category#docs


def get_main_color(file):
    # https://www.geeksforgeeks.org/extract-dominant-colors-of-an-image-using-python/
    # img = Image.open(file).convert("L")
    # colors = img.getcolors(256) #put a higher value if there are many colors in your image
    # max_occurence, most_present = 0, 0
    image = img.imread(file)
    try:
        r = []
        g = []
        b = []
        for row in image:
            for temp_r, temp_g, temp_b in row:
                r.append(temp_r)
                g.append(temp_g)
                b.append(temp_b)

        batman_df = pd.DataFrame({'red': r,
                                  'green': g,
                                  'blue': b})

        batman_df['scaled_color_red'] = whiten(batman_df['red'])
        batman_df['scaled_color_blue'] = whiten(batman_df['blue'])
        batman_df['scaled_color_green'] = whiten(batman_df['green'])

        cluster_centers, _ = kmeans(batman_df[['scaled_color_red',
                                               'scaled_color_blue',
                                               'scaled_color_green']], 3)

        dominant_colors = []

        red_std, green_std, blue_std = batman_df[['red',
                                                  'green',
                                                  'blue']].std()

        for cluster_center in cluster_centers:
            red_scaled, green_scaled, blue_scaled = cluster_center
            dominant_colors.append((
                red_scaled * red_std / 255,
                green_scaled * green_std / 255,
                blue_scaled * blue_std / 255
            ))
        logger.info(dominant_colors)
        # for color in dominant_colors:
        #     color = tuple([int(i) for i in color])
        #     color_block = Image.new(mode="RGB", size=(100, 100), color=(52.1804984096743, 52.57110764851953, 53.14699427890356))
        #     color_block.show()

        # plt.imshow([dominant_colors])
        # # plt.show()
        # for i in range(len(dominant_colors)):
        #     plt.savefig(f"color{i}.png")
        #

        return dominant_colors
    except Exception as e:
        raise Exception(str(e))

# def check_reputation(url):


def phish_check():
    # api_key = '9kzw52syuiwj60j9b1s104uddiqra9yg7sif6a6b22j50qffphrsl9mwtxc3c358'
    body = { "apiKey": "1f207653ec034ab9f04fbdd8e09fa7879205b4c85addeaa299da326167cc00a1",
             "urlInfo": {
                 "url": "http://webidlogin101997.5gbfree.com/"
             }
           }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url=f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}',
                         data=json.dumps(body), headers=headers)
    logger.info(resp.status_code)
    logger.info(resp.text)


def urlscan():
    api_key = 'e276aca8-85b2-4152-963a-7a25181b2be3'
    body = {"apiKey": "1f207653ec034ab9f04fbdd8e09fa7879205b4c85addeaa299da326167cc00a1",
            "urlInfo": {
                "url": "http://webidlogin101997.5gbfree.com/"
            }
            }
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url=f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}',
                         data=json.dumps(body), headers=headers)
    logger.info(resp.status_code)
    logger.info(resp.text)





if __name__ == '__main__':
    # save_active_urls()
    # d = url_generator('http://www.sberbanku.ru')
    # logger.info(d)
    # print(get_logo_clearbit('psbank.ru'))
    get_screenshot_site('sberbank.ru')
    # print(get_logo('psbank.ru'))
    # check_reputation('http://sberbank-online-skachat.asvas.ru/')