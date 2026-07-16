import requests
import time
import re
import csv
from aircrafts import find_aircrafts


header = ['flightId', "finalStatus", "flightNumber", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration', 'carrier', 'equipment', 'depTimeScheduled', 'depTimeActual', 'arrTimeScheduled', 'arrTimeActual']
sezArrival = []
sezEquipment = []
headerEquipment = ['name', 'pax', 'range', 'id']
headerArrival = ["fs", 'iata', 'name', 'city', 'country', 'timeZoneRegionName', 'regionName']

datum = {'leto': 2026, 'mesec': 7, 'dan': 14}  # datum mora biti najvise 3 dana pre trenutnog datuma
obdobje = 12  # 4 moznosti: 0 (med 00:00 in 6:00), 6 (med 6:00 in 12:00), 12 (med 12:00 in 18:00), 18 (med 18:00 in 24:00)


def get_departures(datum, obdobje):
    odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year={datum['leto']}&month={datum['mesec']}&date={datum['dan']}&hour={obdobje}')
    vsebina = odgovor.text
    with open("hndDepartures.html", "w", encoding="utf-8") as dat:
        print(vsebina, file=dat)


def txt_file():
    with open('urls.txt', 'w', encoding='utf-8') as d:
        with open("hndDepartures.html", encoding="utf-8") as dat:
            vsebina = dat.read()
            indexes = [x.start() for x in re.finditer('"url"', vsebina)]
            for index in indexes:
                url = "https://www.flightstats.com/v2" + \
                    vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('"')]
                # gleda da li je code share
                if vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('}}')] \
                    < vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('Codeshare')]:
                    print(url, file=d)


def izdvoj(niz, vsebina):
    p = re.findall(f'"{niz}"'+r':.*?[,}]', vsebina)[0]
    n = p[p.find(':')+1:len(p)-1]
    if niz == 'flightDuration':
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


def izdvoj_equipment(vsebina):
    t = re.findall('"equipment"'+':.*?}', vsebina)[0]
    name = izdvoj('name',t)
    iata = izdvoj('iata', t)
    return find_aircrafts(iata, name)


def staviuslovar(vsebina):
    slovar = {'flightId': [], "finalStatus": [], "flightNumber": [], "arrivalAirportFS": [], "divertedAirport": [], "operatedBy": [], "gate": [], "terminal": [], 'flightDuration': [], 'carrier': [], 'equipment': [], 'depTimeScheduled': [], 'depTimeActual': [], 'arrTimeScheduled': [], 'arrTimeActual': []}
    niz1 = ['flightId', "finalStatus", "flightNumber", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration']
    
    slovar['depTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[0])
    slovar['depTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[1])
    try:
        slovar['arrTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[2])
    except:
        slovar['arrTimeScheduled'] = slovar['depTimeActual']
        slovar['depTimeActual'] = 'null'
    try:
        slovar['arrTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[3])
    except:
        slovar['arrTimeActual'] = 'null'
    for j in niz1:
        if j == 'divertedAirport':
            p = izdvoj(j, vsebina)
            if p == 'null':
                slovar[j] = p
            else:
                slovar[j] = p[7:10]
                slovar['arrTimeActual'], slovar['depTimeActual'] = \
                    slovar['depTimeActual'], slovar['arrTimeActual']
                slovar['arrTimeScheduled'], slovar['depTimeScheduled'] = \
                    slovar['depTimeScheduled'], slovar['arrTimeScheduled']
        else:
            slovar[j] = izdvoj(j, vsebina)
        
    slovar['carrier'] = izdvoj('name', re.findall('"carrier":{"name":.*?}', vsebina)[0])
    slovarEquipment = izdvoj_equipment(vsebina)
    if slovarEquipment not in sezEquipment:
        sezEquipment.append(slovarEquipment)
    slovar['equipment'] = slovarEquipment['id']
    return slovar


def izdvoj_arrivalAirport(vsebina):   
    t = re.findall('"arrivalAirport"'+':.*?}', vsebina)[0]
    slovar = {}
    for i in headerArrival:
        slovar.update({i: izdvoj(i, t)})
    return slovar




def glavni():
    with open("urls.txt", encoding='utf8')as dat:
        f = open("flights.csv", 'w', newline='', encoding='utf-8')
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        
        for vrstica in dat:
            vrstica = vrstica[:len(vrstica)-1]
            vrstica = vrstica.replace('\\u0026', '&')
            odgovor = requests.get(vrstica)
            print(vrstica)
            while odgovor.status_code == 504:
                time.sleep(4)
                odgovor = requests.get(vrstica)
            if odgovor.status_code == 403:
                time.sleep(90)
                odgovor = requests.get(vrstica)
        
            vsebina = odgovor.text
            p = izdvoj_arrivalAirport(vsebina)
            if p not in sezArrival:
                sezArrival.append(p)
            writer.writerow(staviuslovar(vsebina))
        f.close()
                
                
def csv_file(niz1, niz2, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=niz2)
        writer.writeheader()
        for i in niz1:
            writer.writerow(i)
            
            
#get_departures(datum, obdobje)
#txt_file()
#glavni()
#csv_file(sezArrival, headerArrival, 'arrivalAirport.csv')
#csv_file(sezEquipment, headerEquipment, 'equipment.csv')


#vrstica = ''          
#vrstica = vrstica.replace('\\u0026', '&') 
          
#odgovor = requests.get('https://www.flightstats.com/v2/flight-tracker/JL/461?year=2026&month=7&date=12&flightId=1395051712')
#print(odgovor.status_code)
#v = odgovor.text
#izdvoj_arrivalAirport(v)


