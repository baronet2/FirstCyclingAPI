from first_cycling_api import Race, RaceEdition

import vcr

my_vcr = vcr.VCR(cassette_library_dir='tests/vcr_cassettes/race', path_transformer=vcr.VCR.ensure_suffix('.yaml'))

@my_vcr.use_cassette()
def test_2019_amstel():
	amstel = Race(9)
	amstel_2019 = amstel.edition(year=2019)
	results_2019 = amstel_2019.results()
	assert len(results_2019.results_table) == 175
	assert results_2019.results_table['Rider'].iloc[0] == 'van der Poel Mathieu'


@my_vcr.use_cassette()
def test_2014_giro_rosa_prologue():
	giro_rosa_2014 = RaceEdition(race_id=9064, year=2014)
	results = giro_rosa_2014.results(stage_num=0)
	assert results.results_table['Rider'].iloc[0] == 'van Vleuten Annemiek'


@my_vcr.use_cassette()
def test_2023_amstel():
	amstel = Race(9)
	amstel_2023 = amstel.edition(year=2023)
	results_2023 = amstel_2023.results()
	assert len(results_2023.results_table) == 175
	assert results_2023.results_table['Rider'].iloc[0] == 'Pogacar Tadej'
