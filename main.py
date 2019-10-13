import argparse
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
import pandas as pd
import requests
import time


parser = argparse.ArgumentParser(description="Calculate the annualized return on options")
optional = parser._action_groups.pop()
arglist = parser.add_argument_group("Arguments")
arglist.add_argument("-t", "--ticker", default="BNS",
    help="Stock symbol")
arglist.add_argument("-n", "--min_days", default=10,
    help="Minimum days to expiry")
arglist.add_argument("-x", "--max_days", default=120,
    help="Maximum days to expiry")
arglist.add_argument("-r", "--strike_range", default=0.10,
    help="Percent strike price range")
parser._action_groups.append(optional)
args = parser.parse_args()

# get the option quotes for the ticker passed in
ticker = args.ticker
strike_range = args.strike_range
max_days = args.max_days
today = date.today()
url = "https://www.m-x.ca/nego_cotes_en.php?symbol=" + ticker + "*"
page_response = requests.get(url,
    headers={"User-Agent":"Mozilla/6.0"}, timeout=5)
page_content = BeautifulSoup(page_response.content, features="html.parser")

# the quote-info class has the snapshot of the last traded price
# the last price is in a b tag within the first li tag
quote_info = page_content.find(class_="quote-info")
last_price = float(quote_info.find("li").find("b").text.strip())
min_price = last_price - (last_price * float(strike_range))
max_price = last_price + (last_price * float(strike_range))

print(last_price)
print(min_price)
print(max_price)
print(max_days)

# option chain is the tbody of a table with class='data'
chainhtml = page_content.find(class_="data").find("tbody").findChildren("tr")
chain = []

# loop through the rows and put the info into a dataframe
# each row has 15 columns
for row in chainhtml:
    expiry = datetime.strptime(row.findAll('td')[0]['data-expiry'], '%Y%m%d').date()
    s_price = float(row.findAll('td')[7].text)
    c_bid = float(row.findAll('td')[1].text)
    c_ask = float(row.findAll('td')[2].text)
    c_last = float(row.findAll('td')[3].text)
    p_bid = float(row.findAll('td')[9].text)
    p_ask = float(row.findAll('td')[10].text)
    p_last = float(row.findAll('td')[11].text)
    daystoexp = (expiry - today).days
    option = [expiry, s_price, c_bid, c_ask, c_last, p_bid, p_ask, p_last, daystoexp]
    chain.append(option)

chain_df = pd.DataFrame(chain)
chain_df.columns = ['expiry', 'strike',
                    'call_bid', 'call_ask', 'call_last',
                    'put_bid', 'put_ask', 'put_last', 'daystoexp']

# strip out rows outside the price range or date range
chain_df = chain_df.drop(chain_df[chain_df.strike < min_price].index)
chain_df = chain_df.drop(chain_df[chain_df.strike > max_price].index)
chain_df = chain_df.drop(chain_df[chain_df.daystoexp > max_days].index)
print(chain_df)

# calculate the annualized return assuming OOTM put exp or call away
