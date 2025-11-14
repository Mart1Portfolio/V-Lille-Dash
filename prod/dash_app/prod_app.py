#%%
# Chargement des librairies
import plotly.express as px 
import pandas as pd
import datetime as dt
import dash 
from dash import dcc, html, dash_table
from dash.dependencies import Output, Input, State
from adress_to_coordinates import geopy_script
import requests
import json

# Importation de la base 
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

# Fonction pour créer la carte
def create_map(df, show_legend=False):
    fig = px.scatter_map(
        df,
        lat="properties.y",
        lon="properties.x", 
        hover_data={"properties.nb_places_dispo": True,
                  "properties.nb_velos_dispo": True},
        color="properties.nom",
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=13, 
        height=600,
    )
    fig.update_traces(marker=dict(size=15))
    fig.update_layout(mapbox_style="open-street-map")
    # Basic layout improvements (for all devices)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},  # Remove margins
        autosize=True,                            # Allow autosize
        height=600,                              # Set reasonable height
        showlegend=show_legend,                  # Set based on parameter
        legend=dict(
            itemsizing='constant',  # Keep icon sizes consistent
            font=dict(size=12)      # Reasonable font size for legend
        )
    )
    
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

def get_closest_station(coordinates):
    df = call_data()
    df['distance'] = df.apply(lambda x: call_calculate_distance(coordinates, (x['properties.y'], x['properties.x'])), axis=1)
    closest_station = df[df['distance'] == df['distance'].min()]
    return closest_station.iloc[0]

