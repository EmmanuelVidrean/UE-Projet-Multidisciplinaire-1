from dash import html, dcc
from src.utils.get_data import get_all_categories, get_all_states_name, get_all_region_name

def filters_bar():
    """
    Barre de filtres en haut de la page DataViz.
    Permet de filtrer les sites UNESCO par catégorie, pays et région.
    """
    # Récupération des options pour les dropdowns
    categories = get_all_categories()
    states = sorted(get_all_states_name())
    regions = sorted(get_all_region_name())
    
    return html.Div(
        style={
            "padding": "20px",
            "marginBottom": "20px",
            "borderRadius": "8px",
            "backgroundColor": "#f8f9fa",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        },
        children=[
            html.H3("Filtres", style={"marginBottom": "16px", "color": "#333"}),
            
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "16px",
                },
                children=[
                    # Filtre par catégorie
                    html.Div([
                        html.Label("Catégorie", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-category',
                            options=[{'label': 'Toutes les catégories', 'value': 'all'}] + 
                                    [{'label': cat, 'value': cat} for cat in categories],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                    
                    # Filtre par pays
                    html.Div([
                        html.Label("Pays", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-state',
                            options=[{'label': 'Tous les pays', 'value': 'all'}] + 
                                    [{'label': state, 'value': state} for state in states],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                    
                    # Filtre par région
                    html.Div([
                        html.Label("Région", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-region',
                            options=[{'label': 'Toutes les régions', 'value': 'all'}] + 
                                    [{'label': region, 'value': region} for region in regions],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                ],
            ),
            
            # Barre de recherche
            html.Div(
                style={"marginTop": "16px"},
                children=[
                    html.Label("Recherche par nom", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                    dcc.Input(
                        id='filter-search',
                        type='text',
                        placeholder='Rechercher un site par nom...',
                        style={
                            "width": "100%",
                            "padding": "8px",
                            "borderRadius": "4px",
                            "border": "1px solid #ccc",
                        }
                    ),
                ]
            ),
        ],
    )
