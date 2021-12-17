from first_cycling_api import Rider

import vcr

my_vcr = vcr.VCR(cassette_library_dir='tests/vcr_cassettes/rider', path_transformer=vcr.VCR.ensure_suffix('.yaml'))

@my_vcr.use_cassette()
def test_roglic_2020_results():
	roglic = Rider(18655)
	results_2020 = roglic.year_results(2020)
	assert results_2020.sidebar_details['nation'] == 'Slovenia'
	assert results_2020.sidebar_details['height'] == 1.77
	assert results_2020.results_df['UCI'].max() == 850