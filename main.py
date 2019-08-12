# main part of the program
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import tickerlist
from datetime import datetime, timedelta

# for a specific list of tickers, retrieve option quotes
tickers = tickerlist.TICKERLIST
mindaystoexpiry = 10
maxdaystoexpiry = 60
percentstrikerange = 0.05
maindf = pd.DataFrame()

# loop through and grab the quotes
# calculate the annualized return on a best case scenario