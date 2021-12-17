from first_cycling_api import Rider
roglic = Rider(18655)
results_2020 = roglic.year_results(2020)

print(results_2020.sidebar_details) 
print(results_2020.results_df.head())