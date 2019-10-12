# cdn-options
calculate the potential return on canadian options

This project retrieves option quotes for Canadian stocks.
The program calculates the potential return for a strategy
that writes covered calls or naked puts.

# parameters

The script accepts parameters to set:
- the minimum and maximum days to expiry
- the range of strike prices to evaluate; as a percentage of the last closing price
- the stock symbol

- to run the script in command line: python3 main.py -t tickersymbol

# To Do

- Need to calculate the date range
- Need to parse the option chain
- Need to calculate the annualized return (likely a function called by the dataframe)