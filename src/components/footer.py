from dash import html, dcc

def footer():
    return html.Footer(
        style={
            "position": "fixed",
            "bottom": 0,
            "left": 0,
            "right": 0,
            "height": "60px",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
            "gap": "40px",
            "backgroundColor": "#f5f5f5",
            "borderTop": "1px solid #ddd",
            "zIndex": 1000,
        },
        children=[
            dcc.Link(
                "Home",
                href="/",
                style={
                    "textDecoration": "none",
                    "fontWeight": "bold",
                    "color": "#333",
                },
            ),
            dcc.Link(
                "Data visualization",
                href="/dataviz",
                style={
                    "textDecoration": "none",
                    "fontWeight": "bold",
                    "color": "#333",
                },
            ),
        ],
    )
