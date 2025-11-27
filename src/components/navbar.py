from dash import html, dcc

def navbar():
    return html.Nav(
        style={
            "position": "sticky",
            "top": 0,
            "zIndex": 1000,
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "10px 30px",
            "backgroundColor": "#ffffff",
            "borderBottom": "1px solid #e0e0e0",
        },
        children=[
            html.Div(
                "UNESCO Dashboard",
                style={"fontWeight": "bold", "fontSize": "20px"},
            ),
            html.Div(
                style={"display": "flex", "gap": "20px"},
                children=[
                    dcc.Link(
                        "Home",
                        href="/",
                        style={
                            "textDecoration": "none",
                            "color": "#333",
                            "fontWeight": "500",
                        },
                    ),
                    dcc.Link(
                        "Data visualization",
                        href="/dataviz",
                        style={
                            "textDecoration": "none",
                            "color": "#333",
                            "fontWeight": "500",
                        },
                    ),
                ],
            ),
        ],
    )
