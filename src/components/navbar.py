from dash import html, dcc

def navbar():
    return html.Nav(
        children=[
            html.Div(
                "UNESCO Dashboard",
            ),
            html.Div(
                children=[
                    dcc.Link(
                        "Home",
                        href="/",
                    ),
                    dcc.Link(
                        "Data visualization",
                        href="/dataviz",
                    ),
                ],
            ),
        ],
    )