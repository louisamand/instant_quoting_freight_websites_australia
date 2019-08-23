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
import random
import string
import time
directory_path = '/Users/louis-amandgerard/IT/PyCharm'
# This command had to be made in the Terminal to grant access permissions:
#chmod +x /Users/louis-amandgerard/IT/PyCharm/WebScraping/Output/export_data_scraper.py
sys.path.append(directory_path + '/WebScraping/Output') # link to export source
import export_data_scraper as exp




def fill_form(driver, fr, to, dt, vog, pk):

    # Origin
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="pickup_location"]'))) # wait up to 3 sec for the page to load
    driver.find_element_by_xpath('//*[@id="pickup_location"]').send_keys(fr) # input the ZIP code of origin
    # as some suburbs share the same ZIP code, we need to manually, if we care, take the right city
    # (ex: '2000, Barangaroo' does not have as many options as '2000, Sydney', hence this addition of complexity)
    f = "1" # initialise row. Default will be first proposition
    if fr == "2000": # Sydney
        f = "6" # take 6th row
    elif fr == "2300": # Newcaslte
        f = "3" # ...
    elif fr == "3220": # Geelong
        f = "2" # ...
    elif fr == "4000": # Brisbane
        f = "2" # ...
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '//*[@id="frm_quote"]/div[2]/div[1]/div/div[2]/ul/li[' + f + ']'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[1]/div/div[2]/ul/li[' + f + ']').click() # click on the right proposition

    # Destination
    driver.find_element_by_xpath('//*[@id="delivery_location"]').send_keys(to) # input the ZIP code of destination
    t = "1" # the same as 'f'
    if to == "2000":
        t = "6"
    elif to == "2300":
        t = "3"
    elif to == "3220":
        t = "2"
    elif to == "4000":
        t = "2"
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable(
        (By.XPATH, '//*[@id="frm_quote"]/div[2]/div[2]/div/div[2]/ul/li[' + t + ']'))) # wait for the drop down menu to load
    driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[2]/div/div[2]/ul/li[' + t + ']').click() # click on the right proposition

    # Pallet choice
    driver.find_element_by_xpath('//*[@id="packet_type[]"]').click()  # item type
    WebDriverWait(driver, 1).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="packet_type[]"]/option[8]'))) # wait for drop down menu to load
    driver.find_element_by_xpath('//*[@id="packet_type[]"]/option[8]').click() # choose 'pallet'

    # Packaging
    driver.find_element_by_xpath('//*[@id="package_qty[]"]').send_keys(Keys.BACK_SPACE) # delete the default quantity of 1 (.clear() did not work)
    # as the website did not allow regular writing, I had so simulate Numeric Pad typing. To make is scalable, this is a function: numpad_fill
    # the eval() function turns a string into executable code
    driver.find_element_by_xpath('//*[@id="package_qty[]"]').send_keys(eval(numpad_fill(pk[0]))) # input pallet quantity
    driver.find_element_by_xpath('//*[@id="package_lt[]"]').send_keys(eval(numpad_fill(pk[1]))) # input pallet length
    driver.find_element_by_xpath('//*[@id="package_wdt[]"]').send_keys(eval(numpad_fill(pk[2]))) # input pallet width
    driver.find_element_by_xpath('//*[@id="package_ht[]"]').send_keys(eval(numpad_fill(pk[3]))) # input pallet height
    driver.find_element_by_xpath('//*[@id="package_wt[]"]').send_keys(eval(numpad_fill(pk[4]))) # input pallet weight

    # Personal details
    name, email, phone = fake_info_fill() # as they ask for name, email and phone number, I created a fake_info_fill function
    driver.find_element_by_xpath('//*[@id="user_name"]').send_keys(name) # input fake name
    driver.find_element_by_xpath('//*[@id="email_id1"]').send_keys(email) # input fake email
    driver.find_element_by_xpath('//*[@id="phone_no"]').send_keys(phone) # input fake phone number

    # Business buttons
    driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[3]/div/div[2]/div[1]/label').click() # click on 'Business' for origin
    driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[4]/div/div[2]/div[1]/label').click() # click on 'Business' for destination

    # Validation
    driver.find_element_by_xpath('//*[@id="get_quote"]').click() # click on the 'Get A Quote' button to load the results page

    return 1

###

def numpad_fill(str_num):

    key = "" # initialisation
    for i in range(len(str_num)): # for each character of the string number
        key = key + "Keys.NUMPAD" + str_num[i] + ", " # the are more than one key press to simulate, hence the ', '
    key = key[:-2] # but the last ', ' would only return an error, so we cut it

    return key

###

def fake_info_fill():

    first = random.choice(string.ascii_uppercase) # one random first capital letter
    last = random.choice(["Perth", "Sydney", "Devil", "Hot", "Haul", "Load", "Miles", "Smith", "Jacks", "Jesus", "Andrew"]) # random last name
    mail = random.choice(["gmail", "hotmail", "mail", "load", "freight", "gloups", "webmail", "icloud", "live", "outlook"]) # random email provider
    domain = random.choice([".com", ".com.au", ".au", ".cn", ".jp", ".asia", ".nz"]) # random email origin
    name = first + "".join(random.choice(string.ascii_lowercase) for i in range(random.randint(1, 9))) + " " + last # concatenation of name
    email = first + "." + last + "@" + mail + domain # concatenation of email
    phone = random.randint(10 ** 9, 10 ** 10 - 1) # random 10 digits number

    return name, email, phone

###

