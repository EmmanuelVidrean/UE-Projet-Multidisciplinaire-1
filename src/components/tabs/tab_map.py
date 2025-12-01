from dash import html
import folium
from folium.plugins import MarkerCluster

from src.utils.get_data import (
    get_all_unique_numbers,
    get_coords_dict,
    get_site_by_unique_number,
)


def make_world_map_html():
    """
    Crée une carte du monde avec Folium et place tous les sites UNESCO.
    """

    m = folium.Map(
        location=[0, 0],
        zoom_start=2,
        tiles=None,
        max_bounds=True,
        min_zoom=2,
        width="100%",
        height="100%",
    )

    folium.TileLayer(
        tiles="CartoDB positron",
        name="CartoDB positron",
        attr="Map tiles by CartoDB, CC BY 3.0 — Map data © OpenStreetMap",
        control=False,
    ).add_to(m)

    return m._repr_html_()


def layout():
    """
    Layout de l’onglet Carte.
    """
    world_map_html = make_world_map_html()

    return html.Div(
        id="tab-map-content",
        children=[
            html.H3("Carte du monde"),
            html.Iframe(
                id="world-map",
                srcDoc=world_map_html,
                style={
                    "width": "100%",
                    "height": "600px",
                    "border": "none",
                },
            ),
        ],
        style={"height": "100%", "width": "100%"},
    )
