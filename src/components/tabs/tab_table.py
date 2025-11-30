from dash import html

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Vue Tableau"),
            html.P("Ici on affichera un tableau des sites UNESCO."),
        ],
    )