def scrape_individual_prices(driver):

    try:
        # Initialisation
        WebDriverWait(driver, 8).until(expected_conditions.text_to_be_present_in_element((By.XPATH,
                                                    '/html/body/div[5]/div/div[2]/div/div[1]/span'),'Details of Quote :')) # wait up to 8 seconds for page to load
        price, type, duration, insurance = [], [], [], [] # initialise output variables

        # General delivery
        try:
            price.append(round(float(driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[5]/div[2]').text.split("$ ", 1)[1]) / 1.1, 2))
            # get the price, after '$ ', convert it to float, take out the GST and round it to 2 digits
            type.append(driver.find_element_by_xpath('//*[@id="frm_quote"]/div[1]/div[9]/div[2]').text)
            # get the type of delivery
            duration.append(driver.find_element_by_xpath('//*[@id="frm_quote"]/div[1]/div[8]/div[2]').text)
            # get the duration of delivery
            insurance.append(driver.find_element_by_xpath('//*[@id="insurance_amt"]').text)
            # get the insured value
        except:
            pass

        # Express delivery
        try:
            driver.find_element_by_xpath('//*[@id="service_div"]/div[2]/div[1]/div[1]/div[2]/div[1]/label').click() # click on the express button
            price.append(round(float(driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[5]/div[2]').text.split("$ ", 1)[1]) / 1.1, 2))
            # ...
            type.append("Express " + driver.find_element_by_xpath('//*[@id="frm_quote"]/div[1]/div[9]/div[2]').text)
            # get the type of delivery and add 'Express '
            duration.append(driver.find_element_by_xpath('//*[@id="service_div"]/div[2]/div[1]/div[1]/div[1]').text.split(": ", 1)[1])
            # get the duration for express (different path), after ': '
            insurance.append(driver.find_element_by_xpath('//*[@id="insurance_amt"]').text)
            # ...
        except:
            pass
    except:
        return [], [], [], [], "Price page not loading for some reason"

    return price, type, duration, insurance

###

def what_went_wrong(driver):

    error = [] # initialisation, as there might be more than one error

    # XPATH
    try:
        if driver.find_element_by_xpath('//*[@id="pickup_location"]').get_attribute('class')[-3:] == "err": # if the last 3 characters of origin's class are 'err'
            error.append("Pick-up address filling error")
        if driver.find_element_by_xpath('//*[@id="delivery_location"]').get_attribute('class')[-3:] == "err": # ... destination
            error.append("Delivery address filling error")
        if driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[3]/div/div[2]/div[1]/label').get_attribute('class')[-3:] == "err": # ... origin button
            error.append("Business origin button error")
        if driver.find_element_by_xpath('//*[@id="frm_quote"]/div[2]/div[4]/div/div[2]/div[1]/label').get_attribute('class')[-3:] == "err": # ... destination button
            error.append("Business destination button error")
        if driver.find_element_by_xpath('//*[@id="package_detail"]/div[2]/div[2]/div/div').get_attribute('class')[-3:] == "err": # ... weight
            error.append("Weight error")
        if driver.find_element_by_xpath('//*[@id="package_detail"]/div[3]/div[1]/div[2]/div/div').get_attribute('class')[-3:] == "err": # ...length
            error.append("Length error")
        if driver.find_element_by_xpath('//*[@id="package_detail"]/div[3]/div[2]/div[2]/div/div').get_attribute('class')[-3:] == "err": # ... width
            error.append("Width error")
        if driver.find_element_by_xpath('//*[@id="package_detail"]/div[3]/div[3]/div[2]/div/div').get_attribute('class')[-3:] == "err": # ... height
            error.append("Height error")
        if driver.find_element_by_xpath('//*[@id="user_name"]').get_attribute('class')[-3:] == "err": # ... name detail
            error.append("Name error")
        if driver.find_element_by_xpath('//*[@id="email_id1"]').get_attribute('class')[-3:] == "err": # ... email detail
            error.append("Email error")
        if driver.find_element_by_xpath('//*[@id="phone_no"]').get_attribute('class')[-3:] == "err": # ... phone detail
            error.append("Phone error")
        if error == []: # if none of the above
            error = "Unknown filling error"
    except:
        error.append("Unknown filling error")

    # HTML
    if re.search(r"Please fill in this field", driver.page_source) is not None: # if string in HTML
        error.append("Date error")
    elif re.search(r"This field is required", driver.page_source) is not None: # ...
        error.append("Packaging filling error")
    elif re.search(r"The total weight is required", driver.page_source) is not None:# ...
        error.append("Weight filling error")

    return error

###

def movit_output_data(driver, fr, to, km, dt, vog, pk, nrows, nerrors):

    # Initializing
    url = "https://www.movit.com.au/quote/"
    driver.get(url)
    now = datetime.now()

    # Scraping
    fill_form(driver, fr, to, dt, vog, pk) # fill
    price, type, duration, insurance = scrape_individual_prices(driver) # scrape

    # Exporting
    if re.search(r'Details of Quote :', driver.page_source) is None: # if string not in HTML, page has not loaded correctly
        error = what_went_wrong(driver)
        row = ["MovIt", now, fr, to, km, datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], "", "", "", "", error]
        exp.export_data_row(row)
        nerrors += 1 # number of errors
        nrows += 1 # one error is still one row
    else:
        for j in range(len(price)): # for every price scraped
            row = ["MovIt", now, fr, to, km,
                   datetime.now().strftime("%d/%m/%Y"), vog, pk[0], pk[1], pk[2], pk[3], pk[4], price[j], type[j], duration[j], insurance[j], ""]
            exp.export_data_row(row)
            nrows += 1 # number of rows

    return nrows, nerrors

