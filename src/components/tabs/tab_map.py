from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
from src.components.site_modal import site_modal 
from src.utils.get_data import (
    load_unesco_data,
    get_coords_dict,
    get_site_by_unique_number,
)


def make_world_map_figure(filtered_df=None):
    """
    Crée une carte du monde avec Plotly (Scattergeo),
    avec un point par site UNESCO.
    Si filtered_df est fourni, utilise ce DataFrame filtré.
    """
    if filtered_df is None:
        filtered_df = load_unesco_data()
    
    unique_numbers = filtered_df["unique_number"].dropna().tolist()
    coords_dict = get_coords_dict(unique_numbers)

    lats = []
    lons = []
    names = []
    descriptions = []
    ids = []

    for unique_num, (lon, lat) in coords_dict.items():
        site = get_site_by_unique_number(unique_num) or {}

        name = site.get("name_en") or f"Site #{unique_num}"
        desc = site.get("short_description_en", "No description available.")

        lats.append(lat)
        lons.append(lon)
        names.append(name)
        descriptions.append(desc)
        ids.append(unique_num)

    fig = go.Figure(
        go.Scattergeo(
            lat=lats,
            lon=lons,
            mode="markers",
            marker=dict(
                size=8,
                color="#0066cc",
            ),
            text=names,
            hovertemplate="%{text}<extra></extra>",
            customdata=list(zip(ids, names, descriptions)),
        )
    )

    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor="#f0f0f0",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode="event+select",
    )

    return fig



def layout():
    """
    Layout de l’onglet Carte avec :
    - la map Plotly
    """
    return html.Div(
        id="tab-map-content",
        style={
            "height": "80%", 
            "width": "80%",
            "margin": "0 auto",
            "padding": "24px",
            "alignItems": "center",
            "justifyContent": "center",
        },
        children=[
            html.H3("World Map of UNESCO World Heritage Sites"),
            dcc.Graph(
                id="world-map",
                figure=make_world_map_figure(),
                style={"width": "100%", "height": "600px"},
            ),

            site_modal(),
        ],
    )

@callback(
    Output("site-modal", "is_open"),
    Output("modal-title", "children"),
    Output("modal-body", "children"),
    Input("world-map", "clickData"),
    State("site-modal", "is_open"),
)
def toggle_modal(clickData, is_open):
    # Quand on clique sur un point de la carte
    if clickData:
        point = clickData["points"][0]
        unique_num, name, desc = point["customdata"]

        # On récupère toutes les infos du site
        site = get_site_by_unique_number(unique_num) or {}

        category = site.get("category", "Unknown")
        year = site.get("date_inscribed", "Unknown")
        region = site.get("region_en", "Unknown")
        country = site.get("states_name_en", "Unknown")
        hectares = site.get("area_hectares", site.get("hectares", "Unknown"))
        desc = site.get("short_description_en", "No description available.")

        body=[]
        
        return True, name, body
    
    return is_open, "", ""
