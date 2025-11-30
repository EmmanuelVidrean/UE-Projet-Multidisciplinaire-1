from dash import html
from src.components.filters import filters_bar

def layout():
    """
    Page Data visualization :
    - en haut : barre de filtres
    - en dessous : onglets Map / Tableau / Graphiques
    """
    return html.Div(
        style={
            "minHeight": "100vh",
            "padding": "40px 40px 80px",
        },
        children=[
            html.H1(
                "UNESCO Data Visualization",
                style={"marginBottom": "24px"},
            ),
            # la barre de filtres
            filters_bar(),

            # les différents sous onglet
        ],
    )
