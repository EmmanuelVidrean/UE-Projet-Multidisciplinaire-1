# src/pages/home.py

from dash import html

def layout():
    """
    Layout de la page d'accueil (Home).
    Titre + texte explicatif à gauche, image à droite.
    """
    return html.Div(
        children=[
            html.Div(
                children=[
                    # Colonne gauche : titre + texte
                    html.Div(
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
                            )
                        ],
                    ),
                ],
            )
        ],
    )
