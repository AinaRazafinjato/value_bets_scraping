[![Python](https://img.shields.io/badge/python-3.7%2B-brightgreen.svg)](https://www.python.org/)

# Value Bets Scraping 🕵️‍♂️📊

Un outil de scraping Python pour extraire les **value bets** depuis [OddsPortal](https://www.oddsportal.com), en combinant **Playwright** pour l’automatisation de la navigation et **BeautifulSoup** pour l’analyse HTML.

---

## Table des matières 📚

1. [Fonctionnalités](#fonctionnalités)  
2. [Installation](#installation)  
3. [Prérequis](#prérequis)  
4. [Structure du projet](#structure-du-projet)  
5. [Utilisation](#utilisation)  
6. [Journalisation](#journalisation)  
7. [Contributions](#contributions)

---

## Fonctionnalités ✨

- 🔄 **Automatisation de la navigation** avec Playwright  
- 📝 **Extraction et parsing HTML** avec BeautifulSoup  
- 🧹 **Nettoyage et transformation des données** avec pandas  
- 💾 **Export des données en CSV** (`oddsportal_data.csv`)  
- 🛠️ **Logging détaillé** avec Loguru  

---

## Installation 🛠️

1. **Cloner le dépôt** :  

  ```bash
  git clone https://github.com/AinaRazafinjato/value_bets_scraping.git
  cd value_bets_scraping
  ```

2. **Installer les dépendances** :  

  ```bash
  pip install -r requirements.txt
  ```

3. **Installer Playwright et ses navigateurs** :  

  ```bash
  playwright install chromium
  ```

---

## Prérequis ✅

- Python 3.7 ou supérieur  
- Bibliothèques (listées dans `requirements.txt`) :  
  - 🎭 Playwright  
  - 🍲 BeautifulSoup4  
  - 📊 Pandas  
  - 📜 Loguru  

---

## Structure du projet 🗂️

```bash
.
├── oddsportal/
│       ├── oddsportal_data.csv         # Fichier de sortie CSV (ignoré dans .gitignore)
│       ├── oddsportal_scraping.py 
│       └── oddsportal.log              # Fichier de log (ignoré dans .gitignore)
├── .gitignore
├── README.md
└── requirements.txt
```

- **`oddsportal_scraping.py`**  
  Script principal :  
  - 🚀 Lance Playwright  
  - 📄 Récupère le HTML  
  - 🔍 Parse avec BeautifulSoup  
  - 🧹 Nettoie les données et les enregistre en CSV  

- **`.gitignore`**  
  🚫 Exclut les fichiers de logs, captures et CSV générés.

---

## Utilisation 🚀

1. **Lancer le script de scraping** :  

  ```bash
  cd oddsportal/scraping/
  python oddsportal_scraping.py
  ```

2. Résultat :

- Le fichier **`oddsportal_data.csv`** est généré à côté du fichier **`oddsportal_scraping.py`**.  
- Consultez **`oddsportal.log`** pour suivre l’exécution étape par étape.


---

## Journalisation 📝

Le projet utilise Loguru pour un logging riche :  

- 📋 Niveau d’information  
- 🕒 Horodatage  
- ❌ Messages d’erreur détaillés  

Les logs sont stockés dans **`oddsportal.log`**.

---

## Contributions 🤝

Les contributions sont les bienvenues !  

1. 🍴 Forkez ce dépôt  
2. 🌱 Créez une branche (**`git checkout -b feature/ma-fonctionnalité`**)  
3. 💾 Commitez vos changements (**`git commit -am 'Ajout de ma fonctionnalité'`**)  
4. 📤 Pushez (**`git push origin feature/ma-fonctionnalité`**)  
5. 🔄 Ouvrez une Pull Request  

---
