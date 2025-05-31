import pandas as pd
import os
import re
import numpy as np
import calendar
import json
import pickle

def load_data():
    directory = './podatki'
    data = []
    max_zaporedna_stevilka = 0  

    pattern = re.compile(r"^pn\d{4}\.csv$", re.IGNORECASE)

    for filename in os.listdir(directory):
        if pattern.match(filename):
            filepath = os.path.join(directory, filename)
            try:
                frame = pd.read_csv(
                    filepath,
                    delimiter=';',
                    encoding='utf-8',
                )
                frame['ZaporednaStevilkaPN'] += max_zaporedna_stevilka
                max_zaporedna_stevilka = frame['ZaporednaStevilkaPN'].max()  

                data.append(frame)
            except Exception as e:
                print(f"Napaka pri branju {filename}: {str(e)}")
                continue

    if data:
        combined_data = pd.concat(data, ignore_index=True)
        return combined_data
    else:
        return pd.DataFrame() 

def stack_data(combined_data, atribute):
    unique_accidents = combined_data.groupby('ZaporednaStevilkaPN').first()

    stacked_data = unique_accidents.groupby([atribute, 'KlasifikacijaNesrece']).size().unstack(fill_value=0)

    stacked_data['Total'] = stacked_data.sum(axis=1)
    stacked_data = stacked_data.sort_values(by='Total', ascending=False).drop(columns=['Total'])

    ordered_columns = ['Z MATERIALNO ŠKODO', 'Z LAŽJO TELESNO POŠKODBO', 'S HUDO TELESNO POŠKODBO', 'S SMRTNIM IZIDOM']
    stacked_data = stacked_data[ordered_columns]
    return stacked_data

def get_monthly_stacked(combined_data):
    unique_accidents = combined_data.groupby('ZaporednaStevilkaPN').first()
    unique_accidents['DatumPN'] = pd.to_datetime(unique_accidents['DatumPN'], format='%d.%m.%Y')
    unique_accidents['Month'] = unique_accidents['DatumPN'].dt.month
    years = unique_accidents['DatumPN'].dt.year.nunique()
    stacked = unique_accidents.groupby(['Month', 'KlasifikacijaNesrece']).size().unstack(fill_value=0)
    ordered_columns = ['Z MATERIALNO ŠKODO', 'Z LAŽJO TELESNO POŠKODBO', 'S HUDO TELESNO POŠKODBO', 'S SMRTNIM IZIDOM']
    stacked[ordered_columns] = stacked[ordered_columns] / years
    stacked = stacked[ordered_columns]
    stacked.index = pd.CategoricalIndex(
        [calendar.month_abbr[m] for m in stacked.index],
        categories=[calendar.month_abbr[m] for m in range(1, 13)],
        ordered=True
    )
    stacked = stacked.sort_index()
    return stacked

def get_weekday_stacked(combined_data):
    unique_accidents = combined_data.groupby('ZaporednaStevilkaPN').first()
    unique_accidents['DatumPN'] = pd.to_datetime(unique_accidents['DatumPN'], format='%d.%m.%Y')
    unique_accidents['Weekday'] = unique_accidents['DatumPN'].dt.day_name()
    days = (unique_accidents['DatumPN'].max() - unique_accidents['DatumPN'].min()).days
    weeks = days // 7
    stacked = unique_accidents.groupby(['Weekday', 'KlasifikacijaNesrece']).size().unstack(fill_value=0)
    ordered_columns = ['Z MATERIALNO ŠKODO', 'Z LAŽJO TELESNO POŠKODBO', 'S HUDO TELESNO POŠKODBO', 'S SMRTNIM IZIDOM']
    stacked[ordered_columns] = stacked[ordered_columns] / weeks
    stacked = stacked[ordered_columns]
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    stacked.index = pd.CategoricalIndex(stacked.index, categories=order, ordered=True)
    stacked = stacked.sort_index()
    return stacked

