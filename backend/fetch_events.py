#!/usr/bin/python
import os
import json
import pandas as pd
from tqdm import tqdm
import inspect
from typing import List, Callable

import config

from scraper_util import clean_date_format, clean_starttime, clean_endtime, save_json


def drop_duplicate_events(df):
    """
    Function to group dataframe, use all new information from the latest row
    but keep the ``event_index`` from the first one
    """
    df = df.sort_values('event_index', na_position='last')
    event_index = df.event_index.iloc[0]
    r = df.iloc[-1].to_dict()
    r['event_index'] = event_index
    return r


def find_scrapers(module) -> List[Callable]:
    """
    Build a list of 'scraper' functions contained in a module.
    These consist of every function public function (i.e., does not begin with_)
    that is defined, but not imported, in the module

    :param module: Module containing local
    :return: List of scraper functions, each of which returns a List of Event dicts
    """

    def predicate(event):
        return inspect.isfunction(event) and inspect.getmodule(event) == module

    scrapers = inspect.getmembers(module, predicate)
    return [s[1] for s in scrapers if not s[0].startswith('_')]


def fetch_all_events(scraper_module):
    events = []
    fetch_fns = find_scrapers(scraper_module)

    for f in tqdm(fetch_fns):
        try:
            events.extend(f())
        except:
            print(f)

    events_df = pd.DataFrame(events).fillna('')
    events_df['date_dt'] = events_df['date'].map(
        lambda x: clean_date_format(x))
    events_df.loc[:, 'starttime'] = events_df.apply(clean_starttime, axis=1)
    if len(events_df.loc[events_df.endtime == '']) > 0:
        events_df.loc[events_df.endtime == '', 'endtime'] = events_df.loc[events_df.endtime == ''].apply(
            clean_endtime, axis=1
        )

    # save data to json if not data in ``data`` folder
    group_columns = ['owner', 'title', 'date_dt', 'starttime']
    if not os.path.exists(config.PATH_DATA):
        # save events
        events_df = events_df.drop_duplicates(
            subset=group_columns, keep='first')
        events_df['event_index'] = list(range(len(events_df)))
        events_json = events_df.to_dict(orient='records')
        save_json(events_json, config.PATH_DATA)

    # if data already exist, append new fetched data to an existing data
    else:
        # save events
        events_json = json.loads(open(config.PATH_DATA, 'r').read())
        events_former_df = pd.DataFrame(events_json)
        events_df = pd.concat(
            (events_former_df, events_df), axis=0, sort=False
        )
        events_df = pd.DataFrame([drop_duplicate_events(df_)
                                  for _, df_ in events_df.groupby(group_columns)])
        events_df.sort_values('event_index', na_position='last', inplace=True)
        event_idx_begin = events_former_df['event_index'].max() + 1
        event_idx_end = event_idx_begin + events_df.event_index.isnull().sum()
        if event_idx_begin != event_idx_end:
            events_df.loc[pd.isnull(events_df.event_index), 'event_index'] = list(
                range(event_idx_begin, event_idx_end)
            )
        events_df.loc[:, 'event_index'] = events_df.loc[:,
                                                        'event_index'].astype(int)
        events_json = events_df.to_dict(orient='records')
        save_json(events_json, config.PATH_DATA)


if __name__ == '__main__':
    fetch_all_events(config.scrapers)
