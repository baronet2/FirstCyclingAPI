from first_cycling_api import Race, RaceEdition

import vcr

my_vcr = vcr.VCR(cassette_library_dir='tests/vcr_cassettes/race', path_transformer=vcr.VCR.ensure_suffix('.yaml'))

@my_vcr.use_cassette()
def test_2019_amstel():
	amstel = Race(9)
	amstel_2019 = amstel.edition(year=2019)
	results_2019 = amstel_2019.results()
	assert len(results_2019.results_table) == 175
	assert results_2019.results_table['Rider'].iloc[0] == 'Mathieu van der Poel'

def test_2023_itzulia():
    r = Race(14244)
    r_2023 = r.edition(year=2023)
    results_2023 = r_2023.results(stage_num=1)
    assert len(results_2023.results_table) == 113
    assert results_2023.results_table['Rider'].iloc[0] == 'Demi Vollering'
    
    standings = r_2023.get_standings()
    
    assert len(standings['gc']) == 97
    assert len(standings['youth']) == 23
    assert len(standings['point']) == 19
    assert len(standings['mountain']) == 7
    assert len(standings['team']) == 19
    
my_vcr.use_cassette()
def test_2014_giro_rosa_prologue():
	giro_rosa_2014 = RaceEdition(race_id=9064, year=2014)
	results = giro_rosa_2014.results(stage_num=0)
	assert results.results_table['Rider'].iloc[0] == 'Annemiek van Vleuten'