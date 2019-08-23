#! /usr/local/bin/python3.7
# This first line is important to be able to use this file from another

import os
import csv


def export_data_row(row): # called by the each scraper_prices function

    # Creating
    if not os.path.isfile('../Output/instant_quote_sraping.csv'): # if the output file is not present
        with open('../Output/instant_quote_sraping.csv', mode = 'w') as f:  # open the output file in a relative path as 'write'
            instant_quote_sraping = csv.writer(f)
            header = ['Website scraped', 'Date of Scraping', 'City From', 'City To', "Distance", 'Date of Transport', 'Value of Goods', 'Number of Pallets',
                      'Length of Pallets', 'Width of Pallets', 'Height of Pallets', 'Weight of Pallets', 'Price Excl. GST', 'Type', 'Duration', 'Insurance bundle',
                      'error']  # define the header
            instant_quote_sraping.writerow(header)  # write the header

    # Filling
    with open('../Output/instant_quote_sraping.csv', mode = 'a') as f: # open the output file in a relative path as 'append'
        instant_quote_sraping = csv.writer(f)
        instant_quote_sraping.writerow(row) # write the given row

    return 1

###

def export_log(beginning, duration, nrows, nsearches, nerrors): # ...

    # Creating
    if not os.path.isfile('../Output/searches_log.csv'): # ...
        with open('../Output/searches_log.csv', mode = 'w') as f:  # ...
            log = csv.writer(f)
            header = ['Beginning of query', 'End of query', 'Rows of data', 'Number of searches', "Number of errors", 'Porportion of errors (%)', 'Duration',
                      'Average duration per row', 'Average duration per search']  # ...
            log.writerow(header)  # ...

    # Filling
    with open('../Output/searches_log.csv', mode = 'a') as f: # ...
        log = csv.writer(f)
        row = [beginning, beginning + duration, nrows, nsearches, nerrors, round(nerrors / nsearches * 100, 2), duration, duration / nrows, duration / nsearches]
        log.writerow(row)

    return 1