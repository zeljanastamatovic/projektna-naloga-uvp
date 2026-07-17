import requests
import time
import re
import csv
from aircrafts import find_aircrafts
from datetime import date, timedelta


header = ['flightId', "finalStatus", "flightNumber", "arrivalAirportFS", "divertedAirport", 'flightDuration', 'carrier', 'equipment', 'depTimeScheduled', 'depTimeActual', 'arrTimeScheduled', 'arrTimeActual']
sezArrival = []
sezEquipment = []
headerEquipment = ['name', 'pax', 'range', 'id']
headerArrival = ["fs", 'iata', 'name', 'city', 'country', 'timeZoneRegionName', 'regionName']


def get_departures(datum, obdobje):
    # poišče spletno stran z odhodi za določen datum in jih shrani v HTML datoteko 
    odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year={datum['leto']}&month={datum['mesec']}&date={datum['dan']}&hour={obdobje}')
    vsebina = odgovor.text
    with open("hndDepartures.html", "w", encoding="utf-8") as dat:
        print(vsebina, file=dat)


def txt_file():
    # poišče URL za vsak let in jih shrani v txt datoteko.
    with open('urls.txt', 'w', encoding='utf-8') as d:
        with open("hndDepartures.html", encoding="utf-8") as dat:
            vsebina = dat.read()
            indexes = [x.start() for x in re.finditer('"url"', vsebina)]
            for index in indexes:
                url = "https://www.flightstats.com/v2" + \
                    vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('"')]
                # preveri če ni  code share (isti let z drugo številko)
                if vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('}}')] \
                    < vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('Codeshare')]:
                    print(url, file=d)


def izvleci_info(niz, vsebina):
    # iz vsebine nalazi kolika je vrednost elementa
    try:
        p = re.findall(f'"{niz}"'+r':.*?[,}]', vsebina)[0]
        n = p[p.find(':')+1:len(p)-1]
        if niz == 'flightDuration': 
            #pretvori niz oblike '..h..m' v minute
            if 'h' in n:
                if 'm' in n:
                    return int(n[1:n.find('h')]) * 60 + int(n[n.find(' ') + 1: n.find('m')])
                else:
                    return int(n[1:n.find('h')]) * 60
            else:
                return int(n[1:n.find('m')])
        if n[0] in '\'"':
            return n[1:len(n)-1]
        return n
    except:
        return 'null'


def izvleci_equipment(vsebina):
    # najde informacije o uporabljenem letalu
    t = re.findall('"equipment"'+':.*?}', vsebina)[0]
    name = izvleci_info('name', t)
    iata = izvleci_info('iata', t)
    return find_aircrafts(iata, name)


def naredi_slovar(vsebina):
    slovar = {'flightId': [], "finalStatus": [], "flightNumber": [],
              "arrivalAirportFS": [], "divertedAirport": [],
              'flightDuration': [], 'carrier': [], 'equipment': [],
              'depTimeScheduled': [], 'depTimeActual': [],
              'arrTimeScheduled': [], 'arrTimeActual': []}
    niz1 = ['flightId', "finalStatus", "flightNumber", "arrivalAirportFS",
            "divertedAirport", 'flightDuration']

    slovar['depTimeScheduled'] = izvleci_info('time24', re.findall('"time24":.*?},', vsebina)[0])
    slovar['depTimeActual'] = izvleci_info('time24', re.findall('"time24":.*?},', vsebina)[1])
    try:
        slovar['arrTimeScheduled'] = izvleci_info('time24', re.findall('"time24":.*?},', vsebina)[2])
    except:
        slovar['arrTimeScheduled'] = slovar['depTimeActual']
        slovar['depTimeActual'] = 'null'
    try:
        slovar['arrTimeActual'] = izvleci_info('time24', re.findall('"time24":.*?},', vsebina)[3])
    except:
        slovar['arrTimeActual'] = 'null'

    for j in niz1:
        if j == 'divertedAirport':
            p = izvleci_info(j, vsebina)
            if p == 'null':
                slovar[j] = p
            else:
                slovar[j] = p[7:10]
                slovar['arrTimeActual'], slovar['depTimeActual'] = \
                    slovar['depTimeActual'], slovar['arrTimeActual']
                slovar['arrTimeScheduled'], slovar['depTimeScheduled'] = \
                    slovar['depTimeScheduled'], slovar['arrTimeScheduled']
        else:
            slovar[j] = izvleci_info(j, vsebina)

    slovar['carrier'] = izvleci_info('name', re.findall(
        '"carrier":{"name":.*?}', vsebina)[0])

    slovarEquipment = izvleci_equipment(vsebina)
    if slovarEquipment not in sezEquipment:
        sezEquipment.append(slovarEquipment)
    slovar['equipment'] = slovarEquipment['id']
    return slovar


def izvleci_arrivalAirport(vsebina):
    # najde informacije o letališču prihoda 
    t = re.findall('"arrivalAirport":.*?}', vsebina)[0]
    slovar = {}
    for i in headerArrival:
        slovar.update({i: izvleci_info(i, t)})
    return slovar


def csv_file(niz1, niz2, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=niz2)
        writer.writeheader()
        for i in niz1:
            writer.writerow(i)


def preveri_url(niz, datum):
    p = re.findall('date=.*?&', niz)[0]
    p = p[5:len(p)-1]
    if int(p) == datum.day:
        return True
    return False


def glavni(datum):
    dat = open("urls.txt", encoding='utf8')
    n = dat.read().count('\n')
    dat.close()
    with open("urls.txt", encoding='utf8')as dat:
        f = open("podatki/flights.csv", 'w', newline='', encoding='utf-8')
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        i = 1
        for vrstica in dat:
            print(f'{i}/{n}')
            i += 1
            vrstica = vrstica[:len(vrstica)-1]
            vrstica = vrstica.replace('\\u0026', '&')
            if preveri_url(vrstica, datum):
                
                odgovor = requests.get(vrstica)
                while odgovor.status_code == 504:
                    time.sleep(4)
                    odgovor = requests.get(vrstica)
                if odgovor.status_code == 403:
                    print('Prosim počakajte')
                    time.sleep(90)
                    odgovor = requests.get(vrstica)
                if odgovor.status_code == 200:
                    vsebina = odgovor.text
                    p = izvleci_arrivalAirport(vsebina)
                    if p not in sezArrival:
                        sezArrival.append(p)
                    writer.writerow(naredi_slovar(vsebina))
        f.close()
    csv_file(sezArrival, headerArrival, 'podatki/arrivalAirport.csv')
    csv_file(sezEquipment, headerEquipment, 'podatki/equipment.csv')
