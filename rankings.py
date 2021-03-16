"""
author: Ethan Baron
"""

from utilities import *


def get_raw_rankings_data(url):
	return pd.read_html(url, thousands='.')


def parse_rider_td(td):
    rider_id = int(td.a['href'].split('r=')[1])
    return rider_id

def parse_nation_td(td):
    code = img_to_country_code(td.img)
    return code

def parse_team_td(td):
	if td.a:
	    team_id = int(td.a['href'].split('l=')[1])
	    country_code = img_to_country_code(td.img)
	    return team_id, country_code
	else:
		return None, None

def tr_to_dict(headers, tr):
	# Set up dictionary
	data = tr.find_all('td')
	data = [td.extract() for td in data] # Needed to manage nested td's
	d = dict(zip(headers, data))

	# Obtain hidden metadata
	if 'rider' in d:
		d['rider_id'] = parse_rider_td(d['rider'])
	if 'nation' in d:
		d['nation_code'] = parse_nation_td(d['nation'])
	if 'team' in d:
		d['team_id'], d['team_nation_code'] = parse_team_td(d['team'])
	
	# Reload raw data
	d.update({k: v.text.strip() for k, v in dict(zip(headers, data)).items()})

	# Clean entries
	if 'points' in d:
		d['points'] = int(d['points'].replace('.', ''))
	if 'team' in d:
		d['team'] = d['team'] if d['team'] != '-' else None

	return d

class Ranking:
	def __init__(self, url):
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')
		rankings_table = soup.find('table', {'class': 'tablesorter sort'})
		headers = [th.text.lower() for th in rankings_table.tr.find_all('th')]
		trs = rankings_table.find_all('tr')[1:]
		self.df = pd.DataFrame([tr_to_dict(headers, tr) for tr in trs])



# OLD ----
def get_dict_from_td(headers, tr): # UCI rankings only
    data = tr.find_all('td')
    d = dict(zip(headers, data))
    d['rider_id'] = int(d['rider'].a['href'].split('r=')[1])
    d['rider_country_code'] = img_to_country_code(d['nation'].img)
    d['team_country_code'] = img_to_country_code(d['team'].img)
    d['team_id'] = int(d['team'].a['href'].split('l=')[1])
    d.update({k: v.text.strip() for k, v in dict(zip(headers, data)).items()})
    d['points'] = int(d['points'].replace('.', ''))
    return d

class UCIRanking:
	def __init__(self, url):
		page = requests.get(url)
		soup = bs4.BeautifulSoup(page.text, 'html.parser')
		trs = soup.find('table', {'class': 'tablesorter sort'}).find_all('tr')[1:]
		headers = [th.text.lower() for th in soup.find('table', {'class': 'tablesorter sort'}).tr.find_all('th')]
		self.df = pd.DataFrame([get_dict_from_td(headers, tr) for tr in trs])
