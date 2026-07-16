import requests
import re

odgovor = requests.get('https://24timezones.com/time-zones')
sez = []   
vsebina = odgovor.text
for najdba in re.finditer(r'<tr.*?</td>.*?</tr>', vsebina, flags=re.DOTALL):
    ime = re.findall(r'<a.*?</a>', najdba[0])[0]
    ime = re.findall(r'>.*?<', ime)[0]
    p = re.findall(r'UTC.*?<', najdba[0])[0]
    sez.append({'ime': ime[1:len(ime)-1], 'pomjerenost': p[3:len(p)-1]})


def dajzonu(niz):
    for slovar in sez:
        if slovar['ime'] == niz:
            return int(slovar['pomjerenost'])
    return 'null'