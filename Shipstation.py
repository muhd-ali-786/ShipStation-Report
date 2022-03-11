import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import pandas as pd
from pathlib import Path
import requests
import shutil
import math
import csv
import re
import datetime
import sys

def get_profile_path(profile):
    FF_PROFILE_PATH = os.path.join(os.environ['APPDATA'],'Mozilla', 'Firefox', 'Profiles')

    try:
        profiles = os.listdir(FF_PROFILE_PATH)
    except WindowsError:
        print("Could not find profiles directory.")
        sys.exit(1)
    try:
        for folder in profiles:
            print(folder)
            if folder.endswith(profile):
                loc = folder
    except StopIteration:
        print("Firefox profile not found.")
        sys.exit(1)
    return os.path.join(FF_PROFILE_PATH, loc)


today_date = datetime.datetime.now()

DD = datetime.timedelta(days=90)
from_date = today_date - DD

DD = datetime.timedelta(days=1)
to_date = today_date - DD


url="https://ss5.shipstation.com/#/track/shipments";
download_path_root = # Report Download Root Path Here


file_path= # Report Folder Name


prof = # Firefox Profile name i.e: abcxyz.default-release

# file_name=""
email= # Login Email
password= # Login Password


mime_types = "application/octet-stream"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
# profile.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(firefox_profile=profile)
driver.get(url)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

time.sleep(20)
try:
    try:
        driver.find_element(By.XPATH,"/html/body/div/div/form/div[1]/input").send_keys(email)
        driver.find_element(By.XPATH,"/html/body/div/div/form/div[2]/input").send_keys(password)
        driver.find_element(By.ID, "btn-login").click()
    except:
        driver.find_element(By.CSS_SELECTOR,"input[type='text']").send_keys(email)
        driver.find_element(By.CSS_SELECTOR,"input[type='password']").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='button']").click()
except:
    driver.find_element(By.CSS_SELECTOR,"#username").send_keys(email)
    driver.find_element(By.CSS_SELECTOR,"#password").send_keys(password)
    driver.find_element(By.ID, "btn-login").click()

try:

    time.sleep(20)
    # driver.find_element_by_link_text("Shipments").click()

    driver.get("https://ship5.shipstation.com/shipments/")
    time.sleep(10)

    driver.get("https://ship5.shipstation.com/shipments/")
    time.sleep(60)
    drps = driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggler")
    for drp in drps:
        if drp.text == 'Ship Date':
            drp.click()
            break
    time.sleep(5)
except:
    # driver.find_element_by_link_text("Shipments").click()

    driver.get("https://ship5.shipstation.com/shipments/")
    time.sleep(60)
    drps = driver.find_elements(By.CSS_SELECTOR, ".dropdown-toggler")
    for drp in drps:
        if drp.text == 'Ship Date':
            drp.click()
            break
    time.sleep(5)

btns = driver.find_elements(By.CSS_SELECTOR, '#dropdown-wrapper-container form button')

for btn in btns:
    if btn.text == 'Custom Range':
        btn.click()
        break
time.sleep(5)
cal1 = driver.find_elements(By.CSS_SELECTOR, '#dropdown-wrapper-container form .components-date-picker input')
cal1[0].send_keys(Keys.CONTROL+'a')
time.sleep(1)
cal1[0].send_keys(from_date.strftime('%m/%d/%Y'))

cal1[1].send_keys(Keys.CONTROL+'a')
time.sleep(1)
cal1[1].send_keys(to_date.strftime('%m/%d/%Y'))
# print(cal1)

time.sleep(5)


driver.find_element(By.CSS_SELECTOR, '#filter-form-apply').click()
time.sleep(5)

btns = driver.find_elements(By.CSS_SELECTOR, 'button')

for btn in btns:
    if btn.text == 'Export Shipments':
        btn.click()
        break


time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "#exportPrimaryRecordsAndLineItems").click()
time.sleep(5)
driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[5]/div/div[2]/div/div/div[2]/div/div[2]/div/div[3]/div[2]/div/div[5]/label/div[2]").click()
time.sleep(5)




for root,dirs, files in os.walk(download_path_root+"\\"+file_path):
    for file in files:
        os.remove(os.path.join(root, file))
driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[5]/div/div[2]/div/div/div[2]/div/div[3]/div/button[2]").click()

time.sleep(60)
driver.quit()
