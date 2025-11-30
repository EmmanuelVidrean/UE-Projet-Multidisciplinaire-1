from dash import html

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
            # Barre de filtres
            # les différents sous onglet
        ],
    )
