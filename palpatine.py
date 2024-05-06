######## LIBRERIE #######
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import readline
import time
import random
import pandas as pd
import numpy as np
import itertools
import statsmodels.api as sm

####### FUNZIONI   ########
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
"""
#creazione del link con aggiunta di anno
def crea_link(nome_squadra, codici_squadre, anno=None):
    # Controlla se la squadra è nel dizionario
    if nome_squadra in codici_squadre:
        codice_squadra = codici_squadre[nome_squadra]
        link = f"https://www.fbref.com/it/squadre/{codice_squadra}/"
        
        # Aggiungi la parte dell'anno, se specificata
        if anno:
            link += f"{anno}/"
        
        return link
    else:
        print("Errore: Squadra non trovata nel dizionario.")
        return None
"""
def create_links(base_url, squadre_dict, squadra, comp_types):
    codice_squadra = squadre_dict.get(squadra)
    if codice_squadra:
        links = [f"{base_url}/{codice_squadra}/2023-2024/partite/all_comps/{comp_type}/" for comp_type in comp_types]
        # Aggiungiamo anche i link per il 2022-2023 e il 2021-2022
        links2 = [f"{base_url}/{codice_squadra}/2022-2023/partite/all_comps/{comp_type}/" for comp_type in comp_types]
        links3 = [f"{base_url}/{codice_squadra}/2021-2022/partite/all_comps/{comp_type}/" for comp_type in comp_types]
        return links, links2,links3
    else:
        return []
def download_data(links):
    all_dataframes = []
    for link in links:
        try:
            ritardo = random.uniform(0.88, 1.20)
            time.sleep(ritardo)
            dataframe = pd.read_html(link)[0]  # Assume che la tabella che ti interessa sia la prima
            all_dataframes.append(dataframe)
            print(f"Dati scaricati con successo da {link}")
        except Exception as e:
            print(f"Errore durante il download dei dati da {link}: {e}")
            
    return all_dataframes
