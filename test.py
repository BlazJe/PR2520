from thefuzz import fuzz, process
import pandas as pd
from funkcije import load_data
from collections import defaultdict

pldp = pd.read_csv("podatki/pldp2023noo.csv", sep=";", encoding="utf-8")
pn = load_data()
stevci = ( 
    pldp[["Prometni odsek", "Ime števnega mesta"]]
    .astype(str)
    .agg(";".join, axis=1)
    .dropna()
    .unique()
    .tolist()
)

upravne = (
    pn[["UpravnaEnotaStoritve", "TekstCesteNaselja", "TekstOdsekaUlice"]]
    .astype(str)
    .agg(";".join, axis=1)
    .dropna()
    .unique()
    .tolist()
)

# s1 = "LITIJA MALA KOSTREVNICA NI ODSEKOV"
#s2 = "MP ŠENTILJ - POČIVALIŠČE ŠENTILJ"

#print(fuzz.ratio(s1, s2))  
#print(fuzz.partial_ratio(s1, s2))  
#print(fuzz.token_sort_ratio(s1, s2))
#print(fuzz.token_set_ratio(s1, s2))

# ...obstoječa koda...

# Pripravi slovarje za vsako kategorijo
import csv
slovar = defaultdict(int)
motorji = defaultdict(int)
osebna_vozila = defaultdict(int)
avtobusi = defaultdict(int)
lahki_tovornjaki = defaultdict(int)
srednji_tovornjaki = defaultdict(int)
tezki_tovornjaki = defaultdict(int)
tovornjaki_s_prik = defaultdict(int)
vlacilci = defaultdict(int)

for ime in stevci:
    match = process.extract(ime, upravne, scorer=fuzz.partial_ratio, limit=1)
    upravna_enota = match[0][0].split(";")[0]
    mask = (pldp["Prometni odsek"] + ";" + pldp["Ime števnega mesta"]) == ime
    vsa_vozila = pldp.loc[mask, "Vsa vozila (PLDP)"]
    motorji_v = pldp.loc[mask, "Motorji"]
    osebna_v = pldp.loc[mask, "Osebna vozila"]
    avtobusi_v = pldp.loc[mask, "Avtobusi"]
    lahki_v = pldp.loc[mask, "Lah. tov.  < 3,5t"]
    srednji_v = pldp.loc[mask, "Sr. tov.  3,5-7t"]
    tezki_v = pldp.loc[mask, "Tež. tov. nad 7t"]
    prik_v = pldp.loc[mask, "Tov. s prik."]
    vlacilci_v = pldp.loc[mask, "Vlačilci"]

    def sum_col(col):
        s = 0
        for v in col:
            try:
                s += int(float(str(v).replace('.', '').replace(',', '.')))
            except Exception:
                continue
        return s

    slovar[upravna_enota] += sum_col(vsa_vozila)
    motorji[upravna_enota] += sum_col(motorji_v)
    osebna_vozila[upravna_enota] += sum_col(osebna_v)
    avtobusi[upravna_enota] += sum_col(avtobusi_v)
    lahki_tovornjaki[upravna_enota] += sum_col(lahki_v)
    srednji_tovornjaki[upravna_enota] += sum_col(srednji_v)
    tezki_tovornjaki[upravna_enota] += sum_col(tezki_v)
    tovornjaki_s_prik[upravna_enota] += sum_col(prik_v)
    vlacilci[upravna_enota] += sum_col(vlacilci_v)

# Shrani rezultate v CSV datoteko
with open("vsota_vozil_po_upravnih_enotah.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Upravna enota", "Vsota vseh vozil", "Motorji", "Osebna vozila", "Avtobusi",
        "Lah. tov. < 3,5t", "Sr. tov. 3,5-7t", "Tež. tov. nad 7t", "Tov. s prik.", "Vlačilci"
    ])
    for k in slovar.keys():
        writer.writerow([
            k,
            slovar[k],
            motorji[k],
            osebna_vozila[k],
            avtobusi[k],
            lahki_tovornjaki[k],
            srednji_tovornjaki[k],
            tezki_tovornjaki[k],
            tovornjaki_s_prik[k],
            vlacilci[k]
        ])

print("Rezultati so shranjeni v vsota_vozil_po_upravnih_enotah.csv")