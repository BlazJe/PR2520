# Modeli za napovedovanje vrednosti generirani z naivnim bayesom.

## kratka predstavitev podatkov v modelu

Od vseh originalnih podatkov so izbrisani stolpci (zaradi nepomemnosti pri napovedovanju):
- datum prometne nesreče (se skoraj vsakič spreminja)
- zaporedna številka osebe v prometni nesreči (vsaka oseba unikatno številko) 
- vozniški staz v mesecih (podatek nepomemben, ker obstaja podatek vozniški staz v letih)
- zaporedna številka nesreče (unikatne številke nesreče)

Od preostalih podatkov so bili še izbrisani tisti, ki niso imeli vrednosti:
- NaN vrednosti
- 0 vrednosti v koordinatah
- -1 vrednost pri starosti

Večina vrstic je že prisotnih v diskretni obliki. Zvezne spremenljivke pa so bile diskritizirane na intervale:
- ura nesreče iz ura:minuta -> ura (23.15 -> 23)
- koordinate na intervale velike 10000 (230000 -> 23 pomen: koordinata od 230000-239999)
- starost na intervale velike 10 (25 -> 2 pomen: starost od 20-29 let)
- vozniški staz v letih na intervale velike 10 (25 -> 2 pomen: vozniški staz od 20-29 let)
- vrednost alkotesta in vrednost strokovnega pregleda na intervale velike 0.1 in pretvorba v cela števila(1.12 - 11 pomen vrednost 1.1 - 1.19)

Po pretvorbi vseh spremenljivk v diskretne, tiste ki so predstavljeni kot nizi mapiarmo v celoštevilske vrednosti v obliki json datotek.

Modeli nimajo privzete možnosti za shranjevanje, zato se za zhranjevanje natreniranih modelov (obljektov) uporabljajo pkl datoteke.


## uspešnost modelov

Modeli zo bili generirani z modelom naivni bayes.
Med generiranimi modeli se vredu odnesejo tisti, ki imajo na izbiro samo 2 ali 3 možne napovedi.
V našem primeru VNaselju, spol, povzročitelj in lokacija. Veliko modelov pa napoveduje zelo slabo, kar
pa je lahko problem izbire modela ali pa pomeni, da podatki za tisti stolpec nimajo neko povezave z ostalimi atributi.

Stolpični diagram prikaza natančnosti modelov.

![Graf](slike/accuracy_graph.png "Slika grafa natančnosti")

# Modeli za napovedovanje vrednosti generirani z random forest.

Podatki so preprocesirani enako kot v zgorjnem opisu. Pri modelu se uporablja 200 dreves, ki pa precej bolje napovedujejo kot modeli zgenerirani
z naivinim bajesom. Problem random forest modelov je, da potrebujejo za učenje veliko več pomnilnika in ker tudi ta model ne podpira shranjevanja modelov se uporabljajo pkl datoteke.
Modeli zgenerirni z metodo random forest niso objavljeni na repozitoriju zaradi njihove velikosti (30GB), zato če jih želite preizkusiti jih je treba zgenerirati lokalno.
Pri metodi je 5 modelov izpuščenih, saj so preveč računsko zahtevni in zavzamejo preveč prostorja ter pomnilnika (32GB RAM-a in dodatnih 120GB swap pomnilnika za generiranje modela).
Razlog za tako zahtevne modele pa je da imajo čez 5000 različnih možnosti za atribute. Poleg modelov pa je prikazan še graf za vsak model, ki vzame eno izmed 200 dreves in ga prikaže
do globine 2, da lahko približno vidimo kateri atributi so najpomembnejši pri napovedovanju. Prikaz pa ni najboljši saj se za generiranje modelov uporablja mapping namesto onehot encodinga 
in je prikaz na grafih precej nesmiselen (vrednost atributa <= 4.5 pri diskretnih vrednostih). 

Stolpični diagram prikaza natančnosti modelov.

![Graf](slike/accuracy_graph.png "Slika grafa natančnosti")

# Napovedovanje

Pri obeh modelih lahko napovedujemo ciljne spremenljivke brez vseh podatkov. Če kateri od podatkov manjka ga nadomestimo z vrednostjo "-1" in se ob napovedi zamenja z največkrat ponovljeno vrednostjo v tistem stolpcu (tudi pri naivnem bayesu,
čeprav to model sam podpira). Podatke ki uporabnik vnese se spet pretvorijo preko mappingov v celoštevilske vrednosti, preden se izvede napoved. Ob poklicani napovedi se naloži željen model in vrne napovedano vrednost.
Na spletni aplikaciji se uporabljajo slabši modeli z naivnim bajesom, ker so modeli generirani z random forest-om preveliki. 

## ideja ustvarjanja modelov

Modele za napovedovanje katerih koli stolpcev želimo realizirati, ker bi lahko bili uporabni pri svetovalnih sistemih
za klice v sili. Ob klicu pridobijo določene podatke po navadi pa ne vseh. Modele bi lakho uporabili za napovedovanje 
teh manjkajočih podatkov. Glede na napovedi bi se lahko v naprej pripravili za najbolj verjetno stanje, ki jih čaka.

