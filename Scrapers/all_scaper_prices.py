#! /usr/local/bin/python3.7

import sys
from selenium import webdriver
from datetime import datetime, timedelta
directory_path = '/Users/louis-amandgerard/IT/PyCharm'
# This command had to be made in the Terminal to grant access permissions
#chmod +x /Users/louis-amandgerard/IT/PyCharm/WebScraping/Input/import_data_scraper.py
sys.path.append(directory_path + '/WebScraping/Input')
sys.path.append(directory_path + '/WebScraping/Output')
import import_data_scraper as imp                           # be careful not to have any space or typo of falsely "empty" cells
import export_data_scraper as exp                           # also be careful excel does not format the number in any other way than text
import freightexchange_scraper_prices as fesp
import transdirect_scraper_prices as tdsp
import peakup_scraper_prices as pusp
import movit_scraper_prices as misp

websites = ["freightexchange", "transdirect", "peakup", "movit"]     # Change however you like the websites to test/scrape
#websites = ["peakup"]
#websites = ["freightexchange"]
#websites = ["transdirect"]
#websites = ["movit"]




def how_long_is_it_going_to_take(websites, average_duration = 14): # the average is 14 seconds per website

    fr, to, km, dt, vog, pk = imp.input_data()
    total_duration = timedelta(seconds = len(fr) * len(websites) * average_duration)
    # how long is the input times how many websites are used times the length for one website search
    print("It will take approximatelly", total_duration)

    return total_duration
#how_long_is_it_going_to_take(websites, average_duration = 15)

###

def global_output(websites, max_minutes = 8 * 60):

    # Initializing
    beginning = datetime.now()
    nsearches = 0
    nrows = 0
    nerrors = 0
    fr, to, km, dt, vog, pk = imp.input_data()
    l = len(fr) * len(websites) # how many search will be made

    # Scraping
    for i in range(len(fr)):
        if datetime.now() - beginning >= timedelta(minutes = max_minutes): # if max duration has been reached
            break
        for website in websites:
            if datetime.now() - beginning >= timedelta(minutes = max_minutes): # if max duration has been reached
                break
            now = datetime.now()

            # Browser
            driver = webdriver.Chrome(executable_path = r"" + directory_path + "/WebScraping/Scrapers/chromedriver") # open the driver/browser
            try:
                if website == "peakup":
                    nrows, nerrors = pusp.peakup_output_data(driver, fr[i], to[i], km[i], dt[i], vog[i], pk[i], nrows, nerrors)
                elif website == "freightexchange":
                    nrows, nerrors = fesp.freightexchange_output_data(driver, fr[i], to[i], km[i], dt[i], vog[i], pk[i], nrows, nerrors)
                elif website == "transdirect":
                    nrows, nerrors = tdsp.transdirect_output_data(driver, fr[i], to[i], km[i], dt[i], vog[i], pk[i], nrows, nerrors)
                elif website == "movit":
                    nrows, nerrors = misp.movit_output_data(driver, fr[i], to[i], km[i], dt[i], vog[i], pk[i], nrows, nerrors)
            except:
                row = [website, now, fr[i], to[i], km[i], dt[i], vog[i], pk[i][0], pk[i][1], pk[i][2], pk[i][3], pk[i][4],
                       "", "", "", "", "Unexpected error with '" + website + "'. Might be the page taking too long to load"]
                exp.export_data_row(row)
                nerrors += 1 # number of errors
                nrows += 1 # one error is still one row
            nsearches += 1 # number of searches
            driver.quit() # quit the driver/browser

            # Visual output after each search
            duration = datetime.now() - beginning
            print(nsearches, " searches made. A total of ", l, " to make.\n",
                  round(nsearches / l * 100, 2), " %.\n",
                  timedelta(minutes = max_minutes) - duration, " available for this query.\n",
                  (duration / nsearches) * (l - nsearches), " remaining for the whole data output.\n", sep = "")

    # Visual output at the very end of the program
    print('\nRows of data :', nrows,
          '\nNumber of searches made :', nsearches,
          '\nNumber of errors :', nerrors,
          '\nPorportion of errors :', round(nerrors / nsearches * 100, 2), '%')
    print('\nDuration :', duration,
          '\nAverage duration per row :', duration / nrows,
          '\nAverage duration per search :', duration / nsearches)
    exp.export_log(beginning, duration, nrows, nsearches, nerrors)

    return 1


global_output(websites, 0.5)#11 * 60)



# Be careful when opening with Excel the output .csv, it will delete everything except for minutes and secondes in the dates, hence making them useless
