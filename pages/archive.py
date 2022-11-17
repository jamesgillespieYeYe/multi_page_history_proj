import dash
from dash import html, dcc
import os

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Archive page'),

    html.Div(children='''
        This is our Archive page content.
    '''),
    #html.Iframe(src="https://docs.google.com/document/d/e/2PACX-1vSB0XVIcy4sIFhtbb3opECAP5GSMm-K9lAoOsJxg-KYsZRMneISm_dAnZ-s_gkKVNt1N8bj91th7uFR/pub?embedded=true")
    #html.Iframe(src="/mnt/c/test_pages/pages/assets/mypdf.pdf"),
    html.Iframe(src=os.path.join("assets", "mypdf.pdf"), width="100%", height="1000"),
    html.Iframe(src=os.path.join("assets", "functions.py"), width="100%", height="1000")


])

print(os.path.join("assets", "mypdf.pdf"))