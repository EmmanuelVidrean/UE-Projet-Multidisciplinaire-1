#
# Imports
#
import plotly.express as px
from dash import Dash, dcc, html

#
# Data
#
year = 2002
gapminder = px.data.gapminder()
years = gapminder["year"].unique()
data = {year: gapminder.query("year == @year") for year in years}

#
# Main
#
if __name__ == '__main__':
    app = Dash(__name__)

    fig = px.scatter(
        data[year],
        x="gdpPercap",
        y="lifeExp",
        color="continent",
        size="pop",
        hover_name="country",
        title=f"Life Expectancy vs GDP per Capita ({year})"
    )

    app.layout = html.Div([
        html.H1(
            children=f'Life expectancy vs GDP per capita ({year})',
            style={'textAlign': 'center', 'color': '#0078D7'}
        ),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),

        html.Div(
            children=f"""
            The graph above shows the relationship between life expectancy and GDP per capita 
            for the year {year}. Each continent has its own color, and bubble size 
            is proportional to the country's population.
            Mouse over the points for details.
            """
        ),
    ])

    #
    # RUN APP
    #
    app.run(debug=False)
