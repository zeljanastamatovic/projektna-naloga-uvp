import requests
import re

sez = []


def find_text():
    # sprejema podatke o letalih
    odgovor = requests.get('https://planefyi.com/aircraft/')
    v = odgovor.text
    vsebina = v[v.find('Complete database of'):]
    vsebina = vsebina[:vsebina.find('</div>\n</div>')]
    return vsebina


def naredi_sez():
    # vstavi te podatke v sezam
    vsebina = find_text()
    for najdba in re.finditer(r'<h2.*?</', vsebina):
        sez.append({'name': najdba[0][najdba[0].find('>')+1:len(najdba[0])-2]})
    i = 0
    for najdba in re.finditer(r'<span.*?<', vsebina):
        p = najdba[0][najdba[0].find('>')+1: len(najdba[0])-1]
        if i % 3 == 0:
            sez[i//3].update({'pax': p[:p.find(' ')]})
        if i % 3 == 1:
            sez[i//3].update({'range': p[:p.find(' ')].replace(',', '')})
        if i % 3 == 2:
            sez[i//3].update({'id': p})
        i += 1


naredi_sez()


def find_aircrafts(iata, name):
    # Za letalo z danim imenom in iata kodo poišče njegov doseg in povprečno število potnikov
    for slovar in sez:
        if slovar['id'] == iata:
            return slovar
        if name in slovar['name'] or slovar['name'] in name:
            return slovar
    if name[name.find(' ')+1:].find(' ') >= 0:
        name = name[:name.find(' ') + name[name.find(' ')+1:].find(' ') + 1]
        return find_aircrafts(iata, name)
    if name.find('(') >= 0:
        return find_aircrafts(iata, name[:name.find('(')])
    if name.find('-') >= 0:
        return find_aircrafts(iata, name[:name.find('-')])
