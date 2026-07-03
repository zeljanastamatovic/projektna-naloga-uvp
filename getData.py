import requests
import time
import re
import csv


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
    
with open("urls.txt",encoding='utf8')as dat:
    for i in range(4):
        v = dat.readline()
    vrstica = v[:len(v)-1]
    odgovor = requests.get(vrstica)
    print(odgovor.status_code)
    vsebina = odgovor.text
    vrstica = vrstica.replace('\\u0026','&')
    print(vrstica)

    #vsebina = vsebina[vsebina.find(''):]
    vsebina = vsebina.replace(',',',\n')
    with open('flight1.txt',"w",encoding='utf-8') as d:
        print(vsebina, file=d)
    
    
    
    
#https://www.flightstats.com/v2/flight-tracker/arrivals/LJU/?year=2026&month=5&date=29&hour=6