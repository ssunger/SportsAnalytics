import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from time import sleep

website = lambda start, end: [f"https://en.wikipedia.org/wiki/UFC_{i}" for i in range(start, end)]


def get_top_level_data(end, start=20, get_fight_card_stats=False, both=True, avg_pause=.6):
    """

    @param end: integer
    @param start : integer
    @param get_fight_card_stats :
    @param both : boolean
    @param avg_pause : float
    """

    def add_d_set(df_use, name):
        df = df_use.copy()
        df.insert(0, "Event", f"UFC{name}")
        return df

    vals = website(start, end)
    rets_df = []
    if both:
        rets_df_2 = []

    for j, pause in zip(vals, np.random.poisson(avg_pause, len(vals))):
        print(j)
        if get_fight_card_stats and not both:
            rets_df.append(add_d_set(pd.read_html(j)[2], j))
        elif get_fight_card_stats and both:
            d = pd.read_html(j)
            rets_df.append(add_d_set(d[2], j))
            rets_df_2.append(add_d_set(d[0], j))
        else:
            rets_df.append(add_d_set(pd.read_html(j)[2], j))
            sleep(pause)
    return pd.concat(rets_df, axis=0)