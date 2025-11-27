from dash import Dash, html, dcc, Input, Output
import src.components.navbar as navbar_module
import src.components.footer as footer_module
from src.pages.home import layout as home_layout

def dataviz_layout():
    """Page Data visualization (placeholder pour l’instant)."""
    return html.Div(
        children=[
            html.H1("Data visualization"),
            html.P(
                "Ici, tu ajouteras plus tard les cartes, tableaux et "
                "graphiques liés aux données UNESCO."
            ),
        ],
    )

app = Dash(__name__, suppress_callback_exceptions=True) #dataviz n'existe pas encore et pour pas crash

def serve_layout():
    """Layout global : navbar + contenu + footer."""
    return html.Div(
        children=[
            dcc.Location(id="url"),
            navbar_module.navbar(),
            html.Div(
                id="page-content",
            ),
            footer_module.footer(),
        ]
    )

app.layout = serve_layout

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname"),
)
def display_page(pathname: str):
    if pathname == "/dataviz":
        return dataviz_layout()
    # par défaut : home
    return home_layout()

if __name__ == "__main__":
    app.run(debug=True)
