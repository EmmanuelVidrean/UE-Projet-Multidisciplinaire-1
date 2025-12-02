from dash import html, dash_table, callback, Input, Output
from src.utils.get_data import load_unesco_data

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Vue Tableau", style={"marginBottom": "16px"}),
            dash_table.DataTable(
                id='sites-table',
                columns=[
                    {'name': 'Nom du site', 'id': 'name_en'},
                    {'name': 'Catégorie', 'id': 'category'},
                    {'name': 'Pays', 'id': 'states_name_en'},
                    {'name': 'Région', 'id': 'region_en'},
                ],
                data=load_unesco_data()[['name_en', 'category', 'states_name_en', 'region_en']].to_dict('records'),
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
)
def update_table(category, state, region, search_text):
    """
    Met à jour le tableau en fonction des filtres sélectionnés.
    """
    df = load_unesco_data()
    
    # Appliquer les filtres
    if category and category != 'all':
        df = df[df['category'] == category]
    
    if state and state != 'all':
        df = df[df['states_name_en'] == state]
    
    if region and region != 'all':
        df = df[df['region_en'] == region]
    
    if search_text:
        df = df[df['name_en'].str.contains(search_text, case=False, na=False)]
    
    return df[['name_en', 'category', 'states_name_en', 'region_en']].to_dict('records')
