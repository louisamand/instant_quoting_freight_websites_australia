#! /usr/local/bin/python3.7
# This first line is important to be able to use this file from another file.

from datetime import datetime, timedelta
import csv


def import_routes():

    name = '../Input/routes.csv' # relative path to the routes file
    with open(name, mode = 'r') as f: # open as 'read'
        routes = list(csv.reader(f)) # make a list made of all non empty rows
    routes.pop(0) # deleted the header
    fr, to, km = [], [], [] # initialising the output values (lists)
    for i in range(len(routes)): # for each row of data
        fr.append(routes[i][0]) # take the first column of the i'th row and add it to the [fr = ZIP code of origin] list
        to.append(routes[i][1]) # ... [to = ZIP code of destination]
        km.append(routes[i][2]) # ... [km = distance between the two cities]

    return fr, to, km

###

def import_value_of_goods(): # mostly the same as import_routes

    name = '../Input/value_of_goods.csv'
    with open(name, mode = 'r') as f:
        value_of_goods = list(csv.reader(f))
    value_of_goods.pop(0)
    for i in range(len(value_of_goods)):
        value_of_goods[i] = value_of_goods[i][0]

    return value_of_goods

###

def import_packaging(): # mostly the same as import_routes

    name = '../Input/packaging.csv'
    with open(name, mode = 'r') as f:
        packaging = list(csv.reader(f))
    packaging.pop(0)
    for i in range(len(packaging)):
        packaging[i] = packaging[i][0:5] # take the first five columns of the i'th row and add the list (of five items) to the packaging list

    return packaging

###

def import_dates(): # mostly the same as import_routes

    name = '../Input/dates.csv'
    with open(name, mode = 'r') as f:
        dates = list(csv.reader(f))
    dates.pop(0)
    for i in range(len(dates)):
        dates[i] = dates[i][0]

        # the next few lines are date validation
        if datetime.strptime(dates[i], "%d/%m/%Y") < datetime.now() + timedelta(days = 1): # if the date is today or in the past
            dates[i] = (datetime.now() + timedelta(days = 2)).strftime("%d/%m/%Y") # make the date as the day after tomorrow
        if datetime.strptime(dates[i], "%d/%m/%Y").weekday() == 5: # if the date is a Saturday
            dates[i] = (datetime.strptime(dates[i], "%d/%m/%Y") + timedelta(days = 2)).strftime("%d/%m/%Y") # Make it the next Monday
        elif datetime.strptime(dates[i], "%d/%m/%Y").weekday() == 6: # if the date is a Sunday
            dates[i] = (datetime.strptime(dates[i], "%d/%m/%Y") + timedelta(days = 1)).strftime("%d/%m/%Y") # Make it the next Monday

    return dates

###

def input_data():

    # Getting the base input
    fr, to, km, dt, vog, pk = [], [], [], [], [], [] # initialise the output values (lists)
    route_fr, route_to, route_km = import_routes() # get the routes from the .csv
    dates = import_dates() # get the dates from the .csv
    value_of_goods = import_value_of_goods() # get the v.o.g. from the .csv
    packaging = import_packaging() # get the packagings from the .csv

    # Making the complete input
    for iro in range(len(route_fr)):
        for idt in range(len(dates)):
            for ivog in range(len(value_of_goods)):
                for ipk in range(len(packaging)): # for each route, each date, each v.o.g. and each packaging line, there will be one query row
                    fr.append(route_fr[iro])
                    to.append(route_to[iro])
                    km.append(route_km[iro])
                    dt.append(dates[idt])
                    vog.append(value_of_goods[ivog])
                    pk.append(packaging[ipk])

    return fr, to, km, dt, vog, pk

#fr, to, km, dt, vog, pk = input_data() # testing purpose

impact = """
def export_packaging():
    with open('../Input/packaging.csv', mode='a') as f:
        instant_quote_sraping = csv.writer(f)
        for pallets in range(5, 105, 5): # from 5 to 100 pallets every 5 pallets
            for weight in range(100, 2100, 100): # from 100 to 2000 pallets every 100 pallets
                row = [pallets, 110, 110, 150, weight] # 110 x 110 x height are the Australian standard pallet dimensions
                instant_quote_sraping.writerow(row)
    return "Done"
""" # this was to have a special input for looking at the impact of pallet quantity and pallet weight on prices