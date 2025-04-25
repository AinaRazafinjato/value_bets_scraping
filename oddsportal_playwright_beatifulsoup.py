# Importation des bibliothèques nécessaires
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta


with sync_playwright() as p:
    # Lancement du navigateur en mode headless
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    try:
        # Chargement de l'URL cible
        page.goto("https://www.oddsportal.com/value-bets/#1/0/overall", wait_until="load")
        html = page.content()  # Récupération du contenu HTML
    except Exception as e:
        raise Exception(f"Erreur lors du chargement de l'URL ou de la récupération du contenu HTML : {e}")
    finally:
        browser.close()

# Analyse du contenu HTML avec BeautifulSoup
try:
    soup = BeautifulSoup(html, 'html.parser')
except Exception as e:
    raise Exception(f"Erreur lors de l'analyse du contenu HTML : {e}")

# Sélection de l'élément contenant les données
tabs = soup.select_one("div.tabs")
if not tabs:
    raise ValueError("Aucun élément 'div.tabs' trouvé dans le fichier HTML.")

# Récupération des éléments visibles et cachés
try:
    valuebets = tabs.select("div.visible") + tabs.select("div.hidden")
except Exception as e:
    raise Exception(f"Erreur lors de la récupération des éléments visibles et cachés : {e}")

# Initialisation du dictionnaire pour stocker les données
data = {
    'sports': [], 'countries': [], 'leagues': [], 'pronos': [],
    'date': [], 'time': [], 'team_1': [], 'team_2': [],
    'outcome': [], 'bookmaker': [], 'odds': [], 'value': [], 
    'probability': []
}

# Extraction des données des paris
for valuebet in valuebets:
    try:
        header = valuebet.select("a")
        data['sports'].append(header[0].text.strip() if len(header) > 0 else None)
        data['countries'].append(header[1].text.strip() if len(header) > 1 else None)
        data['leagues'].append(' '.join(header[2].text.split()) if len(header) > 2 else None)
    except Exception as e:
        print(f"Erreur lors de l'extraction des données de l'en-tête : {e}")

# Extraction des informations sur les matchs
match_info = tabs.find_all("div", class_="flex min-h-[90px] w-full")
for match in match_info:
    try:
        p_elements = match.select("p")
        match_data = [p.text.strip() for p in p_elements]
        if len(match_data) >= 9:  # Vérification pour éviter les erreurs d'indice
            data['pronos'].append(match_data[0])
            data['date'].append(match_data[1])
            data['time'].append(match_data[2])
            data['team_1'].append(match_data[3])
            data['team_2'].append(match_data[4])
            data['outcome'].append(match_data[5])
            data['odds'].append(match_data[6])
            data['value'].append(match_data[7])
            data['probability'].append(match_data[8])
    except Exception as e:
        print(f"Erreur lors de l'extraction des informations sur les matchs : {e}")

# Extraction des informations sur les bookmakers
bookmaker_info = tabs.find_all("div", class_="h-[25px] w-[75px]")
for bookmaker in bookmaker_info:
    try:
        img = bookmaker.find("img")
        data['bookmaker'].append(img['alt'] if img and 'alt' in img.attrs else None)
    except Exception as e:
        print(f"Erreur lors de l'extraction des informations sur les bookmakers : {e}")

# Création d'un DataFrame pandas à partir des données collectées
try:
    df = pd.DataFrame(data)
except Exception as e:
    raise Exception(f"Erreur lors de la création du DataFrame : {e}")

# Traitement des données
df['probability'] = pd.to_numeric(df['probability'].apply(lambda p: p.replace('%', '') if isinstance(p, str) else None), errors='coerce')
today = datetime.now()
df['date'] = df['date'].apply(lambda date: date.replace(',', '').replace("Tomorr.", (today + timedelta(days=1)).strftime('%d %b')).replace("Today.", today.strftime('%d %b')) if isinstance(date, str) else None)
current_year = today.year
df['date'] = df['date'].apply(lambda date: f"{date} {current_year}" if isinstance(date, str) else None)
df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')
df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['odds'] = pd.to_numeric(df['odds'], errors='coerce')
df.sort_values(by='probability', ascending=False, inplace=True)

# Sauvegarde des données dans un fichier CSV
try:
    df.to_csv('oddsportal_data.csv', index=False)
    print("Les données ont été sauvegardées avec succès dans 'oddsportal_data.csv'.")
except Exception as e:
    raise Exception(f"Erreur lors de la sauvegarde des données dans un fichier CSV : {e}")

# Affichage des 5 premières lignes
print(df.head())