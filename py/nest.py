#--------------------------------------
#	Robin-stocks related functions
#--------------------------------------

import os
import robin_stocks as rs

# Log into Robinhood
def login():
	# Using os.environ['key'] to keep my login secret.
	# You can switch the *whole* parameter with a string of your username/password 
	rs.login(os.environ['add_your_username_here'], os.environ['add_your_password_here'], expiresIn= 86400)

# Log out of Robinhood
def logout():
	rs.logout()

# Search Most Popular Stocks Under $25 for stocks under $5 and make a list of those stock names (symbol).
def get_stocks_under_x(price_threshold):
	# If the price is 0, don't bother searching the API for stocks
	if price_threshold <= 0:
		return []
	# Search the stocks otherwise
	cheap_stocks = rs.markets.get_all_stocks_from_market_tag('most-popular-under-25', info=None)
	stocks_under_x = []
	for stock in cheap_stocks:
		if float(stock["ask_price"]) <= price_threshold:
			symbol = stock["symbol"]
			stocks_under_x.append(symbol)
			# Fixing a bug where some stock info cam
			while stocks_under_x[-1] == '':
				del stocks_under_x[-1]
				stocks_under_x.append(symbol)
	return stocks_under_x

def get_gen_info(stock_name):
	return rs.stocks.find_instrument_data(stock_name)[0]

def get_price_info(stock_name):
	return rs.stocks.get_quotes(stock_name)[0]

def get_news_info(stock_name):
	return rs.stocks.get_news(stock_name)

def get_latest_price(stock_name):
	return rs.stocks.get_latest_price(inputSymbols=stock_name, priceType=None, includeExtendedHours=True)

def get_stock_historials(stock_name, interval='hour', span='week', bounds='regular', info=None):
	return rs.stocks.get_stock_historicals(stock_name, interval, span, bounds, info)

def get_instrument_details(stock_name):
	return rs.stocks.get_instruments_by_symbols(stock_name, info=None)

def get_name_from_symbol(stock_name):
	return rs.stocks.get_name_by_symbol(stock_name)