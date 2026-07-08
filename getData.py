import requests
import time
import re
import csv


header = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration', 'carrier', 'equipment', 'depTimeScheduled', 'depTimeActual', 'arrTimeScheduled', 'arrTimeActual', 'timezone']
n = []

def get_departures():
    for i in range(4):
        odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year=2026&month=7&date=6&hour={6*i}')
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
    slovar = {'flightId': [], 'canceled': [], "finalStatus": [], "flightNumber": [], "diverted": [], "arrivalAirportFS": [], "divertedAirport": [], "operatedBy": [], "gate": [], "terminal": [], 'flightDuration': [], 'carrier': [], 'equipment': [], 'depTimeScheduled': [], 'depTimeActual': [], 'arrTimeScheduled': [], 'arrTimeActual': [], 'timezone': []}
    niz1 = ['flightId', 'canceled', "finalStatus", "flightNumber", "diverted", "arrivalAirportFS", "divertedAirport", "operatedBy", "gate", "terminal", 'flightDuration']
    for j in niz1:
        #print(j)
        slovar[j] = izdvoj(j, vsebina)
        
        
    slovar['carrier'] = izdvoj('fs',re.findall('"carrier":{"name":.*?}',vsebina)[0])
    slovar['equipment'] = izdvoj('iata',re.findall('"equipment":{.*?}',vsebina)[0])
    
    
    ##get_departures
    slovar['depTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[0])
    slovar['depTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[1])
    slovar['arrTimeScheduled'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[2])
    slovar['arrTimeActual'] = izdvoj('time24', re.findall('"time24":.*?},', vsebina)[3])
    slovar['timezone'] = izdvoj('timezone', re.findall('"timezone":.*?,', vsebina)[2])
    #print(slovar)
    return slovar
    

def glavni():
    with open("urls.txt", encoding='utf8')as dat:
        for i in range(3):
            v = dat.readline()
            
        with open("flights.csv", 'w', newline='',encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            
            for vrstica in dat:
            
                
                vrstica = vrstica[:len(vrstica)-1]
                vrstica = vrstica.replace('\\u0026', '&')
                odgovor = requests.get(vrstica)
                print(i)
                i += 1
                print(vrstica)
                while odgovor.status_code == 504:
                    time.sleep(4)
                    odgovor = requests.get(vrstica)
                print('prvi')
                print(odgovor.status_code)
                if odgovor.status_code == 403:
                    time.sleep(180)
                    odgovor = requests.get(vrstica)
                print('drugi')
                print(odgovor.status_code)
                vsebina = odgovor.text
                if odgovor.status_code == 200:
                    writer.writerow(staviuslovar(vsebina))
                else:
                    print(odgovor.status_code)
                    print('jokjok')
                    break




def csv_file(niz1, niz2):
    with open("flights.csv", 'w', newline='',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=niz2)
        writer.writeheader()
        for film in niz1:
            writer.writerow(film)
            
            



glavni()
#vrstica = ''          
#vrstica = vrstica.replace('\\u0026', '&') 
          
#odgovor = requests.get('https://www.flightstats.com/v2/flight-tracker/JL/479?year=2026&month=7&date=6&flightId=1393848000')
#print(odgovor.status_code)
#v = odgovor.text
#with open('t.html','w',encoding='utf-8') as dat:
#    print(v,file=dat)
#staviuslovar(v)


#with open("flights.csv", "w") as f:
#        writer = csv.DictWriter(f, fieldnames=niz)
#        writer.writeheader()

 
            
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