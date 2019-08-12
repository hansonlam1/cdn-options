# main part of the program
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import argparse
from datetime import datetime, timedelta

maindf = pd.DataFrame()

#instead of a list of tickers we should run this script for a single ticker passed in as an argument to the script
parser = argparse.ArgumentParser(description = "Calculate the annualized return on options")
optional = parser._action_groups.pop()
arglist = parser.add_argument_group("Arguments")
arglist.add_argument("-t", "--ticker", default = "BNS", help = "Canadian stock symbol")
arglist.add_argument("-n", "--min_days", default = 10, help = "Minimum days to option expiry")
arglist.add_argument("-x", "--max_days", default = 60, help = "Maximum days to option expiry")
arglist.add_argument("-r", "--strike_range", default = 0.05, help = "Percent strike price range")
parser._action_groups.append(optional)
args = parser.parse_args()

#get the option quotes for the ticker passed in
ticker = args.ticker
url = "https://www.m-x.ca/nego_cotes_en.php?symbol=" + ticker + "*"
page_response = requests.get(url, headers = {"User-Agent":"Mozilla/6.0"},timeout = 5)
page_content = BeautifulSoup(page_response.content)

#we want the list item for the Last price
quote_info = page_content.find(class_ = "quote-info")   #the quote-info class has the snapshot of the last traded price
print(quote_info.find("li").find("b").text.strip())     #the last price is in a b tag within the first li tag

# calculate the range of strike prices we are interested in

#page_content.tbody  #tbody contains the option chain



