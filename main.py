# main part of the program
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import argparse
from datetime import datetime, timedelta

maindf = pd.DataFrame()

# instead of a list of tickers we should run this script
# for a single ticker passed in as an argument to the script
parser = argparse.ArgumentParser(description="Calculate the annualized return on options")
optional = parser._action_groups.pop()
arglist = parser.add_argument_group("Arguments")
arglist.add_argument("-t", "--ticker", default="BNS", help="Stock symbol")
arglist.add_argument("-n", "--min_days", default=10, help="Minimum days to expiry")
arglist.add_argument("-x", "--max_days", default=120, help="Maximum days to expiry")
arglist.add_argument("-r", "--strike_range", default=0.10, help="Percent strike price range")
parser._action_groups.append(optional)
args = parser.parse_args()

# get the option quotes for the ticker passed in
ticker = args.ticker
strike_range = args.strike_range
url = "https://www.m-x.ca/nego_cotes_en.php?symbol=" + ticker + "*"
page_response = requests.get(url,
                                headers={"User-Agent":"Mozilla/6.0"}, timeout=5)
page_content = BeautifulSoup(page_response.content, features="html.parser")

# we want the list item for the Last price
# calculate the range of strike prices we are interested in
# the quote-info class has the snapshot of the last traded price
quote_info = page_content.find(class_="quote-info")
# the last price is in a b tag within the first li tag
last_price = float(quote_info.find("li").find("b").text.strip())
min_price = last_price - (last_price * float(strike_range))
max_price = last_price + (last_price * float(strike_range))

print(last_price)
print(min_price)
print(max_price)

# option chain is the tbody of a table with class='data'
option_chain = page_content.find(class_="data").find("tbody").findChildren("tr")
print(option_chain)

# loop through the rows and put the info into a dataframe then apply a function to
# strip out rows outside the price range or date range

# calculate the annualized return assuming OOTM put exp or call away
