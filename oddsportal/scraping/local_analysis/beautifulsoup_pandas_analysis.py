from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Charger le fichier HTML local
html = Path("oddsportal_content.html").read_text(encoding="utf-8")

# Analyse avec BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
valuebets = soup.select("div.tabs div.visible")

# Initialisation du dictionnaire pour stocker les données
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


def extract_header_data(valuebet, data):
    header = valuebet.select("a")
    data["sports"].append(header[0].text.strip() if len(header) > 0 else None)
    data["countries"].append(header[1].text.strip() if len(header) > 1 else None)
    data["leagues"].append(
        " ".join(header[2].text.split()) if len(header) > 2 else None
    )


def extract_match_data(match_info, data):
    for match in match_info:
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


def extract_bookmaker_data(bookmaker_info, data):
    for bookmaker in bookmaker_info:
        img = bookmaker.find("img")
        data["bookmaker"].append(img["alt"] if img and "alt" in img.attrs else None)


for valuebet in valuebets:
    extract_header_data(valuebet, data)
    match_info = valuebet.find_all("div", class_="flex min-h-[90px] w-full")
    extract_match_data(match_info, data)
    bookmaker_info = valuebet.find_all("div", class_="h-[25px] w-[75px]")
    extract_bookmaker_data(bookmaker_info, data)

if data:
    dataframe = pd.DataFrame(data)
else:
    raise ValueError(
        "Le dictionnaire 'data' est vide. Impossible de créer un DataFrame."
    )


def clean_probability_column(df):
    df["probability"] = pd.to_numeric(
        df["probability"].apply(
            lambda p: p.replace("%", "") if isinstance(p, str) else None
        ),
        errors="coerce",
    )
    return df


def clean_date_column(df, today):
    df["date"] = df["date"].apply(
        lambda date: (
            date.replace(",", "")
            .replace("Today", today.strftime("%d %b"))
            .replace("Tomorr.", (today + timedelta(days=1)).strftime("%d %b"))
            if isinstance(date, str) and date is not None
            else None
        )
    )
    current_year = today.year
    df["date"] = df["date"].apply(
        lambda date: f"{date} {current_year}" if isinstance(date, str) else None
    )
    df["date"] = pd.to_datetime(df["date"], format="%d %b %Y", errors="coerce")
    return df


def clean_time_column(df):
    df["time"] = pd.to_datetime(
        df["time"], format="%H:%M", errors="coerce"
    ).dt.strftime("%H:%M")
    return df


def convert_columns_to_numeric(df, columns):
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def sort_dataframe(df):
    df.sort_values(
        by=["probability", "date", "time"], ascending=[False, True, True], inplace=True
    )
    return df


df = dataframe.copy()
today = datetime.now()

df = clean_probability_column(df)
df = clean_date_column(df, today)
df = clean_time_column(df)
df = convert_columns_to_numeric(df, ["value", "odds"])
df = sort_dataframe(df)

df.to_csv("oddsportal_data.csv", index=False)
missing_values = df.isnull().sum()
print("Valeurs manquantes par colonne :")
print(missing_values)
