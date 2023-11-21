#! /usr/bin/env python3

# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[html.H1("Flight Delay Time Statistics", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
                                html.Div(["Input Year: ", dcc.Input(id="input-year", value="2010", type="number")],
                                style={'height': '35px', 'font-size': 30}),
                                html.Br(),
                                html.Br(), 
                                html.Div([
                                        html.Div(dcc.Graph(id="carrier-plot")),
                                        html.Div(dcc.Graph(id="weather-plot"))
                                ], style={'display': 'flex'}),
    
                                html.Div([
                                        html.Div(dcc.Graph(id="nas-plot")),
                                        html.Div(dcc.Graph(id="security-plot"))
                                ], style={'display': 'flex'}),
                                
                                html.Div(dcc.Graph(id="late-plot"), style={'width':'65%'})
                                ])

# Run the app
if __name__ == '__main__':
       app.run_server()