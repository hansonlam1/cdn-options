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
arglist.add_argument("-x", "--max_days", default=120,
    help="Maximum days to expiry")
arglist.add_argument("-r", "--strike_range", default=0.15,
    help="Percent strike price range")
arglist.add_argument("-o", "--output_to", default='p',
    help="Output to html or print")
parser._action_groups.append(optional)
args = parser.parse_args()


# calculate the annualized return assuming OOTM put exp
def annualizereturn(s_price, bid, ask, daystoexp):
    p = round(s_price * 0.25, 2)
    prem = round(((bid + ask) / 2), 2)
    basereturn = round(prem/p, 6)
    annualreturn = round(((1+basereturn)**(365/daystoexp)-1)*100, 2)
    #print(s_price, p, prem, daystoexp, basereturn, annualreturn)
    return annualreturn


# get the option quotes for the ticker passed in
ticker = args.ticker
strike_range = args.strike_range
max_days = int(args.max_days)
out_to = args.output_to
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

# option chain is the tbody of a table with class='data'
chainhtml = page_content.find(class_="data").find("tbody").findChildren("tr")
chain = []

for row in chainhtml:
    expiry = datetime.strptime(row.findAll('td')[0]['data-expiry'], '%Y%m%d').date()
    strike = float(row.findAll('td')[7].text)
    call_bid = float(row.findAll('td')[1].text)
    call_ask = float(row.findAll('td')[2].text)
    c_last = float(row.findAll('td')[3].text)
    put_bid = float(row.findAll('td')[9].text)
    put_ask = float(row.findAll('td')[10].text)
    put_last = float(row.findAll('td')[11].text)
    daystoexp = (expiry - today).days
    option = [expiry, strike, call_bid, call_ask, c_last,
        put_bid, put_ask, put_last, daystoexp]
    chain.append(option)

chain_df = pd.DataFrame(chain)
chain_df.columns = ['expiry', 'strike',
                    'call_bid', 'call_ask', 'call_last',
                    'put_bid', 'put_ask', 'put_last', 'daystoexp']

# strip out rows outside the price range or date range
chain_df = chain_df.drop(chain_df[chain_df.strike < min_price].index)
chain_df = chain_df.drop(chain_df[chain_df.strike > last_price].index)
chain_df = chain_df.drop(chain_df[chain_df.daystoexp > max_days].index)
chain_df = chain_df.drop(chain_df[chain_df.daystoexp == 0].index)
chain_df['estimatedprem'] = chain_df.apply(lambda x: (x['put_bid']+x['put_ask'])/2, axis=1)
chain_df['annualreturn'] = chain_df.apply(lambda x: annualizereturn(x['strike'],
    x['put_bid'], x['put_ask'], x['daystoexp']), axis=1)
dropcols = ['call_bid', 'call_ask', 'call_last', 'put_last']
chain_df = chain_df.drop(columns=dropcols, axis=1)
chain_df = chain_df.reset_index()

if out_to == 'c':
    chain_df.to_csv(ticker + "-" + today.strftime('%Y-%b-%d') + ".csv")    
elif out_to == 'h':
    print(chain_df.to_html())
else:
    print(chain_df)