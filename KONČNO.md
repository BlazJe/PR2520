# Končno poročilo o opravljenem delu
## Analiza podatkov



## Napovedovalni modeli



## Časovna analiza

### Povzetek

Predmet analize so časovni vzorci v prometnih nesrečah. Fokus je na ugotavljanju, kako so porazdeljene prometne nesreče glede na mesec, dan v tednu, ali je dan praznik in iskanje trendov s tekočim povprečjem.

### Podatki

Stolpec `DatumPN` je pretvorjen v `Pandas` `DateTime` objekt za lažjo manipulacijo z datumi. Dodani so tudi stolpci za dan, mesec, leto, in dan v tednu.

### Najnevarnejši meseci

Nesreče so grupirane po mesecu v letu in deljene s številom let v podatkih.

![meseci](slike/nesrece_mesecno.png "Nesreče povprečno na mesec")

**Ugotovitev:** Največ nesreč se zgodi v poletni polovici leta, med mesecem majem in oktobrom - približno `1700` na mesec. 

### Najnevarnejši dnevi v tednu

Nesreče so grupirane po dnevu v tednu in deljene s številom tednov v podatkih.

![dnevi_v_tednu](slike/nesrece_dnevno.png "Nesreče povprečno na dan v tednu")

**Ugotovitev:** Na vikend se zgodi najmanj nesreč, v petek pa največ. Na najnevarnejši dan, petek, se zgodi skoraj dvakrat toliko nesreč kot na najmanj nevaren dan, nedeljo - približno `30` nesreč razlike.

### Vpliv praznikov

Ustvarjen je slovar datumov in praznikov v Sloveniji, dobljenih iz `https://www.gov.si/teme/drzavni-prazniki-in-dela-prosti-dnevi/`. Nesreče so nato grupirane po praznikih in deljene s številom praznika v podatkih.

![prazniki](slike/nesrece_prazniki.png "Nesreče povprečno na praznik")

**Ugotovitev:** Na večino praznikov se zgodi manj nesreč kot na tipičen dan, ko ni praznika. Najmanj nesreč se zgodi na božič, največ pa na priključitev Primorske k matični domovini.

### Dela prosti dnevi

Dodan je stolpec, ki opisuje, ali se je nesreča zgodila na dela prost dan. Nesreče so nato grupirane po tem, ali so se zgodile na dela prost dan, in deljene s številom teh dni.

![dela_prosti_dnevi](slike/nesrece_dela_prost_dan.png)

**Ugotovitev:** Dejstvo, ali je dan dela prost, ima velik vpliv na število nesreč. Na dela prost dan se zgodi manj nesreč, približno `20` nesreč manj, kot na normalen dan.

### Trendi

Nesreče so grupirane po datumu in prikazane na grafu s tekočim povprečjem zadnjih `100` in `365` dni.

![rolling_average](slike/nesrece_rolling_average.png)

**Ugotovitev:** Povprečje zadnjih `100` dni pokaže tudi sezonsko nihanje, ker se več nesreč dogaja med poletjem kot zimo. `365`-dnevno povprečje medtem pokaže splošni trend naraščanja števila nesreč, z upadom med leti `2020` in `2022`, v času COVID-19.