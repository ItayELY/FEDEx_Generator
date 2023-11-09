import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from fedex_generator.commons.utils import max_key
from src.fedex_generator.Operations.Filter import Filter
from src.fedex_generator.Measures.ExceptionalityMeasure import ExceptionalityMeasure


def get_score(initial_df, source_df, result_df, desired_attribute):
    initial_size = len(initial_df['id'])
    source_size = len(source_df['id'])
    result_size = len(result_df['id'])
    f_src = Filter(source_df=source_df, source_scheme={}, attribute='popularity', operation_str='>', value=65, result_df=result_df)
    f_init = Filter(source_df=initial_df, source_scheme={}, attribute='popularity', operation_str='>', value=65, result_df=result_df)
    measure = ExceptionalityMeasure()
    scores = measure.calc_measure(f, {}, use_only_columns={})


plt.close("all")
spotify_all = pd.read_csv(r'./spotify_all.csv')
initial_size = len(spotify_all['id'])
popular = spotify_all[spotify_all.popularity > 65]
popular_size = len(popular['id'])
popular_new = popular[popular.decade >= 1990]
popular_new_size = len(popular_new['id'])

popular_new_quiet = popular_new[popular_new.loudness <= -19.5]
popular_new_quiet_size = len(popular_new_quiet['id'])


f = Filter(source_df=spotify_all, source_scheme={}, attribute='popularity', operation_str='>', value=65, result_df=popular_new_quiet)
measure = ExceptionalityMeasure()
scores = measure.calc_measure(f, {}, use_only_columns={}, attribute='energy')
print(scores)
results = measure.calc_influence(attribute='energy')
# res_energy = results[results['col'] == 'energy']
print(results['influence_vals'][0])#res_energy['influence_vals'].reset_index())

score = (0.2 * (popular_new_quiet_size/initial_size)) + 0.8 * (0.4 * scores['energy'] + 0.6 * 0.15)
print(score)
print(popular_new_quiet_size/popular_new_size)
print(popular_new_quiet_size/initial_size)