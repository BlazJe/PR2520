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

## ideja ustvarjanja modelov

Modele za napovedovanje katerih koli stolpcev želimo realizirati, ker bi lahko bili uporabni pri svetovalnih sistemih
za klice v sili. Ob klicu pridobijo določene podatke po navadi pa ne vseh. Modele bi lakho uporabili za napovedovanje 
teh manjkajočih podatkov. Glede na napovedi bi se lahko v naprej pripravili za najbolj verjetno stanje, ki jih čaka.

## uspešnost modelov

Modeli zo bili generirani z modelom naivni bayes.
Med generiranimi modeli se vredu odnesejo tisti, ki imajo na izbiro samo 2 ali 3 možne napovedi.
V našem primeru VNaselju, spol, povzročitelj in lokacija. Veliko modelov pa napoveduje zelo slabo, kar
pa je lahko problem izbire modela ali pa pomeni, da podatki za tisti stolpec nimajo neko povezave z ostalimi atributi.

Stolpični diagram prikaza natančnosti modelov.

![slika grafa natančnosti](https://github.com/BlazJe/PR2520/blob/main/accuracy_graph.png)

