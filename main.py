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

print(args.ticker)

