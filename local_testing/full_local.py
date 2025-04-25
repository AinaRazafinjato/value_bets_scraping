from bs4 import BeautifulSoup
import pandas as pd
from operator import concat
from datetime import datetime, timedelta


# Sauvegarder le contenu HTML dans un fichier local
with open("page_content.html", "r", encoding="utf-8") as file:
    html_content = file.read()


# Analyser avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')


# Analyse du fichier HTML
# Trouver tous les <div> de class="visible"
tabs = soup.select_one("div.tabs")

valuebets = concat(tabs.select("div.visible"), tabs.select("div.hidden"))

data = {
    'sports': [],
    'countries': [],
    'leagues': [],
    'pronos': [],
    'date': [],
    'time': [],
    'team_1': [],
    'team_2': [],
    'outcome': [],
    'bookmaker': [],
    'odds': [],
    'value': [],
    'probability': []
}

for valuebet in valuebets:
    # Récupération de ce qui est sur le head
    header = valuebet.select("a")

    data['sports'].append(header[0].text.strip())
    data['countries'].append(header[1].text.strip())
    data['leagues'].append(' '.join(header[2].text.split()))

# Récupération de tous les div qui contiennent les infos sur les paris
match_info = tabs.find_all("div", class_="flex min-h-[90px] w-full")

for match in match_info:
    p_elements = match.select("p")
    match_data = [p.text.strip() for p in p_elements]
    
    # Vérifiez que la ligne contient suffisamment d'éléments pour éviter les erreurs
    if len(match_data) >= 9:
        data['pronos'].append(match_data[0])
        data['date'].append(match_data[1])
        data['time'].append(match_data[2])
        data['team_1'].append(match_data[3])
        data['team_2'].append(match_data[4])
        data['outcome'].append(match_data[5])
        data['odds'].append(match_data[6])
        data['value'].append(match_data[7])
        data['probability'].append(match_data[8])
        
# Récupération de tous les div qui contiennent les infos sur les bookmakers
bookmaker_info = tabs.find_all("div", class_="h-[25px] w-[75px]")
for bookmaker in bookmaker_info:
    # On cherche une balise <img> qui contient puis la valeur de l'argument [alt] qui contient le nom du bookmaker
    img = bookmaker.find("img")
    if img and 'alt' in img.attrs:
        data['bookmaker'].append(img['alt'])
    else:
        data['bookmaker'].append(None)

# Créer un DataFrame pandas à partir des données collectées
full_df = pd.DataFrame(data)

# Nettoyage des données
df = full_df.copy()

# Nettoyage de la colonne "probability" pour enlever le caractère '%'
df['probability'] =  pd.to_numeric(df['probability'].apply(lambda p: p.replace('%','')))

# Remplacement de "Tomorr.," par la date de demain dans la colonne "date"
today = datetime.now()

# Nettoyage de la colonne "date"
df['date'] = df['date'].apply(lambda date: date.replace(',', '').replace("Tomorr.", (today + timedelta(days=1)).strftime('%d %b')))

# Ajout de l'année actuelle aux dates
current_year = today.year
df['date'] = df['date'] + f" {current_year}"

# Nettoyage de la colonne "date" pour uniformiser le format
df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')
# Nettoyage de la colonne "time" pour uniformiser le format
df['time'] = pd.to_datetime(df['time'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')

# Nettoyage de la colonne "values" en float64
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Nettoyage de la colonne "odds" en float64
df['odds'] = pd.to_numeric(df['odds'], errors='coerce')

# Sauvegarder le DataFrame dans un fichier CSV
df.to_csv('oddsportal_data.csv', index=False)

# Afficher les 5 premières lignes du DataFrame
df.head()