def get_holiday_dict(first_date, last_date):
    holidays = dict()
    def add_holiday(date, name):
        if date < first_date or date > last_date:
            return
        if date in holidays:
            if isinstance(holidays[date], list):
                holidays[date].append(name)
            else:
                holidays[date] = [holidays[date], name]
        else:
            holidays[date] = name

    def get_easter_date(year):
        a = year % 19
        b = year // 100
        c = year % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        month = (h + l - 7 * m + 114) // 31
        day = ((h + l - 7 * m + 114) % 31) + 1
        return month, day
    
    for year in range(first_date.year, last_date.year + 1):
        add_holiday(pd.to_datetime(f"{year}-01-01"), 'novo leto')
        add_holiday(pd.to_datetime(f"{year}-01-02"), 'novo leto')
        add_holiday(pd.to_datetime(f"{year}-02-08"), 'Prešernov dan, slovenski kulturni praznik')
        add_holiday(pd.to_datetime(f"{year}-04-27"), 'dan upora proti okupatorju')
        add_holiday(pd.to_datetime(f"{year}-05-01"), 'praznik dela')
        add_holiday(pd.to_datetime(f"{year}-05-02"), 'praznik dela')
        add_holiday(pd.to_datetime(f"{year}-06-08"), 'dan Primoža Trubarja')
        add_holiday(pd.to_datetime(f"{year}-06-25"), 'dan državnosti')
        add_holiday(pd.to_datetime(f"{year}-08-15"), 'Marijino vnebovzetje')
        add_holiday(pd.to_datetime(f"{year}-08-17"), 'združitev prekmurskih Slovencev z matičnim narodom')
        add_holiday(pd.to_datetime(f"{year}-09-15"), 'priključitev Primorske k matični domovini')
        add_holiday(pd.to_datetime(f"{year}-09-23"), 'dan slovenskega športa')
        add_holiday(pd.to_datetime(f"{year}-10-25"), 'dan suverenosti')
        add_holiday(pd.to_datetime(f"{year}-10-31"), 'dan reformacije')
        add_holiday(pd.to_datetime(f"{year}-11-01"), 'dan spomina na mrtve')
        add_holiday(pd.to_datetime(f"{year}-11-10"), 'dan znanosti')
        add_holiday(pd.to_datetime(f"{year}-11-23"), 'dan Rudolfa Maistra')
        add_holiday(pd.to_datetime(f"{year}-12-25"), 'božič')
        add_holiday(pd.to_datetime(f"{year}-12-26"), 'dan samostojnosti in enotnosti')
        month, day = get_easter_date(year)
        easter_date = pd.to_datetime(f"{year}-{month}-{day}")
        add_holiday(easter_date, 'velikonočna nedelja')
        add_holiday(easter_date + pd.Timedelta(days=1), 'velikonočni ponedeljek')
        add_holiday(easter_date + pd.Timedelta(days=49), 'binkoštna nedelja')
    return holidays

def get_holiday_stacked(combined_data):

    unique_accidents = combined_data.groupby('ZaporednaStevilkaPN').first()
    unique_accidents['DatumPN'] = pd.to_datetime(unique_accidents['DatumPN'], format='%d.%m.%Y')
    first_date = unique_accidents['DatumPN'].min()
    last_date = unique_accidents['DatumPN'].max()
    days = (last_date - first_date).days + 1

    holidays = get_holiday_dict(first_date, last_date)
    unique_accidents['Holiday'] = unique_accidents['DatumPN'].map(holidays)
    unique_accidents = unique_accidents.explode('Holiday')
    unique_accidents['Holiday'] = unique_accidents['Holiday'].fillna('ni praznik')

    years = unique_accidents['DatumPN'].dt.year.nunique()

    def get_holiday_occurence_count(holiday):
        if holiday == 'ni praznik':
            praznicni_dnevi = set([d for d in holidays])
            return days - len(praznicni_dnevi)
        i = 0
        for date in holidays:
            if isinstance(holidays[date], list):
                if holiday in holidays[date]:
                    i += 1
            else:
                if holidays[date] == holiday:
                    i += 1
        return i

    stacked = unique_accidents.groupby(['Holiday', 'KlasifikacijaNesrece'], dropna=False).size().unstack(fill_value=0)
    ordered_columns = ['Z MATERIALNO ŠKODO', 'Z LAŽJO TELESNO POŠKODBO', 'S HUDO TELESNO POŠKODBO', 'S SMRTNIM IZIDOM']
    for col in ordered_columns:
        stacked[col] = stacked.apply(
            lambda row: row[col] / get_holiday_occurence_count(row.name),
            axis=1
        )
    stacked = stacked[ordered_columns]
    stacked['Total'] = stacked.sum(axis=1)
    stacked = stacked.sort_values('Total', ascending=False).drop(columns=['Total'])
    return stacked

