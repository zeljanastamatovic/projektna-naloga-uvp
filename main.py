import getData
from datetime import date, timedelta


print('Podatki so že naloženi. Če jih želite ponovno naložiti (kar traja približno 10 minut), vnesite »da«.')
p = input()

if p == 'da':
    danas = date.today()
    datum = danas - timedelta(days=2)
    print('Vnesite obdobje dneva, ki vas zanima (4 moznosti: »0« (med 00:00 in 6:00), »6« (med 6:00 in 12:00), »12« (med 12:00 in 18:00), »18« (med 18:00 in 24:00))')
    obdobje = input()
    if obdobje == '0' or obdobje == '6' or obdobje == '12' or obdobje == '18':
        getData.get_departures({'leto': datum.year, 'mesec': datum.month, 'dan': datum.day}, int(obdobje))
        getData.txt_file()
        getData.glavni(datum)
    else :
        print('Napačen vnos, ponovno zaženite program.')
