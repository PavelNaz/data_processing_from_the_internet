from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mvideo_db = db.mvideo

options = Options()
options.add_argument('start-maximized')

chromedriver_file = 'C:\webdrivers\chromedriver.exe'

driver = webdriver.Chrome(chromedriver_file, options=options)
driver.get('https://mvideo.ru/')

section = driver.find_element_by_xpath(
    "//div/h2[@class = 'u-mb-0 u-ml-xs-20 u-hidden-phone gallery-layout__title u-font-normal']")
actions = ActionChains(driver)
actions.move_to_element(section)
actions.perform()

goods = driver.find_elements_by_xpath("//ul[contains(@data-init-param, '\"title\":\"Хиты продаж\"')]/li")
goods_count = len(goods)

goods_data = []

for good in goods:
    info = good.find_element_by_class_name('sel-product-tile-title').get_attribute('data-product-info')
    info = json.loads(info)
    info['productPriceLocal'] = float(info['productPriceLocal'])
    info['link'] = 'https://www.mvideo.ru/products/' + info['productId']
    goods_data.append(info)

driver.close()

for good in goods_data:
    mvideo_db.update_one({'_id': good['productId']}, {
        '$set': {'_id': good['productId'], 'Location': good['Location'], 'eventPosition': good['eventPosition'],
                 'productCategoryId': good['productCategoryId'], 'productCategoryName': good['productCategoryName'],
                 'productGroupId': good['productCategoryName'], 'productName': good['productName'],
                 'productPriceLocal': good['productPriceLocal'], 'productVendorName': good['productVendorName'],
                 'link': good['link']}}, upsert=True)