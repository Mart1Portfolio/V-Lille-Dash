import time
start_imports = time.time()
import json
import requests
import pandas as pd
from pandas_gbq import to_gbq
import os
from datetime import datetime
from google.oauth2 import service_account
end_imports = time.time()
print(f"Temps de chargement des librairies: {end_imports - start_imports:.2f} secondes")

# credentials = service_account.Credentials.from_service_account_file(
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
# )

# PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
# DATASET_ID = os.environ.get("BIGQUERY_DATASET_ID")
# TABLE_ID = os.environ.get("BIGQUERY_TABLE_ID")

# if not all([PROJECT_ID, DATASET_ID, TABLE_ID]):
#     raise ValueError("Une ou plusieurs variables d'environnement (GCP_PROJECT_ID, BIGQUERY_DATASET_ID, BIGQUERY_TABLE_ID) ne sont pas définies.")
# TABLE_FULL_ID = f"{DATASET_ID}.{TABLE_ID}"

def call_data():
    start_api = time.time()
    api_url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=geojson&limit=-1"
    api_call = requests.get(api_url)
    api_data = api_call.text
    api_data = json.loads(api_data)
    df = [feature for feature in api_data["features"]]
    df = pd.json_normalize(df)
    end_api = time.time()
    print(f"Temps d'appel et de transformation API: {end_api - start_api:.2f} secondes")
    return df


if __name__ == "__main__":
    start_total = time.time()
    df = call_data()
    start_transform = time.time()
    date = datetime.now().strftime("%d_%m_%Y_%H_%M")
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
    df.columns = df.columns.str.replace(".", "_", regex=False)

    df["Date_Scrapping"] = datetime.now().strftime("%d/%m/%Y")
    df["Heure_Min_Scrapping"] = datetime.now().strftime("%H:%M")
    end_transform = time.time()
    print(f"Temps de transformation des données: {end_transform - start_transform:.2f} secondes")
    # start_upload = time.time()
    # to_gbq(
    #     df,
    #     TABLE_FULL_ID,
    #     project_id=PROJECT_ID,
    #     if_exists="append",
    #     credentials=credentials,
    # )
    # end_upload = time.time()
    # print(f"Temps d'upload vers BigQuery: {end_upload - start_upload:.2f} secondes")
    # print(f"Temps total d'exécution: {end_upload - start_total:.2f} secondes")