# Initialisation de l'application
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)
app.layout = html.Div(
    className="app-container",
    children=[
        # En-tête
        html.Div(
            className="header",
            children=[
                html.Div(
                    className="logo",
                    children=[
                        html.Img(
                            src="https://4.bp.blogspot.com/-eIx0Q3dB_C8/Tmm-4ZmEouI/AAAAAAAAEuA/BASGE7LdYVw/s1600/v-lille.png",
                            alt="Logo V'Lille"
                        )
                    ]
                ),
                html.Div(
                    className="title",
                    children=[
                        html.H1("V'Lille en temps réel"),
                        html.P(f"Réalisé par Martin Coulon, Donnée V'Lille récupérée le {dt.datetime.now().strftime('%d/%m/%Y à %H:%M')}")
                    ]
                ),
                html.Div(
                    className="logo",
                    children=[
                        html.Img(
                            src="https://4.bp.blogspot.com/-eIx0Q3dB_C8/Tmm-4ZmEouI/AAAAAAAAEuA/BASGE7LdYVw/s1600/v-lille.png",
                            alt="Logo V'Lille"
                        )
                    ]
                ),
            ]
        ),
        
        # Contenu principal
        html.Div(
            className="main-content",
            children=[
                # Section des adresses (deux colonnes)
                html.Div(
                    className="address-columns",
                    children=[
                        # Colonne de gauche (adresse de départ)
                        html.Div(
                            className="address-column",
                            children=[
                                html.H2("Votre adresse de départ :", className="input-label"),
                                dcc.Input(
                                    id="Adresse_Depart",
                                    type="text",
                                    placeholder="Renseignez l'adresse complète",
                                    value="13 Rue Auguste Angellier, 59000 Lille",
                                    className="input-box",
                                    debounce=True
                                ),
                                html.H3("L'arrêt le plus proche avec des vélos disponibles est :", className="result-label"),
                                html.Div(id="Arret_Depart", className="result-box")
                            ]
                        ),
                        
                        # Colonne de droite (adresse d'arrivée)
                        html.Div(
                            className="address-column",
                            children=[
                                html.H2("Votre adresse d'arrivée :", className="input-label"),
                                dcc.Input(
                                    id="Adresse_Arrivee",
                                    type="text",
                                    placeholder="Renseignez l'adresse complète",
                                    className="input-box",
                                    debounce=True
                                ),
                                html.H3("L'arrêt le plus proche avec des places disponibles est :", className="result-label"),
                                html.Div(id="Arret_Arrivee", className="result-box")
                            ]
                        )
                    ]
                ),
                
                # Section des filtres
                html.Div(
                    className="filter-section",
                    children=[
                        html.Div(
                            className="filter-title",
                            children=["Filtrer les arrêts disponibles par quartier"]
                        ),
                        dcc.Dropdown(
                            id="Ville_Selector",
                            options=[{"label": v, "value": v} for v in list(df['properties.commune'].unique())],
                            value=["LILLE"],
                            multi=True,
                            className="dropdown"
                        ),
                        html.Div(
                            className="filter-options",
                            children=[
                                html.Div(
                                    className="checkbox-container",
                                    children=[
                                        dcc.Checklist(
                                            id="Show_Available",
                                            options=[{"label": "Afficher uniquement les arrêts disponibles", "value": "show_available"}],
                                            className="checkbox"
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="checkbox-container",
                                    children=[
                                        dcc.Checklist(
                                            id="Show_Nearby",
                                            options=[{"label": "Afficher uniquement les arrêts à - de 250m", "value": "show_nearby"}],
                                            className="checkbox"
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                # Section de sélection des arrêts
                html.Div(
                    className="station-selector",
                    children=[
                        html.H2("Sélectionner le ou les arrêt(s) qui vous intéressent", className="section-title"),
                        dcc.Dropdown(
                            id="Arret_Selector",
                            options=[{"label": v, "value": v} for v in list(df['properties.nom'].unique())],
                            value=["BRULE MAISON", "GARE LILLE EUROPE", "EURALILLE", "FLANDRES EURALILLE", "GARE LILLE FLANDRES"],
                            multi=True,
                            className="dropdown"
                        )
                    ]
                ),
                
                # Information sur les arrêts sélectionnés
                html.Div(
                    className="station-info",
                    children=[
                        html.Div("Information à partir des arrêts sélectionnées :"),
                        html.Div(id="Result_Station")
                    ]
                ),
                
                # Carte interactive
                html.Div(
                    className="map-container",
                    children=[
                        html.H2("Carte interactive", className="map-title"),
                        dcc.Graph(id="Map", figure=create_map(df))
                    ]
                )
            ]
        ),
        
        # Stockage des données
        dcc.Store(id="store_ville_selected", storage_type="memory"),
        dcc.Interval(
        id='interval-component',
        interval=1000000,  # in milliseconds - update every 1000 second
        n_intervals=0
        ),
        html.Div([
        dcc.Store(id='screen-size', storage_type='memory'),
        html.Div(id='screen-size-container')
    ]),
    ]
)

# Callback pour les arrêts proches de l'adresse de départ
@app.callback(
    Output("Arret_Depart", "children"),
    Input("Adresse_Depart", "value")
)
def update_arret_depart(address):
    if not address:
        return "Veuillez entrer une adresse"
    
    try:
        coordinates = call_address_to_coordinates(address)
        station = get_closest_station(coordinates)
        return f"L'arrêt {station['properties.nom']} avec {station['properties.nb_velos_dispo']} vélos disponibles"
    except:
        return "Adresse non trouvée"

# Callback pour les arrêts proches de l'adresse d'arrivée
@app.callback(
    Output("Arret_Arrivee", "children"),
    Input("Adresse_Arrivee", "value")
)
def update_arret_arrivee(address):
    if not address:
        return "Veuillez entrer une adresse"
    
    try:
        coordinates = call_address_to_coordinates(address)
        station = get_closest_station(coordinates)
        return f"L'arrêt {station['properties.nom']} avec {station['properties.nb_places_dispo']} places disponibles"
    except:
        return "Adresse non trouvée"

# Clientside callback to get screen dimensions
app.clientside_callback(
    """
    function(n_intervals) {
        return {
            width: window.innerWidth,
            height: window.innerHeight,
            isPortrait: window.innerHeight > window.innerWidth
        }
    }
    """,
    Output('screen-size', 'data'),
    [Input('interval-component', 'n_intervals')]
)
# Callback pour filtrer les arrêts et mettre à jour la carte
@app.callback(
    [Output("store_ville_selected", "data"),
     Output("Arret_Selector", "options"),
     Output("Result_Station", "children"),
     Output("Map", "figure")],
    [Input("Ville_Selector", "value"),
     Input("Arret_Selector", "value"),
     Input("Show_Available", "value"),
     Input("Show_Nearby", "value"),
     Input("Adresse_Depart", "value"),
     Input("screen-size", "data")]  
)
def update_data(ville_selected, arret_selected, show_available, show_nearby, address_depart, screen_size):
    df = call_data()

    if ville_selected:
        df = df[df['properties.commune'].isin(ville_selected)]

    if show_available:
        df = df[df['properties.nb_velos_dispo'] > 0]

    if show_nearby and address_depart:
        coordinates = call_address_to_coordinates(address_depart)
        df['distance'] = df.apply(lambda x: call_calculate_distance(coordinates, (x['properties.y'], x['properties.x'])), axis=1)
        df = df[df['distance'] <= 250]
    
    available_arrets = [{"label": v, "value": v} for v in df['properties.nom'].unique()]

    if arret_selected:
        df = df[df['properties.nom'].isin(arret_selected)]
        result_station = [
            html.Div(f"Pour l'arrêt {row['properties.nom']}, il y a {row['properties.nb_places_dispo']} places disponibles et {row['properties.nb_velos_dispo']} vélos disponibles")
            for _, row in df.iterrows()
        ]
    else:
        result_station = [html.Div("Aucun arrêt sélectionné")]
    # Determine if legend should be visible based on screen size
    show_legend = False
    print(f"triger numéro {dt.datetime.now().strftime('%d/%m/%Y à %H:%M à %S')} : ",screen_size)
    if screen_size and 'width' in screen_size and 'isPortrait' in screen_size:
        width = screen_size['width']
        is_portrait = screen_size['isPortrait']
        # Show legend on portrait mobile devices
        if width > 600:
            show_legend = True
    
    fig = create_map(df, show_legend=show_legend)

    return ville_selected, available_arrets, result_station, fig

server = app.server
if __name__ == "__main__":
    app.run(debug=True, port=8152)
# %%
