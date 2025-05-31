import pandas as pd
import os
import re

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