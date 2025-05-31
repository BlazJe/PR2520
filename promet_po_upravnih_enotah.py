import pandas as pd
from thefuzz import fuzz, process
from funkcije import load_data
from collections import defaultdict
import csv

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

def sum_col(col):
    return sum(
        int(float(str(v).replace('.', '').replace(',', '.')))
        for v in col if pd.notnull(v) and str(v).strip() != ""
    )

rezultati = defaultdict(int)

for ime in stevci:
    match = process.extractOne(ime, upravne, scorer=fuzz.partial_ratio)
    upravna_enota = match[0].split(";")[0] if match else "NEZNANO"
    mask = (pldp["Prometni odsek"] + ";" + pldp["Ime števnega mesta"]) == ime
    rezultati[upravna_enota] += sum_col(pldp.loc[mask, "Vsa vozila (PLDP)"])

with open("vsota_vozil_po_upravnih_enotah.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Upravna enota", "Vsota vseh vozil (PLDP)"])
    for enota in sorted(rezultati.keys()):
        writer.writerow([enota, rezultati[enota]])

print("Rezultati so shranjeni v vsota_vozil_po_upravnih_enotah.csv")