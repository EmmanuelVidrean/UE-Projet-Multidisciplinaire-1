from dash import html

def filters_bar():
    """
    Barre de filtres en haut de la page DataViz.
    (Recherche, dropdowns, sélecteurs, bouton Rechercher...)
    Manu c'est à toi de travailler la dessus (je vais te démarrer si tu le fais pas)
    """
    return html.Div(
        style={
            "padding": "16px 24px",
            "marginBottom": "16px",
            "borderRadius": "8px",
            "backgroundColor": "#f5f5f5",
            "display": "flex",
            "gap": "16px",
            "alignItems": "center",
            "flexWrap": "wrap",
        },
        children=[
            html.Strong("Filtres (placeholder)"),
            html.Span(
                "Ici on ajoutera : barre de recherche, dropdowns, sélecteur d'année, bouton Rechercher...",
                style={"fontSize": "14px", "color": "#555"},
            ),
        ],
    )