def mange_merge(dataframes):
    zero = dataframes[0]
    # Lista di indici delle colonne da mantenere
    fd_indici_casa = [0, 1, 2, 3, 5, 6, 7, 8, 12, 13]  # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    zero = zero.iloc[:, fd_indici_casa]
    # Converte la colonna 'Data' in formato datetime
    zero.loc[:, 'Data'] = pd.to_datetime(zero['Data'], format='%d-%m-%Y')

    # Filtra le righe in base alla data odierna
    data_odierna = datetime.now()
    zero = zero[zero['Data'] <= data_odierna]

    uno = dataframes[1]
    uno = uno.reset_index(drop=True, level=uno.index.names)
    uno.columns = uno.columns.droplevel(level=0)
    # Nome della colonna da dividere
    colonna_da_dividere = '% TiP'  # Sostituisci con il nome effettivo della tua colonna

    # Dividi i valori della colonna per 10
    uno[colonna_da_dividere] = uno[colonna_da_dividere] / 100
    # Lista di indici delle colonne da mantenere
    fd_indici_casa2 = [13, 14, 15, 16, 17, 18, 19]  # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    uno = uno.iloc[:-1, fd_indici_casa2]
    due = dataframes[2]
    due = due.reset_index(drop=True, level=due.index.names)
    due.columns = due.columns.droplevel(level=0)
    # Nome della colonna da dividere
    colonna_da_dividere2 = '%Parate'  # Sostituisci con il nome effettivo della tua colonna
    # Nome della colonna da dividere
    colonna_da_dividere3 = '% compl.'  # Sostituisci con il nome effettivo della tua colonna
    # Nome della colonna da dividere
    colonna_da_dividere4 = '% lanci'  # Sostituisci con il nome effettivo della tua colonna
    # Nome della colonna da dividere
    colonna_da_dividere5 = '% lanci'  # Sostituisci con il nome effettivo della tua colonna
    # Nome della colonna da dividere
    colonna_da_dividere6 = '% par.'  # Sostituisci con il nome effettivo della tua colonna

    # Dividi i valori della colonna per 10
    due[colonna_da_dividere2] = due[colonna_da_dividere2] / 10
    # Dividi i valori della colonna per 10
    due[colonna_da_dividere3] = due[colonna_da_dividere3] / 10
    # Dividi i valori della colonna per 10
    due[colonna_da_dividere4] = due[colonna_da_dividere4] / 10
    # Dividi i valori della colonna per 10
    due[colonna_da_dividere5] = due[colonna_da_dividere5] / 10
    # Dividi i valori della colonna per 10
    due[colonna_da_dividere6] = due[colonna_da_dividere6] / 10

    # Lista di indici delle colonne da mantenere
    fd_indici_casa3 = [13, 14, 23, 26, 29, 33, 34] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    due = due.iloc[:-1, fd_indici_casa3]
    tre = dataframes[3]
    tre = tre.reset_index(drop=True, level=tre.index.names)
    tre.columns = tre.columns.droplevel(level=0)
    # Lista di indici delle colonne da mantenere
    colonna_da_dividere7 = '% compl.'  # Sostituisci con il nome effettivo della tua colonna

    tre[colonna_da_dividere7] = tre[colonna_da_dividere7] / 10

    fd_indici_casa4 = [12, 17, 20, 23, 27, 28, 29, 31] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    tre = tre.iloc[:-1, fd_indici_casa4]
    quattro = dataframes[4]
    quattro = quattro.reset_index(drop=True, level=quattro.index.names)
    quattro.columns = quattro.columns.droplevel(level=0)
    # Lista di indici delle colonne da mantenere
    fd_indici_casa5 = [11, 13, 14, 15, 22, 23, 24] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    quattro = quattro.iloc[:-1, fd_indici_casa5]
    cinque = dataframes[5]
    cinque = cinque.reset_index(drop=True, level=cinque.index.names)
    cinque.columns = cinque.columns.droplevel(level=0)
    # Lista di indici delle colonne da mantenere
    fd_indici_casa6 = [10,17] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    cinque = cinque.iloc[:-1, fd_indici_casa6]
    sei = dataframes[6]
    sei = sei.reset_index(drop=True, level=sei.index.names)
    sei.columns = sei.columns.droplevel(level=0)
    # Lista di indici delle colonne da mantenere
    colonna_da_dividere8 = '% cntrs'  # Sostituisci con il nome effettivo della tua colonna

    sei[colonna_da_dividere8] = sei[colonna_da_dividere8] / 10
    # Lista di indici delle colonne da mantenere
    fd_indici_casa7 = [11, 17, 22, 24, 25] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    sei = sei.iloc[:-1, fd_indici_casa7]
    sette = dataframes[7]
    sette = sette.reset_index(drop=True, level=sette.index.names)
    sette.columns = sette.columns.droplevel(level=0)
    colonna_da_dividere10 = 'Succ%'  # Sostituisci con il nome effettivo della tua colonna
    colonna_da_dividere11 = 'Tkld%'
    sette[colonna_da_dividere10] = sette[colonna_da_dividere10] / 10
    sette[colonna_da_dividere11] = sette[colonna_da_dividere11] / 10
    # Lista di indici delle colonne da mantenere
    fd_indici_casa8 = [16, 20, 22, 26, 27, 30, 31, 32] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    sette = sette.iloc[:-1, fd_indici_casa8]
    otto = dataframes[8]
    otto = otto.reset_index(drop=True, level=otto.index.names)
    otto.columns = otto.columns.droplevel(level=0)
    colonna_da_dividere9 = '% vinti'  # Sostituisci con il nome effettivo della tua colonna

    otto[colonna_da_dividere9] = otto[colonna_da_dividere9] / 10
    # Lista di indici delle colonne da mantenere
    fd_indici_casa9 = [10,11,12, 13, 14, 15, 18, 21, 22, 25] # Sostituisci con gli indici delle colonne che vuoi mantenere
    # Filtra il dataset mantenendo solo le colonne specificate
    otto = otto.iloc[:-1, fd_indici_casa9]

    
    data_merge = pd.concat([zero, uno, due, tre, quattro, cinque, sei, sette, otto], axis=1)
    data_merge = data_merge.fillna(0)
    #data_merge3 = data_merge2[data_merge2['Competizione'] == 'Serie A', 'Champions Lg', 'Premier League']

    # Mappa delle sostituzioni
    mappa_sostituzioni = {'V': 3, 'N': 1, 'P': 0}

    # Sostituisci i valori nella colonna "risultato" utilizzando la mappa
    data_merge['Risultato'] = data_merge['Risultato'].replace(mappa_sostituzioni)

    return data_merge
