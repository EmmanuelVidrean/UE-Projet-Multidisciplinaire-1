from dash import html

def layout():
    """
    Layout de la page d'accueil (Home).
    Titre + texte explicatif à gauche, image à droite.
    """
    return html.Div(
        style={
            "minHeight": "100vh",
            "padding": "40px 40px 80px",  # pour laisser la place au footer
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "center",
                    "gap": "40px",
                },
                children=[
                    # Colonne gauche : titre + texte
                    html.Div(
                        style={"flex": "1"},
                        children=[
                            html.H1(
                                "UNESCO Data Dashboard",
                                style={"marginBottom": "20px"},
                            ),
                            html.P(
                                "Ce dashboard permet d’explorer les sites "
                                "inscrits au patrimoine mondial de l’UNESCO "
                                "à travers des cartes, tableaux et graphiques "
                                "interactifs.",
                                style={"fontSize": "18px", "lineHeight": "1.5"},
                            ),
                        ],
                    ),
                    # Colonne droite : image
                    html.Div(
                        style={"flex": "1", "textAlign": "right"},
                        children=[
                            html.Img(
                                src="/assets/landing_image.png",
                                style={
                                    "maxWidth": "100%",
                                    "height": "80vh",
                                    "borderRadius": "8px",
                                    "boxShadow": "0 2px 8px rgba(0,0,0,0.1)",
                                },
                            )
                        ],
                    ),
                ],
            )
        ],
    )
