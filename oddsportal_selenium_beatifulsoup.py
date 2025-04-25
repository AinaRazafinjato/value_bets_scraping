# Importation des bibliothèques nécessaires
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime, timedelta

# Configuration des options pour le navigateur Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Mode headless pour exécuter sans interface graphique
chrome_options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU
chrome_options.add_argument("--window-size=1920x1080")  # Définir la taille de la fenêtre
chrome_options.set_capability('pageLoadStrategy', 'normal')  # Attendre le chargement complet de la page

# Initialisation du service pour le driver Chrome
try:
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    raise Exception(f"Erreur lors de l'initialisation du driver Selenium : {e}")

# Réinitialisation du driver si nécessaire
if driver.session_id is None:
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        raise Exception(f"Erreur lors de la réinitialisation du driver Selenium : {e}")

# Chargement de l'URL cible
try:
    driver.get("https://www.oddsportal.com/value-bets/#1/0/overall")
    html = driver.page_source  # Récupération du contenu HTML
except Exception as e:
    driver.quit()
    raise Exception(f"Erreur lors du chargement de l'URL ou de la récupération du contenu HTML : {e}")

# Analyse du contenu HTML avec BeautifulSoup
try:
    soup = BeautifulSoup(html, 'html.parser')
except Exception as e:
    raise Exception(f"Erreur lors de l'analyse du contenu HTML : {e}")

# Sélection de l'élément contenant les données
tabs = soup.select_one("div.tabs")
if not tabs:
    driver.quit()
    raise ValueError("Aucun élément 'div.tabs' trouvé dans le fichier HTML.")

# Récupération des éléments visibles et cachés
try:
    valuebets = tabs.select("div.visible") + tabs.select("div.hidden")
except Exception as e:
    driver.quit()
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
        driver.quit()
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
        driver.quit()
        print(f"Erreur lors de l'extraction des informations sur les matchs : {e}")

# Extraction des informations sur les bookmakers
bookmaker_info = tabs.find_all("div", class_="h-[25px] w-[75px]")
for bookmaker in bookmaker_info:
    try:
        img = bookmaker.find("img")
        data['bookmaker'].append(img['alt'] if img and 'alt' in img.attrs else None)
    except Exception as e:
        driver.quit()
        print(f"Erreur lors de l'extraction des informations sur les bookmakers : {e}")

# Fermeture du driver Selenium
driver.quit()

# Création d'un DataFrame pandas à partir des données collectées
try:
    df = pd.DataFrame(data)
except Exception as e:
    driver.quit()
    raise Exception(f"Erreur lors de la création du DataFrame : {e}")


# Nettoyage de la colonne "probability" pour enlever le caractère '%'
df['probability'] = pd.to_numeric(df['probability'].apply(lambda p: p.replace('%', '') if isinstance(p, str) else None), errors='coerce')

# Remplacement de "Tomorr." par la date de demain dans la colonne "date"
today = datetime.now()
df['date'] = df['date'].apply(lambda date: date.replace(',', '').replace("Tomorr.", (today + timedelta(days=1)).strftime('%d %b')).replace("Today.", today.strftime('%d %b')) if isinstance(date, str) else None)

# Ajout de l'année actuelle aux dates
current_year = today.year
df['date'] = df['date'].apply(lambda date: f"{date} {current_year}" if isinstance(date, str) else None)

# Uniformisation du format des colonnes "date" et "time"
df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')
df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')

# Conversion des colonnes "value" et "odds" en float
df['value'] = pd.to_numeric(df['value'], errors='coerce')
df['odds'] = pd.to_numeric(df['odds'], errors='coerce')

# Trier le DataFrame par valeur décroissante de la colonne "probability"
df.sort_values(by='probability', ascending=False, inplace=True)

# Sauvegarde du DataFrame dans un fichier CSV
try:
    df.to_csv('oddsportal_data.csv', index=False)
    print("Les données ont été sauvegardées avec succès dans 'oddsportal_data.csv'.")
except Exception as e:
    driver.quit()
    raise Exception(f"Erreur lors de la sauvegarde des données dans un fichier CSV : {e}")

# Affichage des 5 premières lignes du DataFrame
print(df.head())

