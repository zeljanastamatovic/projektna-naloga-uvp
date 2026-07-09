import requests
import time
import re
import csv


header = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration', 'carrier', 'equipment', 'depTimeScheduled', 'depTimeActual', 'arrTimeScheduled', 'arrTimeActual', 'timezone']
sezArrival = []
sezCarrier = []
sezEquipment = []
headerArrival = ["fs", 'iata', 'name', 'city', 'country', 'timeZoneRegionName', 'regionName']
headerCarrier = ['fs', 'name']
headerEquipment = ['iata', 'name', 'title']

datum = {'leto': 2026, 'mesec': 7, 'dan': 6} # datum mora biti najvise 3 dana pre trenutnog datuma
obdobje = 6 # 4 moznosti: 0 (med 00:00 in 6:00), 6 (med 6:00 in 12:00), 12 (med 12:00 in 18:00), 18 (med 18:00 in 24:00)

def get_departures(datum, obdobje):
    odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year={datum['leto']}&month={datum['mesec']}&date={datum['dan']}&hour={obdobje}')
    print(odgovor.status_code)
    vsebina = odgovor.text
    with open(f"hndDepartures.html", "w", encoding="utf-8") as dat:
        print(vsebina, file=dat)


def txt_file():
    with open('urls.txt', 'w', encoding='utf-8') as d:
        with open("hndDepartures1.html", encoding="utf-8") as dat:
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
    
    try:
        return int(n) 
    except:
        if n[0] in '\'"':
            return n[1:len(n)-1]
    return n


def staviuslovar(vsebina):
    slovar = {'flightId': [], 'canceled': [], "finalStatus": [], "flightNumber": [], "diverted": [], "arrivalAirportFS": [], "divertedAirport": [], "operatedBy": [], "gate": [], "terminal": [], 'flightDuration': [], 'carrier': [], 'equipment': [], 'depTimeScheduled': [], 'depTimeActual': [], 'arrTimeScheduled': [], 'arrTimeActual': [], 'timezone': []}
    niz1 = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration']
    
    slovar['depTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[0])
    slovar['depTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[1])
    slovar['arrTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[2])
    slovar['arrTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[3])
    slovar['timezone'] = izdvoj('timezone', re.findall('"timezone":.*?,', vsebina)[2])
    
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
        
        
    slovar['carrier'] = izdvoj('fs', re.findall('"carrier":{"name":.*?}', vsebina)[0])
    slovar['equipment'] = izdvoj('iata', re.findall('"equipment":{.*?}', vsebina)[0])
    
    
    ##get_departures
    
    #print(slovar)
    return slovar


def izdvoj_arrivalAirport(vsebina, sez, opcija):   
    t = re.findall(f'"{opcija}"'+':.*?}', vsebina)[0]
    slovar = {}
    for i in sez:
        slovar.update({i: izdvoj(i, t)})
    return slovar


def stvaiusez(vsebina):
    p = izdvoj_arrivalAirport(vsebina, headerArrival, 'arrivalAirport')
    if p not in sezArrival:
        sezArrival.append(p)
    p = izdvoj_arrivalAirport(vsebina, headerEquipment, 'equipment')
    if p not in sezEquipment:
        sezEquipment.append(p)
    p = izdvoj_arrivalAirport(vsebina, headerCarrier, 'carrier')
    if p not in sezCarrier:
        sezCarrier.append(p)
        

def glavni():
    with open("urls.txt", encoding='utf8')as dat:
            
        with open("flights.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            
            for vrstica in dat:
                vrstica = vrstica[:len(vrstica)-1]
                vrstica = vrstica.replace('\\u0026', '&')
                odgovor = requests.get(vrstica)
                
                while odgovor.status_code == 504:
                    time.sleep(4)
                    odgovor = requests.get(vrstica)

                if odgovor.status_code == 403:
                    time.sleep(90)
                    odgovor = requests.get(vrstica)
            
                vsebina = odgovor.text
                stvaiusez(vsebina)
                writer.writerow(staviuslovar(vsebina))
                
                
def csv_file(niz1, niz2, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=niz2)
        writer.writeheader()
        for i in niz1:
            writer.writerow(i)
            
            
#get_departures(datum, obdobje)
#txt_file()
glavni()
csv_file(sezArrival, headerArrival, 'arrivalAirport.csv')
csv_file(sezEquipment, headerEquipment, 'equipment.csv')
csv_file(sezCarrier, headerCarrier, 'carrier.csv')


#vrstica = ''          
#vrstica = vrstica.replace('\\u0026', '&') 
          
#odgovor = requests.get('https://www.flightstats.com/v2/flight-tracker/CZ/3086?year=2026&month=7&date=6&flightId=1393818227')
#print(odgovor.status_code)
#v = odgovor.text
#print(staviuslovar(v))


