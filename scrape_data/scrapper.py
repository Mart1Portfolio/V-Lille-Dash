import json
import requests
import pandas as pd
from datetime import datetime
import os

def call_data():
    api_url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=geojson&limit=-1"
    api_call = requests.get(api_url)
    api_data = api_call.text
    api_data = json.loads(api_data)
    df = [feature for feature in api_data['features']]
    df = pd.json_normalize(df)
    return df

if __name__ == "__main__":
    try :
        df = call_data()
        date=datetime.now().strftime('%d_%m_%Y_%H_%M')
        if not os.path.exists('data'):
            os.makedirs('data')
        df.to_csv(f'data/vlille_data_{date}.csv', index=False)
        print(f"Data successfully saved to data/vlille_data_{date}.csv")
    except Exception as e:
        print(f"An error occurred: {e}")