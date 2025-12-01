from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from src.utils.get_data import (
    get_all_unique_numbers,
    get_coords_dict,
    get_site_by_unique_number,
)


def make_world_map_figure():
    """
    Crée une carte du monde avec Plotly (Scattergeo),
    avec un point par site UNESCO.
    """
    unique_numbers = get_all_unique_numbers()
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
                size=4,
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
        ],
    )