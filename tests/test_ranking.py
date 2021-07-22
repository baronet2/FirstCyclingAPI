from first_cycling_api import Ranking

import vcr

my_vcr = vcr.VCR(cassette_library_dir='tests/vcr_cassettes/ranking', path_transformer=vcr.VCR.ensure_suffix('.yaml'))

@my_vcr.use_cassette()
def test_2020_UCI_ranking():
	ranking = Ranking(h=1, rank=1, y=2020, page=2)
	assert len(ranking.table) == 100 # 100 rows in result
	assert ranking.table['Rider'].iloc[0] == 'Egan Bernal'

@my_vcr.use_cassette()
def test_2016_french_race_ranking():
	ranking = Ranking(k='nat', nat='fra', y=2016, race=1)
	assert len(ranking.table) == 16
	assert ranking.table['CAT'].iloc[-1] == '1.1'

@my_vcr.use_cassette()
def test_2018_women_junior_fc_ranking():
	ranking = Ranking(k='fc', rank='wjr', y=2018)
	assert len(ranking.table) == 100
	assert ranking.table['Points'].iloc[0] == 2286