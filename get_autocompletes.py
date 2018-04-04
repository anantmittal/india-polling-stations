from selenium import webdriver

import os.path
import os
import random
import sys
import time
from bs4 import BeautifulSoup
import re

from selenium.webdriver import ActionChains

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.phantomjs.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from random import randint

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

import os

DELAY = 0.5

webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US,en;q=0.8'
webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = \
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)

driver.set_window_size(1280, 720)


def check_exists_by_class(cls):
    try:
        driver.find_element_by_class_name(cls)
    except NoSuchElementException:
        return False
    return True


def main():
    driver.get('http://psleci.nic.in/Default.aspx')

    state_select = Select(driver.find_element_by_name('ddlState'))
    number_of_state = len(state_select.options)
    for l in range(1, number_of_state):
        state_select = Select(driver.find_element_by_name('ddlState'))
        state = state_select.options[l]
        state_text = state.text
        print(state_text)
        state_select.select_by_visible_text(state.text)
        time.sleep(10)
        district_select = Select(driver.find_element_by_name('ddlDistrict'))
        number_of_district = len(district_select.options)
        for k in range(1, number_of_district):
            district_select = Select(driver.find_element_by_name('ddlDistrict'))
            district = district_select.options[k]
            district_text = district.text
            print("\t" + district_text)
            district_select.select_by_visible_text(district.text)
            time.sleep(10)
            ac_select = Select(driver.find_element_by_name('ddlAC'))
            number_of_ac = len(ac_select.options)
            for j in range(4, number_of_ac):
                ac_select = Select(driver.find_element_by_name('ddlAC'))
                ac = ac_select.options[j]
                ac_text = ac.text
                print("\t\t" + ac_text)
                ac_select.select_by_visible_text(ac_text)
                os.makedirs("./" + state_text + "/" + district_text + "/" + ac_text)
                time.sleep(10)

                #ps_select = Select(driver.find_element_by_name('ddlPS'))
                driver.find_element_by_id("ImageButton1").click()
                time.sleep(10)
                number_of_ps = driver.execute_script("return markers.markers.length")
                print("\t\t\t" + str(number_of_ps))
                for i in range(0, number_of_ps):
                    print("\t\t\t\t" + str(i))
                    driver.execute_script("google.maps.event.trigger(markers.getValue(" + str(i) + "), 'click');")
                    time.sleep(1)
                    popup_text = driver.execute_script(
                        "return document.getElementsByClassName('gm-style-iw')[0].innerText")
                    file = open("./" + state_text + "/" + district_text + "/" + ac_text + "/" + str(i) + ".txt", "w")
                    file.write(popup_text)
                    file.close()
    try:
        driver.close()
        driver.quit()
    except BaseException as e:
        print(repr(e))  # YOLO


if __name__ == "__main__":
    main()
