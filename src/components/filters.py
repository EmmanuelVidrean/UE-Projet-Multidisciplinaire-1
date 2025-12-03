from dash import html, dcc
import pandas as pd
from src.utils.get_data import get_all_categories, get_all_states_name, get_all_region_name, load_unesco_data

def filters_bar():
    """
    Barre de filtres en haut de la page DataViz.
    Permet de filtrer les sites UNESCO par catégorie, pays, région et année d'inscription.
    """
    # Récupération des options pour les dropdowns
    categories = get_all_categories()
    states = sorted(get_all_states_name())
    regions = sorted(get_all_region_name())
    
    # Calcul des années min/max pour le RangeSlider
    df = load_unesco_data()
    years = pd.to_numeric(df['date_inscribed'], errors='coerce').dropna().astype(int)
    min_year = int(years.min()) if not years.empty else 1900
    max_year = int(years.max()) if not years.empty else 2025
    
    return html.Div(
        style={
            "padding": "20px",
            "marginBottom": "20px",
            "borderRadius": "8px",
            "backgroundColor": "#f8f9fa",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        },
        children=[
            html.H3("Filters", style={"marginBottom": "16px", "color": "#333"}),
            
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "16px",
                },
                children=[
                    # Filtre par catégorie
                    html.Div([
                        html.Label("Category", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-category',
                            options=[{'label': 'All Categories', 'value': 'all'}] + 
                                    [{'label': cat, 'value': cat} for cat in categories],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                    
                    # Filtre par pays
                    html.Div([
                        html.Label("Country", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-state',
                            options=[{'label': 'All Countries', 'value': 'all'}] + 
                                    [{'label': state, 'value': state} for state in states],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                    
                    # Filtre par région
                    html.Div([
                        html.Label("Region", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                        dcc.Dropdown(
                            id='filter-region',
                            options=[{'label': 'All Regions', 'value': 'all'}] + 
                                    [{'label': region, 'value': region} for region in regions],
                            value='all',
                            clearable=False,
                            style={"width": "100%"}
                        ),
                    ]),
                ],
            ),

            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                    "gap": "16px",
                },
                children=[
                    # Barre de recherche
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            html.Label("Search by Name", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
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
                    # Filtre par intervalle d'années d'inscription
                    html.Div(
                        style={"marginTop": "16px"},
                        children=[
                            html.Label("Inscription Years", style={"fontWeight": "bold", "marginBottom": "8px", "display": "block"}),
                            dcc.RangeSlider(
                                id='filter-years',
                                min=min_year,
                                max=max_year,
                                value=[min_year, max_year],
                                marks={str(y): str(y) for y in range(min_year, max_year+1, max(1, (max_year-min_year)//6))},
                                tooltip={"placement": "bottom", "always_visible": True},
                                allowCross=False,
                            ),
                        ]
                    ),
                ],
            ),
            
        ],
    )
