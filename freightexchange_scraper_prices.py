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

    # Opening
    driver.find_element_by_xpath('//*[@id="palletBtn"]').click() # send a click to the "Palletised Freight" button as nothing is shown otherwise

    # Origin
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="originRawAddress"]'))) # wait up to 3 sec for the page to load
    driver.find_element_by_xpath('//*[@id="originRawAddress"]').send_keys(fr) # input the ZIP code of origin
    # as some suburbs share the same ZIP code, we need to manually, if we care, take the right city
    # (ex: '2000, Barangaroo' does not have as many options as '2000, Sydney', hence this addition of complexity)
    f = "1" # initialise row. Default will be first proposition
    if fr == "2000": # Sydney
        f = "6" # take 6th row
    elif fr == "2300": # Newcastle
        f = "3" # ...
    elif fr == "3220": # Geelong
        f = "2" # ...
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/ul[1]/li[' + f + ']'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('/html/body/ul[1]/li[' + f + ']').click() # click on the right proposition

    # Destination
    driver.find_element_by_xpath('//*[@id="destinationRawAddress"]').send_keys(to) # input the ZIP code of destination
    t = "1" # the same as 'f'
    if to == "2000":
        t = "6"
    elif to == "2300":
        t = "3"
    elif to == "3220":
        t = "2"
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/ul[2]/li[' + t + ']'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('/html/body/ul[2]/li[' + t + ']').click() # click on the right proposition

    # Business buttons
    driver.find_element_by_xpath('//*[@id="businessOriginBtn"]').click() # click on 'Commercial' for origin
    driver.find_element_by_xpath('//*[@id="businessDestinationBtn"]').click() # click on 'Commercial' for destination

    # Date
    driver.find_element_by_xpath('//*[@id="dateTimePicker"]').send_keys(dt) # input the date

    # Packaging
    driver.find_element_by_xpath('//*[@id="quantity0"]').send_keys(pk[0]) # input pallet quantity
    driver.find_element_by_xpath('//*[@id="length0"]').send_keys(pk[1]) # input pallet length
    driver.find_element_by_xpath('//*[@id="width0"]').send_keys(pk[2]) # input pallet width
    driver.find_element_by_xpath('//*[@id="height0"]').send_keys(pk[3]) # input pallet height
    driver.find_element_by_xpath('//*[@id="itemWeight0"]').send_keys(pk[4]) # input pallet weight

    # VOG
    driver.find_element_by_xpath('//*[@id="insuranceValue"]').send_keys(vog) # input the value of goods for the insurance

    # Validation
    driver.find_element_by_xpath('//*[@id="getPrices"]').click() # click on the '$ Get A Price!' button to load the results page

    return 1

###

def scrape_individual_prices(driver):

    # Loading
    try:
        WebDriverWait(driver, 5).until(expected_conditions.text_to_be_present_in_element((By.XPATH, '//*[@id="buyItNowTable"]/div[1]/div[1]'), 'BEST PRICE'))
        # wait up to 5 sec for the prices to load after the page has loaded
        # (Selenium automatically waits for the page to be loaded, but not for the content)
    except:
        return [], [], [], [], "Price page not loading for some reason"

    # Scraping
    price, type, duration, insurance  = [], [], [], [] # initialise output variables
    for i in range(1, 6): # there are up to 6 delivery propositions. They are all loaded at once, no wait to wait more
        try: # if i'th element is not present, no error will show, it will just continue
            price.append(driver.find_element_by_xpath('//*[@id="buyItNowTable"]/div[' + str(i) + ']/div[2]/div[3]/strong').text.split("$", 1)[1].replace(',', ''))
            # get the price from the i'th proposition, take only the characters after the '$' sign, and delete the ',' for later converstion to float
            type.append(driver.find_element_by_xpath('//*[@id="buyItNowTable"]/div[' + str(i) + ']/div[2]/div[1]').text.split(": ", 1)[1])
            # get the type of delivery and take the part after 'Service: '
            duration.append(driver.find_element_by_xpath('//*[@id="buyItNowTable"]/div[' + str(i) + ']/div[2]/div[1]/span/strong').text)
            # get the duration of delivery
            insurance.append(driver.find_element_by_xpath('//*[@id="buyItNowTable"]/div[' + str(i) + ']/div[2]/div[2]').text.split(" insurance", 1)[0])
            # get the insured value, written before ' insurance'
        except:
            pass # break # don't want to use 'break' as there has been problems before. The website is taking much longer than the program, so not urgent test

    return price, type, duration, insurance

###

def what_went_wrong(driver):

    # XPATH
    try:
        if driver.find_element_by_xpath('//*[@id="originCity"]').get_attribute('value') == "": # if the origin was not input correctly
            error = "Pick-up address filling error"
        elif driver.find_element_by_xpath('//*[@id="destinationCity"]').get_attribute('value') == "": # ...
            error = "Delivery address filling error"
        else:
            error = "Unknown filling error"
    except:
        error = "Unknown filling error"

    # HTML
    if re.search(r"Please fill in this field", driver.page_source) is not None: # if string in HTML
        error = "Date error"
    elif re.search(r"This field is required", driver.page_source) is not None: # ...
        error = "Packaging filling error"
    elif re.search(r"The total weight is required", driver.page_source) is not None: # ...
        error = "Weight filling error"

    return error

###

def freightexchange_output_data(driver, fr, to, km, dt, vog, pk, nrows, nerrors):

    # Initializing
    url = "https://www.freightexchange.com.au/showQuoteForm"
    driver.get(url)
    now = datetime.now()

    # Scraping
    fill_form(driver, fr, to, dt, vog, pk) # fill
    price, type, duration, insurance = scrape_individual_prices(driver) # scrape

    # Exporting
    if re.search(r'BEST PRICE', driver.page_source) is None: # if string not in HTML, page has not loaded correctly
        error = what_went_wrong(driver)
        row = ["Freight Exchange", now, fr, to, km, dt, vog, pk[0], pk[1], pk[2], pk[3], pk[4], "", "", "", "", error]
        exp.export_data_row(row)
        nerrors += 1 # number of errors
        nrows += 1 # one error is still one row
    else:
        for j in range(len(price)): # for every price scraped
            row = ["Freight Exchange", now, fr, to, km, dt, vog, pk[0], pk[1], pk[2], pk[3], pk[4], price[j], type[j], duration[j], insurance[j], ""]
            exp.export_data_row(row)
            nrows += 1 # number of rows

    return nrows, nerrors

