#! /usr/local/bin/python3.7
# This first line is important to be able to use this file from another file.

import re
import sys
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

    # Origin
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/input').send_keys(fr) # input the ZIP code of origin
    # as some suburbs share the same ZIP code, we need to manually, if we care, take the right city
    # (ex: '2000, Barangaroo' does not have as many options as '2000, Sydney', hence this addition of complexity)
    f = "1" # initialise row. Default will be first proposition
    if fr == "2000": # Sydney
        f = "5" # take 5th row
    elif fr == "4000": # Brisbane
        f = "2" # ...
    elif fr == "2300": # Newcaslte
        f = "3" # ...
    # wait for the drop down menu to load
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/typeahead-container/button[' + f + ']')))
    # click on the right proposition
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/typeahead-container/button[' + f + ']').click()

    # Destination
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/input').send_keys(to) # input the ZIP code of destination
    t = "1" # the same as 'f'
    if to == "2000":
        t = "5"
    elif to == "4000":
        t = "2"
    elif to == "2300":
        t = "3"
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/typeahead-container/button[' + t + ']')))
    # wait for the drop down menu to load
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/typeahead-container/button[' + t + ']').click()
    # click on the right proposition

    # Pallet choice
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/select').click() # item type
    WebDriverWait(driver, 1).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/select/option[6]'))) # wait for drop down menu to load
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/select/option[6]').click() # choose 'pallet'

    # Packaging
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/input').send_keys(pk[0]) # input pallet quantity
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[4]/input').send_keys(pk[1]) # input pallet length
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[5]/input').send_keys(pk[2]) # input pallet width
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[6]/input').send_keys(pk[3]) # input pallet height
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/input').send_keys(pk[4]) # input pallet weight

    # Date
    fill_date(driver, dt) # as the choice of the date (AND time) is very manual, I have made of dedicated function for it

    # Validation
    driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[2]/div/button').click() # click on the 'Show Price' button to load the results page

    return 1

###

def fill_date(driver, dt):

    # Initialisation
    driver.find_element_by_xpath('//*[@id="m_datetimepicker_3"]/span').click() # click the calendar icon
    WebDriverWait(driver, 2).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/table/thead/tr[1]/th[3]'))) # wait for it to load

    # Month
    months_difference = datetime.strptime(dt, "%d/%m/%Y").month - datetime.now().month # in how many months
    for i in range(months_difference): # for as many months difference
        driver.find_element_by_xpath('/html/body/div[4]/div[3]/table/thead/tr[1]/th[3]').click() # click next month

    # Day
    day = datetime.strptime(dt, "%d/%m/%Y").day # what day is it
    row = day // 7 + 1 # on what row this number should be, can not be before, but can be after

    # Execution
    brk = None # initialisation, to be able to break two loops in a row
    for r in range(row, row + 2): # for the rows it should be on
        for c in range(1, 8): # for each day
            if driver.find_element_by_xpath('/html/body/div[4]/div[3]/table/tbody/tr[' + str(r) + ']/td[' + str(c) + ']').text == str(day): # if it is the right day
                driver.find_element_by_xpath('/html/body/div[4]/div[3]/table/tbody/tr[' + str(r) + ']/td[' + str(c) + ']').click() # click on the day
                driver.find_element_by_xpath('/html/body/div[4]/div[2]/table/tbody/tr/td/span[10]').click() # click on the hour (10 am)
                driver.find_element_by_xpath('/html/body/div[4]/div[1]/table/tbody/tr/td/span[1]').click() # click on the minute (:00)
                brk = "" # for breaking the second ('row') for loop
                break
        if brk == "": # breaking the 'row' for loop
            break

    return 1

###

def scrape_individual_prices(driver):
    # there might be a need for modifications if they start proposing more delivery types in the future
    # pallets show only one result, but other types do show multiple solutions

    price, type, duration, insurance = [], [], [], []  # initialise output variables
    try:
        # Loading
        WebDriverWait(driver, 3).until(expected_conditions.text_to_be_present_in_element(
            (By.XPATH,'/html/body/div[2]/div[2]/form/div[1]/div[3]/div/div/div[2]/div/a/div/div/div[1]/h4'), 'Taxi Truck Service')) # wait for the result to load
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down (test purpose)

        # General (only) delivery
        duration.append(driver.find_element_by_xpath('/html/body/div[2]/div[2]/form/div[1]/div[3]/div/div/div[2]/div/a/div/div/div[1]/span').text) # get the duration
        price.append(driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/form/div[1]/div[3]/div/div/div[2]/div/a/div/div/div[2]/span').text.split("\n")[0].split("$")[1].replace(',', ''))
        # get the price, take the first line of text, take away the '$' sign and delete the ',' for later conversion to float
        type.append("General Peak Up") # as there is only one result yet
        insurance.append("$ 0.00") # as it doesn't provide insurance with instant quotes
    except:
        return [], [], [], [], "Price page not loading for some reason"

    return price, type, duration, insurance

###

def what_went_wrong(driver):

    # HTLM
    if re.search(r"PriceController.cs:line 567", driver.page_source) is not None: # if string in HTML
        error = "Pick-up address filling error"
    elif re.search(r"PriceController.cs:line 569", driver.page_source) is not None: # ...
        error = "Delivery address filling error"
    elif re.search(r"The Receiver/Destination Suburb", driver.page_source) is not None: # ...
        error = "Route not available for quoting"
    elif re.search(r"Pallet dimensions are not correct!", driver.page_source) is not None: # ...
        error = "Height filling error"
    elif re.search(r"Can't find the rate for the provided suburbs", driver.page_source) is not None: # ...
        error = "Can't find the rate for the provided suburbs"
    elif re.search("For bookings more than", driver.page_source) is not None: # ...
        error = "Too many pallet spaces for this route"
    else:
        error = "Error that can not be specified for Peak Up"

    return error

###

def peakup_output_data(driver, fr, to, km, dt, vog, pk, nrows, nerrors):

    # Initializing
    url = "https://app.peakup.com.au/quote"
    driver.get(url)
    now = datetime.now()

    # Scraping
    fill_form(driver, fr, to, dt, vog, pk) # fill
    price, type, duration, insurance = scrape_individual_prices(driver) # scrape

    # Exporting
    if re.search(r'Available Services', driver.page_source) is None:
        error = what_went_wrong(driver)
        row = ["Peak Up", now, fr, to, km, datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], "", "", "", "", error]
        exp.export_data_row(row)
        nerrors += 1 # number of errors
        nrows += 1 # one error is still one row
    else:
        for j in range(len(price)):  # for every price scraped
            row = ["Peak Up", now, fr, to, km,
                   datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], price[j], type[j], duration[j], insurance[j], ""]
            exp.export_data_row(row)
            nrows += 1 # number of rows

    return nrows, nerrors

