from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from src.utils.get_data import load_unesco_data
import pandas as pd

def layout():
    return html.Div(
        style={"padding": "24px"},
        children=[
            html.H3("Charts View", style={"marginBottom": "16px"}),
            dcc.Graph(
                id='sites-by-country-graph',
                style={'height': '600px'}
            ),
            dcc.Graph(
                id='sites-by-category-bar',
                style={'height': '600px', 'marginTop': '40px'}
            ),
            dcc.Graph(
                id='sites-by-area-histogram',
                style={'height': '600px', 'marginTop': '40px'}
            ),
        ],
    )


@callback(
    Output('sites-by-country-graph', 'figure'),
    Input('filter-category', 'value'),
    Input('filter-state', 'value'),
    Input('filter-region', 'value'),
    Input('filter-search', 'value'),
    Input('filter-years', 'value'),
)
def update_graph(category, state, region, search_text, year_range):
    """
    Met à jour le graphique en fonction des filtres sélectionnés.
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
    
    # Convertir area_hectares et date_inscribed en numérique
    df.loc[:, 'area_hectares'] = pd.to_numeric(df['area_hectares'], errors='coerce')
    df.loc[:, 'date_inscribed'] = pd.to_numeric(df['date_inscribed'], errors='coerce')
    
    # Supprimer les valeurs manquantes
    df_with_data = df.dropna(subset=['area_hectares', 'date_inscribed'])
    
    # Grouper par pays et région
    country_stats = df_with_data.groupby(['states_name_en', 'region_en']).agg({
        'area_hectares': 'mean',
        'date_inscribed': 'mean',
        'unique_number': 'count'
    }).reset_index()
    country_stats.columns = ['country', 'region', 'superficie_moyenne', 'annee_moyenne', 'total_sites']
    
    # Trier par nombre total de sites et limiter aux 50 premiers
    country_stats = country_stats.sort_values('total_sites', ascending=False).head(50)
    
    # Créer le scatter plot avec plotly express
    fig = px.scatter(
        country_stats,
        x='superficie_moyenne',
        y='annee_moyenne',
        size='total_sites',
        color='region',
        hover_name='country',
        hover_data={
            'region': True, 
            'superficie_moyenne': ':.2f',
            'annee_moyenne': ':.0f',
            'total_sites': True
        },
        labels={
            'superficie_moyenne': 'Average Area (hectares)',
            'annee_moyenne': 'Average Inscription Year',
            'region': 'Region',
            'total_sites': 'Number of Sites'
        },
        title='Top 50 Countries: Average Area vs Average Inscription Year',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    # Mise à jour du layout
    fig.update_traces(
        mode='markers'
    )
    
    fig.update_layout(
        template='plotly_white',
        height=600,
        title_font_size=20,
        showlegend=True,
        legend_title_text='Région',
        xaxis_type='log'
    )
    
    return fig


@callback(
    Output('sites-by-category-bar', 'figure'),
    Input('filter-category', 'value'),
    Input('filter-state', 'value'),
    Input('filter-region', 'value'),
    Input('filter-search', 'value'),
    Input('filter-years', 'value'),
)
def update_bar_graph(category, state, region, search_text, year_range):
    """
    Met à jour le graphique en barres en fonction des filtres sélectionnés.
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
    
    # Compter le nombre de sites par pays et catégorie
    country_category_stats = df.groupby(['states_name_en', 'category']).size().reset_index(name='count')
    
    # Vérifier s'il y a des données
    if country_category_stats.empty:
        # Retourner un graphique vide avec un message
        fig = go.Figure()
        fig.update_layout(
            template='plotly_white',
            height=600,
            title='Top 30 Countries: Distribution of Sites by Category',
            xaxis={'visible': False},
            yaxis={'visible': False},
            annotations=[{
                'text': 'No data available for the selected filters',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig
    
    # Calculer le total par pays pour trier
    country_totals = country_category_stats.groupby('states_name_en')['count'].sum().reset_index()
    country_totals.columns = ['states_name_en', 'total']
    
    # Trier et limiter aux 30 premiers pays
    top_countries = country_totals.sort_values('total', ascending=False).head(30)
    
    # Filtrer les données pour ne garder que les 30 premiers pays
    country_category_stats = country_category_stats[
        country_category_stats['states_name_en'].isin(top_countries['states_name_en'])
    ]
    
    fig = px.bar(
        country_category_stats,
        x='states_name_en',
        y='count',
        color='category',
        hover_data={'count': True, 'category': True},
        labels={
            'states_name_en': 'Country',
            'count': 'Number of Sites',
            'category': 'Category'
        },
        title='Top 30 Countries: Distribution of Sites by Category',
        color_discrete_map={
            'Cultural': '#1f77b4',
            'Natural': '#2ca02c',
            'Mixed': '#ff7f0e'
        }
    )
    
    # Mise à jour du layout
    fig.update_layout(
        template='plotly_white',
        height=600,
        title_font_size=20,
        xaxis_tickangle=-45,
        showlegend=True,
        legend_title_text='Category',
        barmode='stack'
    )
    
    return fig


@callback(
    Output('sites-by-area-histogram', 'figure'),
    Input('filter-category', 'value'),
    Input('filter-state', 'value'),
    Input('filter-region', 'value'),
    Input('filter-search', 'value'),
    Input('filter-years', 'value'),
)
def update_area_histogram(category, state, region, search_text, year_range):
    """
    Met à jour l'histogramme de la distribution des superficies des sites.
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
    
    # Convertir area_hectares en numérique et en km²
    df.loc[:, 'area_hectares'] = pd.to_numeric(df['area_hectares'], errors='coerce')
    df.loc[:, 'area_km2'] = df['area_hectares'] / 100  # 1 km² = 100 hectares
    
    # Supprimer les valeurs manquantes et les valeurs nulles
    df_with_area = df.dropna(subset=['area_km2']).copy()
    df_with_area = df_with_area[df_with_area['area_km2'] > 0]
    
    # Créer des tranches de superficie
    bins = [0, 5, 10, 50, 100, 500, 1000, 5000, float('inf')]
    labels = ['0-5 km²', '5-10 km²', '10-50 km²', '50-100 km²', '100-500 km²', 
              '500-1000 km²', '1000-5000 km²', '5000+ km²']
    
    df_with_area.loc[:, 'superficie_range'] = pd.cut(df_with_area['area_km2'], bins=bins, labels=labels, include_lowest=True)
    
    # Compter le nombre de sites par tranche
    area_counts = df_with_area['superficie_range'].value_counts().sort_index().reset_index()
    area_counts.columns = ['Tranche de superficie', 'Nombre de sites']
    
    # Créer l'histogramme
    fig = px.bar(
        area_counts,
        x='Tranche de superficie',
        y='Nombre de sites',
        labels={
            'Tranche de superficie': 'Area Range',
            'Nombre de sites': 'Number of Sites'
        },
        title='Distribution of Sites by Area Range',
        color='Nombre de sites',
        color_continuous_scale='Viridis'
    )
    
    # Mise à jour du layout
    fig.update_layout(
        template='plotly_white',
        height=600,
        title_font_size=20,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    # Ajouter les valeurs sur les barres
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )
    
    return fig
