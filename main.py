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
    measure_src = ExceptionalityMeasure()
    interest_src = measure_src.calc_measure(f_src, {}, use_only_columns={}, attribute=desired_attribute)
    bins_src = measure_src.calc_influence(attribute=desired_attribute)['influence_vals'][1]
    max_bin = max(bins_src, key=bins_src.get)
    max_bin_val_src = bins_src[max_bin]

    measure_init = ExceptionalityMeasure()
    interest_init = measure_init.calc_measure(f_init, {}, use_only_columns={}, custom_bins=list(bins_src.keys())
                                              , attribute=desired_attribute)
    bins_init = measure_init.calc_influence(attribute=desired_attribute)['influence_vals'][1]
    # max_bin = max(bins_src, key=bins_src.get)
    excluded = [b for b in bins_src if b not in bins_init.keys()]
    for e in excluded:
        bins_init[e] = 0
    max_bin_val_init = bins_init[max_bin]
    local_score = (0.2 * (result_size/source_size)) + 0.8 * (0.2 * interest_src + 0.8 * max_bin_val_src)
    absolute_score = (0.2 * (result_size / initial_size)) + 0.8 * (0.2 * interest_init + 0.8 * max_bin_val_init)
    print(f'attribute {desired_attribute}: \ninterest_init={interest_init}\ninterest_src={interest_src}'
          f'\nmax_bin={max_bin}\nmax_bin_val_init={max_bin_val_init}\nmax_bin_val_src={max_bin_val_src}\n'
          f'local_score={local_score}\nabsolute_score={absolute_score}')




plt.close("all")
spotify_all = pd.read_csv(r'./spotify_all.csv')
initial_size = len(spotify_all['id'])
popular = spotify_all[spotify_all.popularity > 65]
popular_size = len(popular['id'])
popular_new = popular[popular.decade >= 1990]
popular_new_size = len(popular_new['id'])

popular_new_quiet = popular_new[popular_new.loudness <= -19.5]
popular_new_quiet_size = len(popular_new_quiet['id'])

get_score(spotify_all, popular_new, popular_new_quiet, 'energy')
print("*********************************************")
get_score(spotify_all, popular_new, popular_new_quiet, 'valence')