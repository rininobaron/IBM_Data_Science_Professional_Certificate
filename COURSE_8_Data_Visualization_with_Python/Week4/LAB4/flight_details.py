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

""" Compute_info function description

This function takes in airline data and selected year as an input and performs computation for creating charts and plots.

Arguments:
    airline_data: Input airline data.
    entered_year: Input year for which computation needs to be performed.
    
Returns:
    Computed average dataframes for carrier delay, weather delay, NAS delay, security delay, and late aircraft delay.

"""
def compute_info(airline_data, entered_year):
    # Select data
    df =  airline_data[airline_data['Year']==int(entered_year)]
    # Compute delay averages
    target_columns = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
    avg_car = []
    for col in target_columns:
       avg_car.append(df.groupby(['Month','Reporting_Airline'])[col].mean().reset_index())
    return avg_car

# Callback decorator
graphs = ['carrier-plot', 'weather-plot', 'nas-plot', 'security-plot', 'late-plot']
@app.callback([Output(component_id=graph, component_property='figure') for graph in graphs],
               Input(component_id='input-year', component_property='value'))

# Computation to callback function and return graph
def get_graph(entered_year):
    
    # Compute required information for creating graph from the data
    dataframes = compute_info(airline_data, entered_year)

    # Build Line plots
    plots = []
    targets = [('CarrierDelay', 'carrier'), ('WeatherDelay', 'weather'), ('NASDelay', 'NAS'), ('SecurityDelay', 'Security'), ('LateAircraftDelay', 'late aircraft')]
    for (col, name), df in zip(targets, dataframes):
       plots.append(px.line(df, x='Month', y=col, color='Reporting_Airline', title='Average '+name+' time (minutes) by airline'))
            
    return plots

# Run the app
if __name__ == '__main__':
    app.run_server()