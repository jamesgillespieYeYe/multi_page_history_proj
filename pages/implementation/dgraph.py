import dash
from dash import html, dcc
import os

dash.register_page(
	__name__,
)


layout = html.Div(children=[
    html.H1(children='Graph'),

    html.Div(children='''
        Boring and complicated implementation stuff for the graph page
    '''),
    html.Iframe(src=os.path.join("../assets", "graph.py"), width="100%", height="1000")

])