"""
Constants
=========

Provides useful constants and Enums.
"""

# Global constants ----

colour_icons = ('green', 'red', 'yellow', 'pink', 'violet', 'blue', 'black', 'orange', 'lightblue', 'white', 'polka', 'maillotmon') # TODO Any more?
uci_categories = ['2.2', '2.1', '2.HC', '2.WT1', '2.WT2', '2.WT3', '2.Pro', 'GT1', 'GT2', '1.2', '1.1', '1.HC', '1.WT1', '1.WT2', '1.WT3', '1.Pro']
one_day_categories = ['1.2', '1.1', '1.HC', '1.WT1', '1.WT2', '1.WT3', '1.Pro']
championships_categories = ['CN', 'CCRR', 'CCTT', 'CCU', 'CCUT', 'WCRR', 'WCTT', 'WCU', 'WCUT']
U23_categories = ['1.2U', '2.2U', '1.NC', '2.NC']


# Global enums ----
from enum import Enum

classifications = {'general': 1, 'youth': 2, 'points': 3, 'mountain': 4, 'sprint': 6}
Classification = Enum('Classification', classifications)
"""
Enum mapping classification names to numbers.

Examples
========
>>> Classification.general.value
1
>>> Classification(1).name
'general'
"""

profile_icon_map = {'Bakketempo.png': 'Mountain ITT',
			'Fjell-MF.png': 'Mountain MTF',
			'Fjell.png': 'Mountain',
			'Flatt.png': 'Flat',
			'Smaakupert-MF.png': 'Hilly MTF',
			'Smaakupert.png': 'Hilly',
			'Tempo.png': 'Flat ITT',
			'Brosten.png': 'Cobbles',
			'Ukjent.png': 'Unknown', # e.g. 2021 Vuelta stage 4 - flat with hilltop finish
			'Lagtempo.png': 'TTT'} # TODO Any more?
Profile = Enum('Profile', profile_icon_map)
"""
Enum mapping profile icon file names to profile types.

Examples
========
>>> Profile['Flatt.png'].value
'Flat'
>>> Profile('Flat').name
'Flatt.png'
"""

class Country(Enum):
	"""
	Enum mapping three-letter country flag codes to country names.

	Examples
	========
	>>> Country.SLO.value
	'Slovenia'
	>>> Country('Slovenia').name
	'SLO'
	"""
	ALB = "Albania"
	ALG = "Algeria"
	AND = "Andorra"
	ANG = "Angola"
	AIA = "Anguilla"
	ATG = "Antigua and Barbuda"
	ARG = "Argentina"
	ARU = "Aruba"
	AUS = "Australia"
	AUT = "Austria"
	AZE = "Azerbaijan"
	BAH = "Bahamas"
	BRB = "Barbados"
	BLR = "Belarus"
	BEL = "Belgium"
	BLZ = "Belize"
	BEN = "Benin"
	BER = "Bermuda"
	BOL = "Bolivia"
	BOT = "Botswana"
	BIH = "Bosnia&Herzegovina"
	BRA = "Brazil"
	VGB = "British Virgin Islands"
	BUL = "Bulgaria"
	BFA = "Burkina Faso"
	CAM = "Cambodia"
	CMR = "Cameroon"
	CAN = "Canada"
	CHI = "Chile"
	CHN = "China"
	COL = "Colombia"
	CRC = "Costa Rica"
	CRO = "Croatia"
	CUB = "Cuba"
	CYP = "Cyprus"
	CZE = "Czech Republic"
	DEN = "Denmark"
	DOM = "Dom. Republic"
	CDR = "DR Congo"
	ECU = "Ecuador"
	EGY = "Egypt"
	SLV = "El Salvador"
	ERI = "Eritrea"
	EST = "Estonia"
	ETH = "Ethiopia"
	FIN = "Finland"
	FRA = "France"
	GAB = "Gabon"
	GEO = "Georgia"
	GER = "Germany"
	GHA = "Ghana"
	GBR = "Great Britain"
	GRE = "Greece"
	GUA = "Guatemala"
	GUY = "Guyana"
	HON = "Honduras"
	HKG = "Hong Kong"
	HUN = "Hungary"
	ISL = "Iceland"
	IND = "India"
	IDN = "Indonesia"
	IRL = "Ireland"
	IRN = "Iran"
	ISR = "Israel"
	ITA = "Italy"
	CIV = "Ivory Coast"
	JPN = "Japan"
	KAZ = "Kazakhstan"
	KEN = "Kenya"
	KOS = "Kosovo"
	KUW = "Kuwait"
	LAO = "Laos"
	LAT = "Latvia"
	LIB = "Lebanon"
	LES = "Lesotho"
	LTU = "Lithuania"
	LUX = "Luxembourg"
	MAC = "Macao"
	MKD = "Macedonia"
	MAS = "Malaysia"
	MLI = "Mali"
	MLT = "Malta"
	MRI = "Mauritius"
	MEX = "Mexico"
	MDA = "Moldova"
	MGL = "Mongolia"
	MGO = "Montenegro"
	MON = "Monaco"
	MAR = "Morocco"
	NAM = "Namibia"
	NED = "Netherlands"
	ANT = "Netherlands Antilles"
	NZL = "New Zealand"
	NCA = "Nicaragua"
	NGA = "Nigeria"
	NON = "None given"
	NOR = "Norway"
	PAN = "Panama"
	PAR = "Paraguay"
	PER = "Peru"
	PHI = "Philippines"
	POL = "Poland"
	POR = "Portugal"
	PUR = "Puerto Rico"
	QAT = "Qatar"
	ROM = "Romania"
	RUS = "Russia"
	RWA = "Rwanda"
	KSA = "Saudi Arabia"
	SEN = "Senegal"
	SBA = "Serbia"
	SEY = "Seychelles"
	SIN = "Singapore"
	SVK = "Slovakia"
	SLO = "Slovenia"
	RSA = "South Africa"
	KOR = "South Korea"
	ESP = "Spain"
	SRI = "Sri Lanka"
	VIN = "St.Vincent&Grenadines"
	SUD = "Sudan"
	SWE = "Sweden"
	SUI = "Switzerland"
	SYR = "Syria"
	TPE = "Taiwan"
	TAN = "Tanzania"
	THA = "Thailand"
	TRI = "Trinidad & Tobago"
	TUN = "Tunisia"
	TUR = "Turkey"
	UGA = "Uganda"
	UKR = "Ukraine"
	UAE = "United Arab Emirates"
	URU = "Uruguay"
	USA = "USA"
	UZB = "Uzbekistan"
	VEN = "Venezuela"
	VIE = "Vietnam"
	UCI = "World Championship"
	ZIM = "Zimbabwe"