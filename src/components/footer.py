from dash import html, dcc

def footer():
    return html.Footer(
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
    )
