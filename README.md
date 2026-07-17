#Analiza letov z letališča Haneda v Tokiu <br/>


Ta program shranjuje informacije o letih z letališča Tokio Haneda in prikazuje nekaj koristnih informacij.Prvotna ideja je bila, da se podatki obdelujejo ves dan, vendar se izkazalo, da nalaganje traja predolgo. Torej gleda le četrtino dneva.<br/>

Program se zažene iz datoteke main.py, večino dela pa opravi datoteka getData.py. Najprej se najde spletna stran s seznamom letov za dan 2 dni pred trenutnim v želenem obdobju. Za vsak let se izvleče njegov URL in shrani v datoteko *urls.txt*. To se izvede s funkciji *get_departures* in *txt_file*. Nato se za vsak URL naložijo podatki za ta let (z uporabo funkcije *glavni*). Teh podatkov ni na začetni spletni strani, zato je treba do vsakega leta dostopati posebej, kar traja veliko časa. Zato se podatki zbirajo le za četrtino dneva. <br/>

Med vsakim dostopom do URL-ja se pridobljeni podatki zapišejo v slovar (s pomočjo funkcije *naredi_slovar*) in tabelo v datoteki *flights.csv*. Stolpci tabele so naslednji: ID leta, končni status, številka leta, ID letališča prihoda, ID preusmerjenega letališča (če obstaja, sicer je null), dolžina leta, letalska družba, letalo, predvideni in dejanski časi vzleta in pristanka. Poseben primer je, ko je let odpovedan, takrat sta dejanska časa odhoda in prihoda null. Obstaja zelo uporabna funkcija *izvleci_info*, ki za dani parameter poišče njegovo vrednost (npr. če je parameter 'flightDuration', potem bo funkcija poiskala, koliko časa je let trajal). 

Shranjeni so tudi podatki o letališčih prihoda (v datoteki *arrivalAirport.csv*) in uporabljenih letalih (v datoteki *equipment.csv*). Informacije o letalih so vzete s posebne spletne strani in so na podlagi IATA kode in imena povezane z vsakim uporabljenim letalom, tako da se za vsako uporabljeno letalo pridobi njegovo ime, število potnikov in domet. To se naredi z uporabo *aircrafts.py*.<br/>

Rezultati so prikazani v *analiza.ipynb*.\
Za lažje delo s časi vzleta in pristanka sem definirala razred Cas, ki mi omogoča izvajanje osnovnih operacij z njimi. 

