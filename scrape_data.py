import json
import requests
import pandas as pd
from datetime import datetime

def call_data():
    api_url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=geojson&limit=-1"
    api_call = requests.get(api_url)
    api_data = api_call.text
    api_data = json.loads(api_data)
    df = [feature for feature in api_data['features']]
    df = pd.json_normalize(df)
    return df
df = call_data()
date=datetime.now().strftime('%d_%m_%Y_%H_%M')
df.to_csv(f'vlille_data_{date}.csv', index=False)
