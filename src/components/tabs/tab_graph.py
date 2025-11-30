from dash import html

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Vue Graphiques"),
            html.P("Ici on affichera les graphiques (barres, lignes, etc.)."),
        ],
    )
