# Getting the rates of Australian instant quoting websites for palletised freight

To run the scraper, run `Scrapers/all_scraper_prices.py` after having chosen how long (in minutes) you want the program to run.

## Input

**Be aware of typos in the input**

### dates.csv

Takes one date per row, in the first column as dd/mm/YYYY.

If the date is in weekends or in the past it will be automatically changed to the next suitable date.


### packaging.csv

Takes one packaging type per row over 5 columns as:

Pallet quantity | Pallet length (cm) | Pallet width (cm) | Pallet height (cm) | Pallet weight (kg)


### routes.csv

Takes one route per row over 3 columns as:

ZIP code of origin city | ZIP code of destination city | Kilometer distance between the two

The km distance is not required for the program but for the later analysis.


### value_of_goods.csv

Takes one value per row on the first column in dollar value.

Only required for one website and possibly useful for a second to benchmark the price of their insurance service.


### import_data_scraper.py

Imports all data from `.csv` files, deletes the header and take only the relevant columns.

Then, for as many combinations as there can be bewteen the rows of each file, there are as many rows of search.


## Scrapers

### chromedriver

It might be needed to get the lastest version of chromedriver. The firefox equivalent would work the same I expect.

I do not own any right, if there is any issue with it being present here please contact me.

### freightexchange_scraper_prices.py

Fills the main page, then scrapes the price, type, duration and insured value for each proposition.

### movit_scraper_prices.py

Fills the main page, then scrapes the price and duration for general and express delivery.

### peakup_scraper_prices.py

Fills the main page, then scrapes the price and duration of the only proposition.

### transdirect_scraper_prices.py

Fills the main page, then scrapes the price, type, duration and insured value for each proposition.

### all_scraper_prices.py

Checks before each search if the input max amount of minutes has not been reached. If not, the program continues searching alternativelly on each website.

## Output

### instant_quote_scraping.csv

It is the destination file with all the data.


### searches_log.csv

It is the log that logs every query made. It does not yet take into account the input files.


### export_data_scraper.py

Takes one row of data and adds it to the existing `instant_quote_scraping.csv` file, or creates it if it has been deleted or moved.
Takes the information of a query and adds it to the existing `searches_log.csv` file, or creates it if it has been deleted or moved.
Takes the information of a query and adds it to the existing `searches_log.csv` file, or creates it if it has been deleted or moved.
