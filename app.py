#%%
# Chargement des librairies
import plotly.express as px 
import pandas as pd
import datetime as dt
import dash 
from dash import dcc, html, dash_table
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Output, Input, State
import os 
import plotly.io as pio
import copy
from adress_to_coordinates import geopy_script
import requests
import json
import geopandas as gpd
import matplotlib.pyplot as plt

#Importation de la base 
def call_data():
    api_url = "https://data.lillemetropole.fr/data/ogcapi/collections/ilevia:vlille_temps_reel/items?f=geojson&limit=-1"
    api_call = requests.get(api_url)
    api_data = api_call.text
    api_data = json.loads(api_data)
    df = [feature for feature in api_data['features']]
    df = pd.json_normalize(df)
    df['properties.commune'] = df['properties.commune'].apply(lambda x: x.upper())
    return df

df = call_data()

#Fonction pour créer la carte
def create_map(df):
    fig = px.scatter_map(df,
                        lat="properties.y",
                        lon="properties.x", 
                        hover_data = {"properties.nb_places_dispo" : True,
                            "properties.nb_velos_dispo" : True},
                        color="properties.nom",
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        zoom=13, 
                        height=800,
                        )
    fig.update_traces(marker=dict(size=15))
    fig.update_layout(mapbox_style="open-street-map")
    return fig

def call_address_to_coordinates(address):
    coordinates = geopy_script.address_to_coordinates(address)
    return coordinates

def call_coordinates_to_address(coordinates):
    address = geopy_script.coordinates_to_address(coordinates)
    return address

def call_calculate_distance(coordinates1, coordinates2):
    distance = geopy_script.calculate_distance(coordinates1, coordinates2)
    return distance

def update_address_to_coordinates(address):
    coordinates = call_address_to_coordinates(address)
    return coordinates

def get_closest_station(coordinates):
    df = call_data()
    df['distance'] = df.apply(lambda x: call_calculate_distance(coordinates, (x['properties.y'], x['properties.x'])), axis = 1)
    closest_station = df[df['distance'] == df['distance'].min()]
    closest_station = closest_station['properties.nom'].values[0]
    return closest_station

#Fonction pour créer le tableau 
def create_table(df):
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict('records')
    table = dash_table.DataTable(
        columns = columns,
        data = data,
        style_table={'height': '300px', 'overflowY': 'auto'}
    )
    return table    

#%%
#Frontend
app = dash.Dash()

app.layout = html.Div(
        

    className="clearfix",
    children=[html.Title(
        title="V'Lille en temps réel"),
        # Bannière du dessus
        html.Div(
            className="upper-column",
            children=[
                html.Div(
                    className="image-container",
                    children=[
                        html.Img(
                            src="https://4.bp.blogspot.com/-eIx0Q3dB_C8/Tmm-4ZmEouI/AAAAAAAAEuA/BASGE7LdYVw/s1600/v-lille.png",
                            alt="Image"
                        )
                    ]
                ),
                html.Div(
                    className="title-container",
                    children=[
                        html.H1("Outil de visualisation des données V'Lille en temps réel"),
                        html.Span(children=[
                            f"Préparé par ", html.B("Martin Coulon, étudiant en master Société Numérique à Sciences Po Lille et Centrale Lille"),
                            # html.Br(), "le ", dt.datetime.now().date()
                        ])
                    ]
                ),
            ]
        ),
                
        # Contenu Principal
        html.Div(
            className="content",
            children=[
                html.Div(className= "Colonne_Haut", children = [
                    html.Div(className= "Adress_Selector", children=[
                        html.H2("Indiquez l'adresse que vous cherchez :"),
                        dcc.Input(
                            id="Adresse",
                            type="text",
                            placeholder="Entrez une adresse",
                            value="13 Rue Auguste Angellier, 59000 Lille",
                            debounce=True,
                            style={'backgroundColor': 'white', 'color': 'black'}
                        )
                    ]),
                    html.Div(className= "Ville_Selector", children=[
                        html.H2("Indiquez les quartiers que vous souhaitez analyser :"),
                        dcc.Dropdown(
                            id="Ville_Selector",
                            options=[{"label": v, "value": v} for v in list(df['properties.commune'].unique())],
                            value=["Lille"], multi=True, optionHeight=30,
                            style={'backgroundColor': 'white', 'color': 'black'}
                        ),
                    ]),
                    html.Div(className= "Arrêt_Selector", children=[
                        html.H2("Sélectionner l'arrêt que vous cherchez :"),
                        dcc.Dropdown(
                            id="Arrêt_Selector",
                            options=[{"label": v, "value": v} for v in list(df['properties.nom'].unique())],
                            value=["BRULE MAISON"], multi=True, optionHeight=30,
                            style={'backgroundColor': 'white', 'color': 'black'}
                        )
                    ]),
                    
                    html.Div(className="right-column", children=[
                    html.Div([
                        dcc.Checklist(
                            id="show_table",
                            options=[{'label': 'Afficher les tableaux', 'value': 'show'}],
                            value=[] 
                        )
                        ])
                    ]),
                    html.Div(className="Arrêt_Next_to_Address", children=[
                        html.H2("Arrêt le plus proche de l'adresse :"),
                        html.Div(id="Arrêt_Next_to_Address")  # This will display the result
                    ]),
                    html.Div(
                        id='table_container',
                        children=[]
                    ),


                    html.Div(className= "Map", children=[
                        dcc.Graph(id="Map", figure=create_map(df))
                    ]),
                ])
                ]
                ),
                dcc.Store(id = "store_ville_selected",
                          storage_type= "memory"),
            ]
        ),
#     ],

# )
#%%
#______Mise à jour du dictionnaire pour ne contenir que les variables disponibles dans les expos sélectionnées_______#
@app.callback(
    [Output("store_ville_selected", "data"),
    Output("Arrêt_Selector", "options"),
    Output("Map", "figure")],
    [Input("Ville_Selector", "value"),
    Input("Arrêt_Selector", "value")])

def update_df(ville_selected, arret_selected): 
    print(ville_selected)
    print(arret_selected)
    df = call_data()
    available_arrêt = [{"label": v, "value": v} for v in list(df['properties.nom'].unique())]
    if len(ville_selected) == 0 : 
        ville_selected = list(df['properties.commune'].unique())
        available_arrêt = [{"label": v, "value": v} for v in list(df['properties.nom'].unique())]

    else : 
        df = df[df['properties.commune'].isin(ville_selected)]
        available_arrêt = [{"label": v, "value": v} for v in list(df['properties.nom'].unique())]

    if len(arret_selected) == 0 :
        arret_selected = list(df['properties.nom'].unique())
    else :
        df = df[df['properties.nom'].isin(arret_selected)]



    fig = create_map(df)
    return ville_selected, available_arrêt, fig

@app.callback(
    [Output("Arrêt_Next_to_Address", "children")],
    [Input("Adresse", "value")])

def Arrêt_Next_to_Address(address):
    coordinates = call_address_to_coordinates(address)
    closest_station = get_closest_station(coordinates)
    return [closest_station]

if __name__ == "__main__":
    app.run(debug = True, port = 8152)

# %%