def partite_di_oggi(competition):
 
    if competition == '0':
        #Scariamento calendario 
        calendar = pd.read_html("https://fbref.com/it/comp/11/calendario/Risultati-e-partite-di-Serie-A")
        calendar_seriea = calendar[0]
        calendar_seriea['Casa']
        calendar_seriea['Ospiti']
        colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
        seriea = calendar_seriea[colonne_selezionate]


        def filtro_giornata_odierna(dataset, colonne_selezionate):
            # Ottenere la data odierna
            oggi = datetime.today().strftime('%d-%m-%Y')

            # Filtrare il dataset in base alla giornata odierna
            dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

            return dataset_odierno

        # Esempio di utilizzo
        # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
        seriea_di_oggi = filtro_giornata_odierna(calendar_seriea, colonne_selezionate)

        import re
        from bs4 import BeautifulSoup
        url_seriea = 'https://fbref.com/it/comp/11/Statistiche-di-Serie-A'
        codici_squadre_seriea = extract_team_codes(url_seriea)
        codici_squadre_seriea = dict(list(codici_squadre_seriea.items())[:21])
        squadre_disponibili_seriea = list(codici_squadre_seriea.keys())


        # Stampare il sottodataset relativo alla giornata odierna
        return seriea_di_oggi, squadre_disponibili_seriea,codici_squadre_seriea
    
    elif competition == "1":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/9/calendario/Risultati-e-partite-di-Premier-League")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

            # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_premier = 'https://fbref.com/it/comp/9/Statistiche-di-Premier-League'
            codici_squadre_premier = extract_team_codes(url_premier)
            codici_squadre_premier = dict(list(codici_squadre_premier.items())[:21])
            squadre_disponibili_premier = list(codici_squadre_premier.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_premier,codici_squadre_premier
    elif competition == "2":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/12/calendario/Risultati-e-partite-di-La-Liga")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

             # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_champions = 'https://fbref.com/it/comp/12/Statistiche-di-La-Liga'
            codici_squadre_champions= extract_team_codes(url_champions)
            codici_squadre_champions = dict(list(codici_squadre_champions.items())[:21])
            squadre_disponibili_champions = list(codici_squadre_champions.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_champions,codici_squadre_champions
    elif competition == "3":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/13/calendario/Risultati-e-partite-di-Ligue-1")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

            # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_champions = 'https://fbref.com/it/comp/13/Statistiche-di-Ligue-1'
            codici_squadre_champions= extract_team_codes(url_champions)
            codici_squadre_champions = dict(list(codici_squadre_champions.items())[:21])
            squadre_disponibili_champions = list(codici_squadre_champions.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_champions,codici_squadre_champions
    elif competition == "4":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/20/calendario/Risultati-e-partite-di-Bundesliga")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

            # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_champions = 'https://fbref.com/it/comp/20/Statistiche-di-Bundesliga'
            codici_squadre_champions= extract_team_codes(url_champions)
            codici_squadre_champions = dict(list(codici_squadre_champions.items())[:21])
            squadre_disponibili_champions = list(codici_squadre_champions.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_champions,codici_squadre_champions
    elif competition == "5":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/8/calendario/Risultati-e-partite-di-Champions-League")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

            # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_champions = 'https://fbref.com/it/comp/8/Statistiche-di-Champions-League'
            codici_squadre_champions= extract_team_codes(url_champions)
            codici_squadre_champions = dict(list(codici_squadre_champions.items())[:21])
            squadre_disponibili_champions = list(codici_squadre_champions.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_champions,codici_squadre_champions    
    elif competition == "6":
            #Scariamento calendario 
            calendar = pd.read_html("https://fbref.com/it/comp/19/calendario/Risultati-e-partite-di-Europa-League")
            calendar_premier = calendar[0]
            calendar_premier['Casa']
            calendar_premier['Ospiti']
            colonne_selezionate = ["Data","Ora", "Casa", "Ospiti"]
            premier = calendar_premier[colonne_selezionate]
            
            def filtro_giornata_odierna(dataset, colonne_selezionate):
                # Ottenere la data odierna
                oggi = datetime.today().strftime('%d-%m-%Y')

                # Filtrare il dataset in base alla giornata odierna
                dataset_odierno = dataset[dataset["Data"] == oggi][colonne_selezionate]

                return dataset_odierno

            # Esempio di utilizzo
            # Supponendo che `calendar_seriea` sia il tuo DataFrame e `colonne_selezionate` sia la lista di colonne
            premier_di_oggi = filtro_giornata_odierna(calendar_premier, colonne_selezionate)

            url_champions = 'https://fbref.com/it/comp/19/Statistiche-di-Europa-League'
            codici_squadre_champions= extract_team_codes(url_champions)
            codici_squadre_champions = dict(list(codici_squadre_champions.items())[:21])
            squadre_disponibili_champions = list(codici_squadre_champions.keys())


            # Stampare il sottodataset relativo alla giornata odierna
            return premier_di_oggi, squadre_disponibili_champions,codici_squadre_champions   
    """
def completer(text, state):
    options = [name for name in nomi_possibili if name.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None
def inserisci_nome():
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")

    while True:
        input_utente = input("Inserisci un nome: ")
        if input_utente in nomi_possibili:
            print("Hai inserito:", input_utente)
            break
        else:
            print("Nome non valido. Riprova.")
    return input_utente
    """
def sarimax_rs(k, correlation, squadra):

    data = k
    best_variable = find_best_sarimax_parameters(data,len(data)/3)
    
    # Conversione della colonna 'Data' in formato datetime
    data['Data'] = pd.to_datetime(data['Data'])

    # Impostare la colonna 'Data' come indice del DataFrame
    #k.set_index('Data', inplace=True)
    # Aggiungi una nuova colonna 'Giornate' che rappresenta l'indice delle giornate
    data['Giornate'] = range(1, len(data) + 1)

    # Selezionare solo le variabili con correlazione superiore a 0.50
    selected_variables = correlation[correlation > 0.40].index.tolist()

    # Creare un nuovo dataset contenente solo le variabili selezionate
    new_dataset = data[selected_variables]
    print(best_variable)
    # Creazione del modello SARIMAX con variabili esogene
    model = SARIMAX(data['Rs'], exog=new_dataset, order=(1, 1, 1), seasonal_order= best_variable)

    # Addestramento del modello
    result = model.fit()

    # Effettuare le previsioni per i prossimi 5 step
    forecast = result.forecast(steps=6, exog=new_dataset.iloc[-6:])
    '''
    # Plot delle previsioni
    plt.plot(data['Giornate'], data['Rs'], label='Dati storici', marker='o')
    plt.plot(range(len(data), len(data) + len(forecast)), forecast, label='Previsioni', marker='o')
    plt.xlabel('Numero di giornate')
    plt.ylabel('Reti Subite')
    plt.xticks(range(1, len(data) + 6)) 
    plt.title('Reti Subite {}'.format(squadra))
    plt.legend()
    plt.show()
    '''
    print(forecast)
    return forecast.round(3)
def sarimax_rf(k, correlation, squadra):

    data = k
    best_variable = find_best_sarimax_parameters(data,len(data)/3)
    print(best_variable)

    # Conversione della colonna 'Data' in formato datetime
    data['Data'] = pd.to_datetime(data['Data'])

    # Impostare la colonna 'Data' come indice del DataFrame
    #k.set_index('Data', inplace=True)
    # Aggiungi una nuova colonna 'Giornate' che rappresenta l'indice delle giornate
    data['Giornate'] = range(1, len(data) + 1)

    # Selezionare solo le variabili con correlazione superiore a 0.50
    selected_variables = correlation[correlation > 0.40].index.tolist()

    # Creare un nuovo dataset contenente solo le variabili selezionate
    new_dataset = data[selected_variables]
    print(best_variable)
    # Creazione del modello SARIMAX con variabili esogene
    model = SARIMAX(data['Rf'], exog=new_dataset, order=(1, 1, 1), seasonal_order=best_variable)

    # Addestramento del modello
    result = model.fit()

    # Effettuare le previsioni per i prossimi 5 step
    forecast = result.forecast(steps=6, exog=new_dataset.iloc[-6:])
    '''
    # Plot delle previsioni
    plt.plot(data['Giornate'], data['Rf'], label='Dati storici', marker='o')
    plt.plot(range(len(data), len(data) + len(forecast)), forecast, label='Previsioni', marker='o')
    plt.xlabel('Numero di giornate')
    plt.ylabel('Reti Fatte')
    plt.xticks(range(1, len(data) + 6)) 
    plt.title('Reti Fatte{}'.format(squadra))
    plt.legend()
    plt.show()
    '''
    print(forecast)
    
    return forecast.round(3)
def sarimax_amm(k, correlation, squadra):

    data = k
    best_variable = find_best_sarimax_parameters(data,len(data)/3)
    # Conversione della colonna 'Data' in formato datetime
    data['Data'] = pd.to_datetime(data['Data'])

    # Impostare la colonna 'Data' come indice del DataFrame
    #k.set_index('Data', inplace=True)
    # Aggiungi una nuova colonna 'Giornate' che rappresenta l'indice delle giornate
    data['Giornate'] = range(1, len(data) + 1)

    # Selezionare solo le variabili con correlazione superiore a 0.50
    selected_variables = correlation[correlation > 0.40].index.tolist()

    # Creare un nuovo dataset contenente solo le variabili selezionate
    new_dataset = data[selected_variables]
    print(best_variable)
    # Creazione del modello SARIMAX con variabili esogene
    model = SARIMAX(data['Amm.'], exog=new_dataset, order=(1, 1, 1), seasonal_order=best_variable)

    # Addestramento del modello
    result = model.fit()

    # Effettuare le previsioni per i prossimi 5 step
    forecast = result.forecast(steps=6, exog=new_dataset.iloc[-6:])
    '''
    # Plot delle previsioni
    plt.plot(data['Giornate'], data['Amm.'], label='Dati storici', marker='o')
    plt.plot(range(len(data), len(data) + len(forecast)), forecast, label='Previsioni', marker='o')
    plt.xlabel('Numero di giornate')
    plt.ylabel('Ammonizioni ')
    plt.xticks(range(1, len(data) + 6)) 
    plt.title('Ammonizioni {}'.format(squadra))
    plt.legend()
    plt.show()
    '''
    print(forecast)
    return forecast.round(3)
def sarimax_ris(k, correlation, squadra):

    data = k
    best_variable = find_best_sarimax_parameters(data,len(data)/3)
    # Conversione della colonna 'Data' in formato datetime
    data['Data'] = pd.to_datetime(data['Data'])

    # Impostare la colonna 'Data' come indice del DataFrame
    #k.set_index('Data', inplace=True)
    # Aggiungi una nuova colonna 'Giornate' che rappresenta l'indice delle giornate
    data['Giornate'] = range(1, len(data) + 1)

    # Selezionare solo le variabili con correlazione superiore a 0.50
    selected_variables = correlation[correlation > 0.40].index.tolist()

    # Creare un nuovo dataset contenente solo le variabili selezionate
    new_dataset = data[selected_variables]
    print(best_variable)
    print(new_dataset)
    # Creazione del modello SARIMAX con variabili esogene
    model = SARIMAX(data['Risultato'], exog=new_dataset, order=(1, 1, 1), seasonal_order=best_variable)

    # Addestramento del modello
    result = model.fit(method='nm')

    # Effettuare le previsioni per i prossimi 5 step
    forecast = result.forecast(steps=6, exog=new_dataset.iloc[-6:])
    '''
    # Plot delle previsioni
    plt.plot(data['Giornate'], data['Risultato'], label='Dati storici', marker='o')
    plt.plot(range(len(data), len(data) + len(forecast)), forecast, label='Previsioni', marker='o')
    plt.xlabel('Numero di giornate')
    plt.ylabel('Punti')
    plt.xticks(range(1, len(data) + 6)) 
    plt.title('Punti {}'.format(squadra))
    plt.legend()
    plt.show()
    '''
    print(forecast)
    return forecast.round(3)
def modifica_valori(dataframe):
    # Modifica i valori all'interno delle colonne 'Rf' e 'Rs'
    dataframe['Rf'] = dataframe['Rf'].apply(lambda x: int(x.split()[0]) if isinstance(x, str) else x)
    dataframe['Rs'] = dataframe['Rs'].apply(lambda x: int(x.split()[0]) if isinstance(x, str) else x)
    return dataframe
"""
def extract_team_name(filename):
    # Prendi il nome della squadra da dopo l'underscore al punto
    team_name = os.path.splitext(filename)[0].split('_')[1]
    return team_name
    """
def calcola_risultato(df_a, df_b, casa, trasferta):
    # Estrai i nomi delle squadre da entrambi i nomi file
    risultato_punteggio = []
    gx_casa = []
    gx_trasferta = []
    ammonizioni = []
    print(df_a)
    print(df_b)
    for index, row_a in df_a.iterrows():
        row_b = df_b.iloc[index]
        
        if row_a['Risultato'] > row_b['Risultato']:
            risultato_punteggio.append(casa)
        elif row_a['Risultato'] == row_b['Risultato']:
            risultato_punteggio.append('Uguali')
        else:
            risultato_punteggio.append(trasferta)
        
        gx_casa.append(row_a['Reti Fatte'] - row_b['Reti Subite'])
        gx_trasferta.append(row_b['Reti Fatte'] - row_a['Reti Subite'])
        ammonizioni.append((row_a['Ammonizioni'] + row_b['Ammonizioni']))
    
    nuovo_dataset = pd.DataFrame({
        'Casa': casa,
        'Trasferta': trasferta,
        'Ris. Punteggio': risultato_punteggio,
        'Gx Casa': gx_casa,
        'Gx Trasferta': gx_trasferta,
        'Amm.': ammonizioni
    })
    
    return nuovo_dataset
def find_best_sarimax_parameters(data, seasonal_period):
    p_values = range(0, 11)  # Valori di P possibili
    d_values = range(0, 11)  # Valori di D possibili
    q_values = range(0, 11)  # Valori di Q possibili

    # Genera tutte le possibili combinazioni di parametri
    parameters = list(itertools.product(p_values, d_values, q_values))
    print(parameters)

    best_aic = float("inf")
    best_params = None

    for param in parameters:
        try:
            # Crea e addestra il modello SARIMAX per ogni combinazione di parametri
            model = sm.tsa.SARIMAX(data, order=param, seasonal_order=(p_values, d_values, q_values, seasonal_period))
            results = model.fit()

            # Calcola l'AIC per il modello attuale
            aic = results.aic

            # Aggiorna i parametri ottimali se l'AIC attuale è migliore del miglior AIC trovato finora
            if aic < best_aic:
                best_aic = aic
                best_params = param

        except:
            continue

    return best_params
def analisi(nome_squadra, valore):
    # Lista di nomi possibili
    #nomi_possibili = nomi
    #nome_squadra = inserisci_nome()
    # Usa la funzione create_links per ottenere i link desiderati
    base_url = "https://fbref.com/it/squadre"
    comp_types = ['schedule','shooting', 'keeper', 'passing', 'passing_types', 'gca', 'defense', 'possession', 'misc']

    links, links2, links3 = create_links(base_url, valore, nome_squadra, comp_types)

    # Scarica i dati da ciascun link
    dataframes = download_data(links)
    dataframes2 = download_data(links2)
    dataframes3 = download_data(links3)


    zero = mange_merge(dataframes)
    uno = mange_merge(dataframes2)
    due = mange_merge(dataframes3)
    last3 = pd.concat([due, uno,zero], ignore_index=True)

    k=modifica_valori(last3)
    seen = k.drop(columns=['Ora','Competizione','Girone','Stadio'])
    # Calcola l'indice di correlazione con la variabile 'Risultato'
    correlation_Risultato = seen.corr()['Risultato']
    correlation_RetiFatte = seen.corr()['Rf']
    correlation_RetiSubite = seen.corr()['Rs']
    correlation_Amm = seen.corr()['Amm.']

    #Calcolo Sarimax 
    fore_ris = sarimax_ris(k,correlation_Risultato,nome_squadra)
    fore_rf = sarimax_rf(k,correlation_RetiFatte,nome_squadra)
    fore_rs = sarimax_rs(k,correlation_RetiSubite,nome_squadra)
    fore_amm = sarimax_amm(k,correlation_Amm,nome_squadra)


    # Creazione del dataset vuoto
    dataset_new = pd.DataFrame()

    # Aggiunta delle colonne con le liste di numeri
    dataset_new['Risultato'] = fore_ris   # Esempio di lista di numeri per la colonna 'Risultato'
    dataset_new['Reti Fatte'] = fore_rf  # Esempio di lista di numeri per la colonna 'Reti Fatte'
    dataset_new['Reti Subite'] = fore_rs  # Esempio di lista di numeri per la colonna 'Reti Subite'
    dataset_new['Ammonizioni'] = fore_amm  # Esempio di lista di numeri per la colonna 'Ammonizioni'

    # Salvataggio del dataset in un file CSV nella cartella corrente
    return dataset_new.head(1).reset_index(drop=True)
def finish(df):
    # Numero totale di squadre nel dataset
    numero_squadre = len(df)

    # Lista per memorizzare i risultati
    risultati = []

    # Itera su tutte le squadre nel dataset
    for i in range(numero_squadre):
        # Estrai i dettagli della riga corrente
        riga = df.iloc[i]
        
        # Estrai il nome della squadra di casa e degli ospiti
        nome_squadra_casa = riga['Casa']
        nome_squadra_trasferta = riga['Ospiti']
        
        # Esegui l'analisi per la squadra di casa
        risultato_casa = analisi(nome_squadra_casa, valore)
        
        # Esegui l'analisi per la squadra in trasferta
        risultato_trasferta = analisi(nome_squadra_trasferta, valore)
        
        # Calcola il risultato finale utilizzando i risultati delle analisi
        risultato_finale = calcola_risultato(risultato_casa, risultato_trasferta, nome_squadra_casa, nome_squadra_trasferta)
        
        # Aggiungi il risultato alla lista dei risultati
        risultati.append(risultato_finale)

    # Concatena tutti i risultati in un unico DataFrame
    risultato_completo = pd.concat(risultati)

    # Stampare o fare qualsiasi altra operazione necessaria con il risultato completo
    print("Risultato completo del calcolo:")
    print(risultato_completo)


###### MAIN PROGRAMM  A#######
print(
    '''
    Scegliere competizione 
    [0] Serie A 
    [1] Premier League 
    [2] La Liga
    [3] Ligue One
    [4] Bundersliga
    [5] Champions League
    [6] Europa League
        '''
)
competizione = input('Inserire Numero: ')
pdo, nomi, valore  = partite_di_oggi(competizione)
print(pdo)

finish(pdo)