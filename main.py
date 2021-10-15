#----------------------------------------
#	Main App File
#----------------------------------------

from flask import Flask, render_template, request
import py.nest as nest
import py.html_prep as prep

#----------------------------------------
#	Constructor
#----------------------------------------
app = Flask(__name__)

#----------------------------------------
#	URL Routes
#----------------------------------------
# Initial index page
@app.route('/')
def index():
	sidebar = prep.build_sidebar('Start Here')
	return render_template('home.html', sidebar=sidebar)

# Search Robinhood for stocks within price cap
@app.route('/', methods =["GET", "POST"])
def get_penny_stocks():
	# Set up Sidebar nav
	sidebar = prep.build_sidebar('Dashboard')
	
	# Receive post (from stock price input)
	if request.method == 'POST':	
		# Log into Robinhood
		nest.login()

		# Set price threshold + input validation
		try:
			price_threshold = float(request.form.get("price_input"))
		except ValueError:
			price_threshold = 0
		if price_threshold > 25: price_threshold = 25

		# Get names of stocks under threshold
		stock_list = nest.get_stocks_under_x(price_threshold)

		# Gather items info
		items  = []
		for stock in stock_list:
			general = nest.get_gen_info(stock)
			latest_price = nest.get_latest_price(stock)
			items.append([general, latest_price])

		# Log out of Robinhood
		nest.logout()
		
		# Open the results.html page with all gathered info
		return render_template('home.html', sidebar=sidebar, stock_list=items)

	# 418 alert b/c I don't think we'll ever see this error and I need a return in case the above if returns false
	return render_template('error.html', err='418: I\'m a teapot', sidebar=sidebar)

# Display the results on the Dashboard
@app.route('/', defaults={'symbol': None})
@app.route('/<symbol>')
def show_dashboard(symbol):
	sidebar = prep.build_sidebar('Dashboard')	
	if not symbol:
		symbol = request.args.get('symbol')
	if not symbol:
		# Covering bases. We probably won't see this error as opposed to the 404 below
		return render_template('error.html', err='400: Bad request.', sidebar=sidebar)

	# Log in
	nest.login()

	# Check for legit stock, otherwise 404 alert
	if nest.get_name_from_symbol(symbol) == '':
		return render_template('error.html', err='404: Page doesn\'t exist', sidebar=sidebar)

	# Gather item info
	gen   = nest.get_gen_info(symbol)
	price = nest.get_price_info(symbol)
	news  = nest.get_news_info(symbol)
	info  = nest.get_instrument_details(symbol)

	# Log out
	nest.logout()
	return render_template('dashboard.html', sidebar=sidebar, gen=gen, price=price, news=news, info=info)

# How to page
@app.route('/how-to')
def how_to():
	sidebar = prep.build_sidebar('How to Use')
	return render_template('how_to_use.html', sidebar=sidebar)

# Credit page
@app.route('/credits')
def credit():
	sidebar = prep.build_sidebar('Credits')
	return render_template('credits.html', sidebar=sidebar)

#----------------------------------------
#	The Humble Main
#----------------------------------------
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)