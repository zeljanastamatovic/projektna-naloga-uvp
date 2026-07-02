import requests
import time
import re
import csv


def get_departures():
    for i in range(4):
        odgovor = requests.get(f'https://www.flightstats.com/v2/flight-tracker/departures/HND/?year=2026&month=7&date=1&hour={6*i}')
        print(odgovor.status_code)
        vsebina = odgovor.text
        with open(f"hndDepartures{i}.html","w",encoding="utf-8") as dat:
            print(vsebina, file=dat)
            
            
with open('urls.txt',"w",encoding='utf-8') as d:
    for i in range(4):

        with open(f"hndDepartures{i}.html",encoding="utf-8") as dat:
            vsebina = dat.read()

            indexes = [x.start() for x in re.finditer('"url"', vsebina)]
            print(len(indexes))  # <-- [6, 13, 19]
            n = len('"url"="')
            for index in indexes:
                url = "https://www.flightstats.com/v2" + vsebina[index + 7: index + 7 +(vsebina[index + 7:]).find('"')]
                print(url, file = d)
                
        #indeks = vsebina.find('"url"')
        #print(vsebina[indeks+10:].find('"'))
        #print(vsebina[indeks + 7: indeks + 7 +(vsebina[indeks + 7:]).find('"')])
        ##with open("htmls/hndDepartures.html",encoding="utf-8") as dat:
    
    
    
#https://www.flightstats.com/v2/flight-tracker/arrivals/LJU/?year=2026&month=5&date=29&hour=6