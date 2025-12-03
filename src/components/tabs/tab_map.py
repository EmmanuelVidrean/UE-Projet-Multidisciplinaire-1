from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

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

            dbc.Modal(
                id="site-modal",
                size="lg",
                is_open=False,
                children=[
                    dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                    dbc.ModalBody(id="modal-body"),
                ],
            ),
        ],
    )

@callback(
    Output("world-map", "figure"),
    Input("filter-category", "value"),
    Input("filter-state", "value"),
    Input("filter-region", "value"),
    Input("filter-search", "value"),
    Input("filter-years", "value"),
)
def update_map(category, state, region, search_text, year_range):
    """
    Met à jour la carte en fonction des filtres sélectionnés.
    """
    df = load_unesco_data().copy()
    
    # Appliquer les filtres
    if category and category != 'all':
        df = df[df['category'] == category]
    
    if state and state != 'all':
        df = df[df['states_name_en'] == state]
    
    if region and region != 'all':
        df = df[df['region_en'] == region]
    
    if search_text:
        df = df[df['name_en'].str.contains(search_text, case=False, na=False)]
    
    # Filtre par année d'inscription
    if year_range:
        df.loc[:, 'year_inscribed'] = pd.to_numeric(df['date_inscribed'], errors='coerce')
        df = df[(df['year_inscribed'] >= year_range[0]) & (df['year_inscribed'] <= year_range[1])]
    
    return make_world_map_figure(df)


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
        # Ouvre la modal avec le contenu
        return True, name, desc

    # Aucun clic → on ne change rien
    return is_open, "", ""
