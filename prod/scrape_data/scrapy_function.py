import json
import requests
import pandas as pd
from pandas_gbq import to_gbq
import os
from datetime import datetime
from google.oauth2 import service_account

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATASET_ID = os.environ.get("BIGQUERY_DATASET_ID")
TABLE_ID = os.environ.get("BIGQUERY_TABLE_ID")

if not all([PROJECT_ID, DATASET_ID, TABLE_ID]):
    raise ValueError("Une ou plusieurs variables d'environnement (GCP_PROJECT_ID, BIGQUERY_DATASET_ID, BIGQUERY_TABLE_ID) ne sont pas définies.")
TABLE_FULL_ID = f"{DATASET_ID}.{TABLE_ID}"

def call_data():
    api_url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=geojson&limit=-1"
    api_call = requests.get(api_url)
    api_data = api_call.text
    api_data = json.loads(api_data)
    df = [feature for feature in api_data["features"]]
    df = pd.json_normalize(df)
    return df

def scrape_and_upload():
    """Function to scrape data from API, transform it, and upload to BigQuery.
    Args:
        None
    Returns:
        None
    """
    df = call_data()
    drop_columns = [
        "type",
        "@typeName",
        "geometry.type",
        "geometry.@name",
        "geometry.@srs",
        "properties.code_insee",
        "properties.type",
    ]
    df.drop(columns=drop_columns, inplace=True)
    df.rename(columns={"@id": "ID_station"}, inplace=True)
    df["ID_station"] = df["ID_station"].str.replace("vlille_temps_reel.", "", regex=False)
    df.columns = df.columns.str.replace(".", "_", regex=False)
    df["Date_Paris"] = pd.to_datetime(df["properties_date_modification"]).dt.tz_localize("UTC").dt.tz_convert("Europe/Paris")
    df["Date_Scrapping"] = datetime.now().strftime("%d/%m/%Y")
    df["Heure_Min_Scrapping"] = datetime.now().strftime("%H:%M")
    to_gbq(
        df,
        TABLE_FULL_ID,
        project_id=PROJECT_ID,
        if_exists="append",
        # credentials=credentials, # Pas utile pour cloud run
    )
