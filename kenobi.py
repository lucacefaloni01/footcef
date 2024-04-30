import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re


###FUNZIONI

def extract_team_codes(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trova tutti i tag <a> con l'attributo href che contiene "/squadre/"
        squad_links = soup.find_all('a', href=lambda x: x and "/squadre/" in x)

        # Estrai i codici dalle URL
        codici_squadre = {}
        for link in squad_links:
            # Ottieni il codice dalla parte finale dell'URL
            url_parts = link['href'].split('/')
            codice_squadra = url_parts[-2]

            # Usa il nome della squadra come chiave e il codice come valore nel dizionario
            codici_squadre[link.get_text()] = codice_squadra

        return codici_squadre
    else:
        print(f"Errore nella richiesta HTTP per {url}: {response.status_code}")
        return {}
    
def filtro_giornata_odierna(dataset, colonne_selezionate):
        # Ottenere la data odierna
        oggi = datetime.today().strftime('%d-%m-%Y')

        # Filtrare il dataset in base alla giornata odierna
        dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

        return dataset_odierno

def match_of_the_day():
    calendar = pd.read_html("https://fbref.com/it/comp/11/calendario/Risultati-e-partite-di-Serie-A")
    calendar_seriea = calendar[0]
    calendar_seriea['Casa']
    calendar_seriea['Ospiti']
    colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
    seriea = calendar_seriea[colonne_selezionate]
    seriea['Competizione'] = "seriea"
    return seriea


match_of_the_day()
