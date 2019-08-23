#! /usr/local/bin/python3.7
# This first line is important to be able to use this file from another file.

import re
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from datetime import datetime
directory_path = '/Users/louis-amandgerard/IT/PyCharm'
# This command had to be made in the Terminal to grant access permissions:
#chmod +x /Users/louis-amandgerard/IT/PyCharm/WebScraping/Output/export_data_scraper.py
sys.path.append(directory_path + '/WebScraping/Output') # link to export source
import export_data_scraper as exp






def fill_form(driver, fr, to, dt, vog, pk):

    # Business buttons
    driver.find_element_by_xpath('//*[@id="label-from-type-options"]/label[2]/div/ins').click() # click on 'Commercial' for origin
    driver.find_element_by_xpath('//*[@id="label-to-type-options"]/label[2]/div/ins').click() # click on 'Commercial' for destination

    # Pallet choice
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[1]/div/button').click()  # item type
    WebDriverWait(driver, 1).until(expected_conditions.element_to_be_clickable(
        (By.XPATH,'//*[@id="frm-items"]/div[1]/div[1]/div/div/ul/li[7]/a'))) # wait for drop down menu to load
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[1]/div/div/ul/li[7]/a').click() # choose 'pallet'

    # Packaging
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[6]/input').clear()  # delete the default quantity
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[6]/input').send_keys(pk[0])  # input pallet quantity
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[3]/input').send_keys(pk[1])  # input pallet length
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[4]/input').send_keys(pk[2])  # input pallet width
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[5]/input').send_keys(pk[3])  # input pallet height
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[2]/input').send_keys(pk[4])  # input pallet weight

    # Origin
    driver.find_element_by_xpath('//*[@id="txt-from-postcode-fake"]').send_keys(fr) # input the ZIP code of origin
    WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="ui-id-1"]/li[1]'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('//*[@id="txt-from-postcode-fake"]').send_keys(Keys.ARROW_DOWN) # go down to the first proposition (happily the right one)
    time.sleep(0.1) # implicitly wait for the arrow_down simulation to take effect
    driver.find_element_by_xpath('//*[@id="txt-from-postcode-fake"]').send_keys(Keys.ENTER) # validate the proposition

    # Destination
    driver.find_element_by_xpath('//*[@id="txt-to-postcode-fake"]').send_keys(to) # input the ZIP code of destination
    WebDriverWait(driver, 3).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="ui-id-2"]/li[1]'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('//*[@id="txt-to-postcode-fake"]').send_keys(Keys.ARROW_DOWN) # go down to the first proposition (happily the right one)
    time.sleep(0.1) # implicitly wait for the arrow_down simulation to take effect
    driver.find_element_by_xpath('//*[@id="txt-to-postcode-fake"]').send_keys(Keys.ENTER) # validate the proposition

    # Validation
    driver.find_element_by_xpath('//*[@id="frm-items"]/div[2]/button[2]').click() # click on the 'Get A Quote' button to load the results page

    return fr, to, dt, vog, pk


