from dash import dcc
from src.components.tabs.tab_map import layout as map_layout
from src.components.tabs.tab_table import layout as table_layout
from src.components.tabs.tab_graph import layout as graph_layout

def viz_tabs():
    return dcc.Tabs(
        id="viz-tabs",
        value="tab-map",   # onglet sélectionné par défaut
        children=[
            dcc.Tab(
                label="Carte",
                value="tab-map",
                children=map_layout(),
            ),
            dcc.Tab(
                label="Tableau",
                value="tab-table",
                children=table_layout(),
            ),
            dcc.Tab(
                label="Graphiques",
                value="tab-graph",
                children=graph_layout(),
            ),
        ],
    )
