from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('C:\webdrivers\chromedriver.exe', options=chrome_options)

driver.get('https://mail.ru/')
elem = driver.find_element_by_class_name('email-input')
elem.send_keys('pavelnaztest@mail.ru')
elem.send_keys(Keys.ENTER)

time.sleep(2)
elem = driver.find_element_by_class_name('password-input')
elem.send_keys('1994pavel')
elem.send_keys(Keys.ENTER)
time.sleep(3)


list = []

letters_href = []
page_count = 0
end_of_page = False
mail_id_list = []
last_letter = None
while end_of_page == False:
    letters = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))
    if letters[-1] != last_letter:
        for letter in letters:
            mail_id = letter.get_attribute('data-uidl-id')
            if mail_id not in mail_id_list:
                mail_id_list.append(mail_id)
                letter_href = letter.get_attribute('href')
                letters_href.append(letter_href)
        page_count += 1
        last_letter = letters[-1]
    actions = ActionChains(driver)
    actions.key_down(Keys.PAGE_DOWN)
    actions.perform()
    try:
        driver.find_element_by_class_name('list-letter-spinner')
        end_of_page = True
    except:
        end_of_page = False

driver.implicitly_wait(10)

for index, href in enumerate(letters_href):
    try:
        letter_data = {}
        driver.get(href)

        letter = driver.find_element_by_class_name('layout__letter-content')
        theme = letter.find_element_by_tag_name('h2').text
        letter_author = driver.find_element_by_class_name('letter__author')
        sender = letter_author.find_element_by_class_name('letter-contact')
        sender_email = sender.get_attribute('title')
        sender = sender.text
        letter_date = letter_author.find_element_by_class_name('letter__date').text
        letter_body = driver.find_element_by_class_name('letter-body')
        l_body = letter_body.find_elements_by_tag_name('span')
        if len(l_body) == 0:
            l_body.append(letter_body.find_element_by_tag_name('div'))
        letter_text = ''
        for i in l_body:
            t = ''
            try:
                t = i.text
            except:
                print('Fail ')
            letter_text += t

        letter_data['theme'] = theme
        letter_data['sender'] = sender
        letter_data['sender_email'] = sender_email
        letter_data['date'] = letter_date
        letter_data['text'] = letter_text
        list.append(letter_data)

    except:
        print(f'Fail')

client = MongoClient('localhost', 27017)
db = client['letters']

db.new_letters.insert_many(list)
driver.quit()