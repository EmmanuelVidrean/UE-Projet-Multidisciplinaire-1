from dash import html

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Vue Carte"),
            html.P("Ici on affichera la carte interactive des sites UNESCO."),
        ],
    )
