#!/usr/bin/env python
import os, sys, calendar

def months2season(months):
    '''convert a list of month numbers into a season name of month initials, e.g. [3,4,5] -> 'MAM'. '''
    month_names = ['Dec', 'Jan', 'Feb',
        'Mar', 'Apr', 'May',
        'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov']
    if isinstance(months, int): # months is an integer, e.g. months = 3
        season = month_names[months%12]
    elif len(months) == 1: # months is a length 1 sequence, e.g. months = [12]
        season = month_names[months[0]%12]
    elif len(months) == 12: # months cover every month, e.g. months = range(1,13)
        season = 'annual'
    else:
        season = ''.join([month_names[m%12][0] for m in months])

    return season

def month2name(months):
    '''convert a list of month numbers into a list of month names, e.g. [3,4,5] -> ['Mar', 'Apr', 'May']. '''
    if isinstance(months, int): # months is an integer, e.g. months = 3
        mon_names = calendar.month_name[(months-1)%12+1][0:3]
    else:
        mon_names = [calendar.month_name[(month-1)%12+1][0:3] for month in months]

    return mon_names
def season2months(season):
    '''convert a name of season into a list of month numbers, e.g. 'MAM' -> [3, 4, 5] '''
    months_full = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    month_names_full = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
              'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    season_full = 'JFMAMJJASONDJFMAMJ'
    if season.lower() == 'annual':
        months = list(range(1, 13))
    elif season in month_names_full:
        months = [months_full[i] for i in range(len(months_full))
            if month_names_full[i]==season][0]
    else:
        i = season_full.find(season)
        N = len(season)
        months = months_full[i:i+N]
    return months

def sel_season(ds, season='annual'):
    """given input dataset/dataarray, select data of specified season"""
    L = False
    months = season2months(season)
    for month in months:
        L = L | (ds.time.dt.month==month)
    return ds.isel(time=L)

if __name__ == '__main__':
    if 'test' in sys.argv:
        from xdata import ds
        season = 'annual'
        kws = [s for s in sys.argv if s.startswith('season=')]
        if kws:
            season = kws[-1].split('=')[-1]
        ds_ = ds.pipe(sel_season, season=season)
        print(f'{season = }')
        print()
        print(f'{ds_ = }')
        print()
        print(f'{ds_.time = }')


