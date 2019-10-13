# cdn-options
'''
The program calculates the potential return for a strategy
writing naked puts on Canadian stocks.
'''

# parameters

The script accepts parameters to set:
- the maximum days to expiry
- the range of strike prices to evaluate; as a percentage of the last closing price
- the stock symbol

- to run the script in command line: python3 main.py -t tickersymbol
- main.py --help to see other arguments available

# To Do
'''
- Need to calculate the annualized return (likely a function called by the dataframe)
'''