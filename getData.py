import requests
import time
import re
import csv


niz = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration', 'carrier', 'equipment', 'depTimeScheduled', 'depTimeActual', 'arrTimeScheduled', 'arrTimeActual', 'timezone']

def get_departures():
    for i in range(4):
        odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year=2026&month=7&date=2&hour={6*i}')
        print(odgovor.status_code)
        vsebina = odgovor.text
        with open(f"hndDepartures{i}.html","w",encoding="utf-8") as dat:
            print(vsebina, file=dat)


def txt_file():
    with open('urls.txt',"w",encoding='utf-8') as d:
        for i in range(4):

            with open(f"hndDepartures{i}.html",encoding="utf-8") as dat:
                vsebina = dat.read()
                indexes = [x.start() for x in re.finditer('"url"', vsebina)]
                for index in indexes:
                    url = "https://www.flightstats.com/v2" + vsebina[index + 7: index + 7 +(vsebina[index + 7:]).find('"')]
                    ## gleda da li je code share
                    if vsebina[index + 7: index + 7 + (vsebina[index + 7:]).find('}}')] < vsebina[index + 7: index + 7 +(vsebina[index + 7:]).find('Codeshare')]:
                        print(url, file=d)


#get_departures()
#txt_file()

def nmp():
    with open("urls.txt",encoding='utf8')as dat:
        for i in range(4):
            v = dat.readline()
        vrstica = v[:len(v)-1]
        odgovor = requests.get(vrstica)
        vrstica = vrstica.replace('\\u0026','&')
        print(odgovor.status_code)
        vsebina = odgovor.text
        
        print(vrstica)

    #vsebina = vsebina[vsebina.find(''):]
    # vsebina = vsebina.replace(',',',\n')
    # with open('flight1.txt',"w",encoding='utf-8') as d:
    #     print(vsebina, file=d)
    
    
def izdvoj(niz, vsebina):
    p = re.findall(f'"{niz}"'+r':.*?[,}]', vsebina)[0]
    n = p[p.find(':')+1:len(p)-1]
    
    try:
        return int(n) 
    except:
        if n[0] in '\'"':
            return n[1:len(n)-1]
    return n


def staviuslovar(vsebina):
    slovar = {'flightId':[], 'canceled':[], "finalStatus":[], "flightNumber":[], "diverted":[], "arrivalAirportFS":[], "divertedAirport":[], "operatedBy":[], "gate":[], "terminal":[], 'flightDuration':[], 'carrier': [], 'equipment': [], 'depTimeScheduled': [], 'depTimeActual': [], 'arrTimeScheduled': [], 'arrTimeActual': [], 'timezone': []}
    niz1 = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration']
    for j in niz1:
        slovar[j] = izdvoj(j, vsebina)
        print(j)
        
    slovar['carrier'] = izdvoj('fs',re.findall('"carrier":{"name":.*?}',vsebina)[0])
    slovar['equipment'] = izdvoj('iata',re.findall('"equipment":{.*?}',vsebina)[0])
    
    
    ##get_departures
    slovar['depTimeScheduled'] = izdvoj('time24',re.findall('"time24":.*?},',vsebina)[0])
    slovar['depTimeActual'] = izdvoj('time24',re.findall('"time24":.*?},',vsebina)[1])
    slovar['arrTimeScheduled'] = izdvoj('time24',re.findall('"time24":.*?},',vsebina)[2])
    slovar['arrTimeActual'] = izdvoj('time24',re.findall('"time24":.*?},',vsebina)[3])
    slovar['timezone'] = izdvoj('timezone',re.findall('"timezone":.*?,',vsebina)[2])
    return slovar
    #print(slovar)

   
with open("urls.txt", encoding='utf8')as dat:
    for i in range(3):
        v = dat.readline()
    with open("flights.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=niz)
        writer.writeheader()
        i = 1
        for vrstica in dat:
            print(i)
            print(vrstica)
            i += 1
            vrstica = vrstica[:len(vrstica)-1]
            vrstica = vrstica.replace('\\u0026', '&')
            odgovor = requests.get(vrstica)
            while odgovor.status_code == 504:
                odgovor = requests.get(vrstica)
                time.sleep(2)
            vsebina = odgovor.text
            writer.writerow(staviuslovar(vsebina))







 
            
        #print(re.findall(r'"time24":.*?,',pom[0]))
        #print(re.findall(r'"time24":.*?,',pom[1]))
        #print(re.findall(r'"timezone":.*?,',pom[1]))
        #print(pom)
        
        
        
        
        
        
        #print(re.findall('"fs":"[A-Z][A-Z]',pom))
        
        
        #print(re.findall('"flightId":.*?,',vsebina)[0])
        #print(re.findall('"canceled":.*?,',vsebina)[0])
        #print(re.findall('"finalStatus":.*?,',vsebina))
        #print(re.findall('"flightNumber":.*?,',vsebina))
        #print(re.findall('"diverted":.*?,',vsebina))
        #print(re.findall('"arrivalAirportFS":.*?,',vsebina))
        #print(re.findall('"divertedAirport":.*?,',vsebina))
        #print(re.findall('"operatedBy":.*?,',vsebina))
        #print(re.findall('"gate":.*?,',vsebina))
        #print(re.findall('"terminal":.*?,',vsebina))
        
        
        
        
        
        #time.sleep(1)
            
   
            
          
            
               
               
    
    
#https://www.flightstats.com/v2/flight-tracker/arrivals/LJU/?year=2026&month=5&date=29&hour=