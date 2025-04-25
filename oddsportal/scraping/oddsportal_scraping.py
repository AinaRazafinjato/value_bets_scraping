from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

html = None

# Configuration de loguru
logger.add(
    "oddsportal.log", rotation="1 MB", level="DEBUG", backtrace=True, diagnose=True
)

# Lancement de Playwright
with sync_playwright() as p:
    logger.info("Playwright lancé")
    browser = p.chromium.launch(headless=False)
    logger.info("Navigateur lancé (mode visible)")

    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    )
    page = context.new_page()
    logger.info("Page créée")

    try:
        logger.info("Chargement de l'URL...")
        page.goto("https://www.oddsportal.com/value-bets/", timeout=60000)
        logger.info("URL chargée, attente pour le chargement complet...")

        page.wait_for_selector("body")
        page.click("text='All sports'")
        logger.info("Clic sur 'All sports' effectué")

        time.sleep(2)

        html = page.content()
        logger.info("Contenu HTML récupéré")

        output_path = "local_analysis/"
        output_file = "oddsportal_content.html"
        with open((output_path + output_file), "w", encoding="utf-8") as file:
            file.write(html)
        logger.info(f"Page sauvegardée localement dans le fichier : {output_file}")

    except Exception as e:
        logger.error(f"Erreur lors du chargement de la page ou du clic : {e}")
    finally:
        browser.close()
        logger.info("Navigateur fermé")

# Analyse avec BeautifulSoup en dehors de sync_playwright()
if html:
    soup = BeautifulSoup(html, "html.parser")
    tabs = soup.select_one("div.tabs")

    try:
        valuebets = tabs.select("div.visible") + tabs.select("div.hidden")
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération des éléments visibles et cachés : {e}"
        )
        raise

    data = {
        "sports": [],
        "countries": [],
        "leagues": [],
        "pronos": [],
        "date": [],
        "time": [],
        "team_1": [],
        "team_2": [],
        "outcome": [],
        "bookmaker": [],
        "odds": [],
        "value": [],
        "probability": [],
    }

    for valuebet in valuebets:
        try:
            header = valuebet.select("a")
            data["sports"].append(header[0].text.strip() if len(header) > 0 else None)
            data["countries"].append(
                header[1].text.strip() if len(header) > 1 else None
            )
            data["leagues"].append(
                " ".join(header[2].text.split()) if len(header) > 2 else None
            )
        except Exception as e:
            logger.warning(
                f"Erreur lors de l'extraction des données de l'en-tête : {e}"
            )

    match_info = tabs.find_all("div", class_="flex min-h-[90px] w-full")
    for match in match_info:
        try:
            p_elements = match.select("p")
            match_data = [p.text.strip() for p in p_elements]
            if len(match_data) >= 9:
                data["pronos"].append(match_data[0])
                data["date"].append(match_data[1])
                data["time"].append(match_data[2])
                data["team_1"].append(match_data[3])
                data["team_2"].append(match_data[4])
                data["outcome"].append(match_data[5])
                data["odds"].append(match_data[6])
                data["value"].append(match_data[7])
                data["probability"].append(match_data[8])
        except Exception as e:
            logger.warning(
                f"Erreur lors de l'extraction des informations sur les matchs : {e}"
            )

    bookmaker_info = tabs.find_all("div", class_="h-[25px] w-[75px]")
    for bookmaker in bookmaker_info:
        try:
            img = bookmaker.find("img")
            data["bookmaker"].append(img["alt"] if img and "alt" in img.attrs else None)
        except Exception as e:
            logger.warning(
                f"Erreur lors de l'extraction des informations sur les bookmakers : {e}"
            )

    try:
        df = pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Erreur lors de la création du DataFrame : {e}")
        raise

    df["probability"] = pd.to_numeric(
        df["probability"].apply(
            lambda p: p.replace("%", "") if isinstance(p, str) else None
        ),
        errors="coerce",
    )

    today = datetime.now()
    df["date"] = df["date"].apply(
        lambda date: (
            date.replace(",", "")
            .replace("Tomorr.", (today + timedelta(days=1)).strftime("%d %b"))
            .replace("Today.", today.strftime("%d %b"))
            if isinstance(date, str)
            else None
        )
    )

    current_year = today.year
    df["date"] = df["date"].apply(
        lambda date: f"{date} {current_year}" if isinstance(date, str) else None
    )

    df["date"] = pd.to_datetime(df["date"], format="%d %b %Y", errors="coerce")
    df["time"] = pd.to_datetime(
        df["time"], format="%H:%M", errors="coerce"
    ).dt.strftime("%H:%M")

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["odds"] = pd.to_numeric(df["odds"], errors="coerce")

    df.sort_values(by="probability", ascending=False, inplace=True)

    try:
        df.to_csv("oddsportal_data.csv", index=False)
        logger.info(
            "Les données ont été sauvegardées avec succès dans 'oddsportal_data.csv'."
        )
    except Exception as e:
        logger.error(
            f"Erreur lors de la sauvegarde des données dans un fichier CSV : {e}"
        )
        raise

    logger.info("Affichage des 5 premières lignes du DataFrame")
    logger.debug(df.head())
else:
    logger.warning("Aucun contenu HTML à analyser.")
