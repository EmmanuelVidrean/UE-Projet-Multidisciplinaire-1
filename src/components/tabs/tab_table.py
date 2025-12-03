from dash import html, dash_table, callback, Input, Output
from src.utils.get_data import load_unesco_data
import pandas as pd

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Table View", style={"marginBottom": "16px"}),
            dash_table.DataTable(
                id='sites-table',
                columns=[
                    {'name': 'Site Name', 'id': 'name_en'},
                    {'name': 'Category', 'id': 'category'},
                    {'name': 'Country', 'id': 'states_name_en'},
                    {'name': 'Region', 'id': 'region_en'},
                    {'name': 'Inscription Date', 'id': 'date_inscribed'},
                ],
                data=load_unesco_data()[['name_en', 'category', 'states_name_en', 'region_en', 'date_inscribed']].to_dict('records'),
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_header={
                    'backgroundColor': '#0066cc',
                    'color': 'white',
                    'fontWeight': 'bold',
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f9f9f9',
                    }
                ],
            ),
        ],
    )


@callback(
    Output('sites-table', 'data'),
    Input('filter-category', 'value'),
    Input('filter-state', 'value'),
    Input('filter-region', 'value'),
    Input('filter-search', 'value'),
    Input('filter-years', 'value'),
)
def update_table(category, state, region, search_text, year_range):
    """
    Met à jour le tableau en fonction des filtres sélectionnés.
    """
    df = load_unesco_data().copy()
    
    # Appliquer les filtres
    if category and category != 'all':
        df = df[df['category'] == category]
    
    if state and state != 'all':
        df = df[df['states_name_en'] == state]
    
    if region and region != 'all':
        df = df[df['region_en'] == region]
    
    if search_text:
        df = df[df['name_en'].str.contains(search_text, case=False, na=False)]
    
    # Filtre par année d'inscription
    if year_range:
        df.loc[:, 'year_inscribed'] = pd.to_numeric(df['date_inscribed'], errors='coerce')
        df = df[(df['year_inscribed'] >= year_range[0]) & (df['year_inscribed'] <= year_range[1])]
    
    return df[['name_en', 'category', 'states_name_en', 'region_en', 'date_inscribed']].to_dict('records')
