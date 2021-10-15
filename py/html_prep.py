#--------------------------------------
#	HTML Prepping Functions
#--------------------------------------

# Prep sidebar and set active link
def build_sidebar(page):
	# Hard code the navbar here
	nav_headers = [
		['Start Here', '', '', 'icon-money-coins'],
		['How to Use', 'how-to', '', 'icon-paper'],
		['Credits', 'credits', '', 'icon-badge']
	]
	# Choose which page to activate
	for nav in nav_headers:
		if nav[0] == page:
			nav[2] = 'active'
	return nav_headers