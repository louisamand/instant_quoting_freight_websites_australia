# Getting the rates of Australian instant quoting websites for palletised freight

## Input



## Scrapers

Use the all_scraper.py script.

Just run it.

It should be fairly clear with the comments.


## Output

#### instant_quote_scraping.csv
It is the destination file with all the data.

#### searches_log.csv
It is the log that logs every query made. It does not yet take into account the input files.

#### export_data_scraper.py

Takes one row of data and adds it to the existing *instant_quote_scraping.csv* file, or creates it if it has been deleted or moved.
Takes the information of a query and adds it to the existing *searches_log.csv* file, or creates it if it has been deleted or moved.
