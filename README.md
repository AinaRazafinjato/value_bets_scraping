[![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)]()

# OddsPortal Data Scraper

Un outil de scraping Python pour extraire les **value bets** depuis [OddsPortal](https://www.oddsportal.com), en combinant **Playwright** pour l’automatisation de la navigation et **BeautifulSoup** pour l’analyse HTML.

---

## Table des matières

1. [Fonctionnalités](#fonctionnalités)  
2. [Installation](#installation)  
3. [Prérequis](#prérequis)  
4. [Structure du projet](#structure-du-projet)  
5. [Utilisation](#utilisation)  
6. [Journalisation](#journalisation)  
7. [Contributions](#contributions)  
8. [Licence](#licence)  

---

---

## Fonctionnalités

- 🔄 **Automatisation de la navigation** (Playwright)  
- 📝 **Extraction et parsing HTML** (BeautifulSoup)  
- 🧹 **Nettoyage et transformation des données** (pandas)  
- 💾 **Export en CSV** (`oddsportal_data.csv`)  
- 🛠️ **Logging détaillé** avec Loguru  

---

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone https://github.com/AinaRazafinjato/value_bets_scraping.git
   cd value_bets_scraping
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Installez Playwright et ses navigateurs :
   ```bash
   playwright install chromium
   ```

## Prérequis
- Python 3.7 ou supérieur
- Bibliothèques (déjà listées dans requirements.txt) :
  - playwright
  - beautifulsoup4
  - pandas
  - loguru
    
## Structure du projet
   ```bashh
      .
      ├── .gitignore
      ├── LICENSE
      ├── oddsportal_data.csv       # Fichier de sortie CSV (ignoré par Git)
      ├── oddsportal.html          # Copie locale de la page scrappée (ignoré par Git)
      ├── oddsportal.log           # Fichier de log (Loguru, ignoré par Git)
      ├── screenshot.png           # Capture d’écran du navigateur (ignoré par Git)
      ├── local_analysis.ipynb     # Notebook Jupyter pour analyses ultérieures
      └── oddsportal_playwright_beatifulsoup.py
   ```

- **`oddsportal_playwright_beatifulsoup.py`**  
  Script principal :
    - Lance Playwright
    - Récupère le HTML
    - Parse avec BeautifulSoup
    - Nettoie les données et les enregistre en CSV

- **`local_analysis.ipynb`**  
  Notebook pour explorer et visualiser les value bets extraits.

- **`.gitignore`**  
Exclut les fichiers de logs, captures et CSV générés.

## Utilisation
1. Lancer le script de scraping :
   ```bash
   python oddsportal_playwright_beatifulsoup.py
   ```

2. Résultat
  - Le fichier **`oddsportal_data.csv`** est généré à la racine du projet.
  - La capture d'écran **`screenshot.png`** est pour voir l'état du site avant l'analyse avec BeautifulSoup.
  - Consultez **`oddsportal.log`** pour suivre l’exécution étape par étape.

3. Analyse
  Ouvrez **`local_analysis.ipynb`** pour voir l'analyse avec BeautifulSoup fait en locale.

## Journalisation
Le projet utilise Loguru pour un logging riche :
  - Niveau d’information
  - Horodatage
  - Messages d’erreur détaillés

Les logs sont stockés dans **`oddsportal.log`**.

## Contributions
Les contributions sont les bienvenues !
  1. Forkez ce dépôt
  2. Créez une branche (**`git checkout -b feature/ma-fonctionnalité`**)
  3. Commitez vos changements (**`git commit -am 'Ajout de ma fonctionnalité'`**)
  4. Pushez (**`git push origin feature/ma-fonctionnalité`**)
  5. Ouvrez une Pull Request
