import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1(children=''),

    html.Div(children='''
        Welcome to my project for History of Mathematics, 2022.\n
        I do not do web development, and this will be made painfully clear to you\n
        as you navigate this site.
    '''),
    html.Div(children='''
        The links above provide access to various parts of the site. Most interesting is the "Graph" link, where I demonstrate constructions my mathematician did.
    '''),

])