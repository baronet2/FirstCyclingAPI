from first_cycling_api import Race, RaceEdition

import vcr

my_vcr = vcr.VCR(cassette_library_dir='tests/vcr_cassettes/race', path_transformer=vcr.VCR.ensure_suffix('.yaml'))

#Amstel uses the old style, single day race

@my_vcr.use_cassette()
def test_2019_amstel():
	amstel = Race(9)
	amstel_2019 = amstel.edition(year=2019)
	results_2019 = amstel_2019.results()
	assert len(results_2019.results_table) == 175
	assert results_2019.results_table['Rider'].iloc[0] == 'Mathieu van der Poel'
    
#LBL uses the new style, single day race    
def test_2023_lbl_women():
	lbl = Race(9052)
	lbl_2023 = lbl.edition(year=2023)
	results_2023 = lbl_2023.results()
	assert len(results_2023.results_table) == 140
	assert results_2023.results_table['Rider'].iloc[0] == 'Demi Vollering'    
    
#TdF uses the old style, stage race
def test_2022_TdF():
    tdf= Race(17)
    tdf_2022 = tdf.edition(year=2022)
    results_2022 = tdf_2022.results()
    assert len(results_2022.results_table) == 176
    assert results_2022.results_table['Rider'].iloc[0] == 'Jonas Vingegaard'
    assert results_2022.results_table['Time'].iloc[0] == "79:33:20"
    assert results_2022.results_table['Pos'].iloc[0] == "01"

    r=tdf_2022.results(classification_num=1).results_table
    assert len(r) == 176
    assert r['Rider'].iloc[0] == 'Jonas Vingegaard'
    assert r['Time'].iloc[0] == "79:33:20"
    
    r=tdf_2022.results(classification_num=2).results_table
    assert len(r) == 26
    assert r['Rider'].iloc[0] == "Tadej Pogacar"
    assert r['Time'].iloc[0] == "79:36:03"
    
    r=tdf_2022.results(classification_num=3).results_table
    assert len(r) == 119
    assert r['Rider'].iloc[0] == "Wout van Aert"
    assert r['Points'].iloc[0] == 480
    
    r=tdf_2022.results(classification_num=4).results_table
    assert len(r) == 55
    assert r['Rider'].iloc[0] == 'Jonas Vingegaard'
    assert r['Points'].iloc[0] == 72
   
    assert len(tdf_2022.results(classification_num=8).results_table) == 22

    results_st1 = tdf_2022.results(stage_num=1)
    assert len(results_st1.results_table) == 176
    assert results_st1.results_table['Rider'].iloc[0] == 'Yves Lampaert'
  
#Itzulia uses the new style, stage race
def test_2023_itzulia():
    race = Race(14244)
    r_2023 = race.edition(year=2023)
    
    results_2023 = r_2023.results(stage_num=1)
    assert len(results_2023.results_table) == 113
    assert results_2023.results_table['Rider'].iloc[0] == 'Demi Vollering'
    
    assert 'gc' in results_2023.standings
    assert 'point' in results_2023.standings
    assert 'mountain' in results_2023.standings
    assert 'youth' in results_2023.standings

    r=r_2023.results(stage_num=1,classification_num=1).results_table
    assert len(r) == 97
    assert r['Rider'].iloc[0] == 'Demi Vollering'
    assert r['Time'].iloc[0] == "03:16:22"
    
    r=r_2023.results(stage_num=1,classification_num=2).results_table
    assert len(r) == 23
    assert r['Rider'].iloc[0] == 'Ella Wyllie'
    assert r['Time'].iloc[0] == "03:19:38"
    
    r=r_2023.results(stage_num=1,classification_num=3).results_table
    assert len(r) == 19
    assert r['Rider'].iloc[0] == 'Demi Vollering'
    assert r['Points'].iloc[0] == 25
    
    r=r_2023.results(stage_num=1,classification_num=4).results_table
    assert len(r) == 7
    assert r['Rider'].iloc[0] == 'Demi Vollering'
    assert r['Points'].iloc[0] == 6
    
    assert len(r_2023.results(stage_num=1,classification_num=8).results_table) == 19

my_vcr.use_cassette() #Is it normal that it is no decorator???
def test_2014_giro_rosa_prologue():
	giro_rosa_2014 = RaceEdition(race_id=9064, year=2014)
	results = giro_rosa_2014.results(stage_num=0)
	assert results.results_table['Rider'].iloc[0] == 'Annemiek van Vleuten'
    
def test_giro_donne_2001():
    giro_rosa_2001 = RaceEdition(race_id=9064, year=2001, )
    results = giro_rosa_2001.results(stage_num=1)
    assert len(results.results_table) == 10

    results = giro_rosa_2001.results(stage_num=1,classification_num=3) #not existing
    assert results==None