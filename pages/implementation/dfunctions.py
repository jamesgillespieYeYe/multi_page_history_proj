import dash
from dash import html, dcc
import os

dash.register_page(
	__name__,
)


layout = html.Div(children=[
    html.H1(children='Functions'),

    html.Div(children='''
        functions.py contains the implementation of Axioms - drawing a point, drawing a circle through two points, drawing a line segment through two points, and taking the intersection of two lines/curves
    '''),
    html.Iframe(src=os.path.join("../assets", "functions.py"), width="100%", height="1000")

])