def scrape_individual_prices(driver):

    # Initialisation
    driver.execute_script("window.scrollTo(0, 900);") # scroll (test purpose)
    time.sleep(2) # implicitly wait for 'toll_priority_overnight' to load (usually the first one)
    price, type, duration, insurance = [], [], [], []

    # Scraping
    for carrier in ["toll_priority_overnight", "allied", "sampson_express", "toll_priority_sameday"]: # normal carriers
        try:
            WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(
                (By.XPATH,'//*[@id="data-' + carrier + '"]/table/tbody/tr/td[5]/form/button'))) # wait for item to load (they do individually)
            price.append(round(float(
                driver.find_element_by_xpath('//*[@id="data-' + carrier + '"]/table/tbody/tr/td[5]/form/input[1]').get_attribute("value")) / 1.1, 2))
            # price, take out the GST and round it to 2 digits
            type.append(carrier) # type of delivery is carrier name
            duration.append(driver.find_element_by_xpath('//*[@id="data-' + carrier + '"]/table/tbody/tr/td[2]').text) # duration of delivery
            insurance.append("$ 0.00") # as it doesn't provide insurance with instant quotes
        except:
            pass
    try: # Northline is special (no more than 20 pallets, info is greyed out otherwise, but still visible)
        northline_pop_over = driver.find_element_by_xpath('//*[@id="northline-alternative-popover"]').text
    except:
        try:
            price.append(round(float(
                driver.find_element_by_xpath('//*[@id="data-northline"]/table/tbody/tr/td[5]/form/input[1]').get_attribute("value")) / 1.1, 2))
            # price, take out the GST and round it to 2 digits
            type.append("northline") # type of delivery is carrier name
            duration.append(driver.find_element_by_xpath('//*[@id="data-northline"]/table/tbody/tr/td[2]').text) # duration of delivery
            insurance.append("$ 0.00") # as it doesn't provide insurance with instant quotes
        except:
            pass

    return price, type, duration, insurance


def what_went_wrong(driver):

    test = "try" # initialisation
    try:
        error = "Unknown filling error"
        test = "Pick-up address"
        if driver.find_element_by_xpath('//*[@id="txt-from-postcode-fake"]').get_attribute('class')[-5:] == "error": # if the last 5 characters are 'error'
            error = "Pick-up address filling error"
        test = "Delivery address"
        if driver.find_element_by_xpath('//*[@id="txt-to-postcode-fake"]').get_attribute('class')[-5:] == "error": # ...
            error = "Delivery address filling error"
        test = "Commercial origin"
        if driver.find_element_by_xpath('//*[@id="label-from-type-options"]/label[2]').get_attribute('class')[-6:] == "danger": # ... 'danger'
            error = "Commercial checking origin error"
        test = "Commercial destination"
        if driver.find_element_by_xpath('//*[@id="label-to-type-options"]/label[2]').get_attribute('class')[-6:] == "danger": # ... 'danger'
            error = "Commercial checking destination error"
        test = "Length"
        if driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[3]/input').get_attribute('class')[-5:] == "error": # ...
            error = "Length filling error"
        test = "Width"
        if driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[4]/input').get_attribute('class')[-5:] == "error": # ...
            error = "Width filling error"
        test = "Height"
        if driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[5]/input').get_attribute('class')[-5:] == "error": # ...
            error = "Height filling error"
        test = "Quantity"
        if driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[6]/input').get_attribute('class')[-5:] == "error": # ...
            error = "Quantity filling error"
        test = "Weight"
        if driver.find_element_by_xpath('//*[@id="frm-items"]/div[1]/div[2]/input').get_attribute('class')[-5:] == "error": # ...
            error = "Weight filling error"
    except:
        error = "Website problem (" + test + ")" # what is the test that did not work

    return error


def transdirect_output_data(driver, fr, to, km, dt, vog, pk, nrows, nerrors):

    # Initializing
    url = "https://www.transdirect.com.au/quotes"
    driver.get(url)
    now = datetime.now()

    # Scraping
    fill_form(driver, fr, to, dt, vog, pk) # fill
    price, type, duration, insurance = scrape_individual_prices(driver) # scrape

    # Exporting
    if re.search(r'ATTENTION - ITEM EXCEEDS 25kgs', driver.page_source) is None:
        error = what_went_wrong(driver)
        row = ["Transdirect", now, fr, to, km, datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], "", "", "", "", error]
        exp.export_data_row(row)
        nerrors += 1 # number of errors
        nrows += 1 # one error is still one row
    else:
        for j in range(len(price)): # for every price scraped
            row = ["Transdirect", now, fr, to, km,
                   datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], price[j], type[j], duration[j], insurance[j], ""]
            exp.export_data_row(row)
            nrows += 1 # number of rows

    return nrows, nerrors

