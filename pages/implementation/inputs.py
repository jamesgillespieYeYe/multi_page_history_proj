import dash
from dash import html, dcc
import os

dash.register_page(
	__name__,
)


layout = html.Div(children=[
    html.H1(children='Constructions'),

    html.Div(children='''
        These are the lists of commands for the constructions
    '''),
    html.Iframe(src=os.path.join("../assets", "inputs.json"), width="100%", height="1000")

])