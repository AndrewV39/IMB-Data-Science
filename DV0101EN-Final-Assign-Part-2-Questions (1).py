#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Prepare list of years
year_list = sorted(data['Year'].unique())

# Initialize the app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# App layout
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={
        'textAlign': 'center',
        'color': '#5D3D36',
        'fontSize': '24px'
    }),

    html.Div([
        html.Label("Select Report Type"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
        )
    ]),

    html.Div([
        html.Label("Select Year"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0],
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlign': 'center'}
        )
    ]),

    html.Div(id='output-container', className='chart-grid', style={
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center'
    })
])

# Disable year dropdown if recession selected
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def disable_year_dropdown(stat_type):
    return stat_type == 'Recession Period Statistics'

# Update charts based on selection
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output(stat_type, selected_year):
    if stat_type == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        chart1 = dcc.Graph(figure=px.line(
            recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
            x='Year', y='Automobile_Sales',
            title="Average Automobile Sales During Recession"
        ))

        chart2 = dcc.Graph(figure=px.bar(
            recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
            x='Vehicle_Type', y='Automobile_Sales',
            title="Average Vehicles Sold by Type During Recession"
        ))

        chart3 = dcc.Graph(figure=px.pie(
            recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(),
            values='Advertising_Expenditure', names='Vehicle_Type',
            title="Ad Expenditure by Vehicle Type (Recession)"
        ))

        chart4 = dcc.Graph(figure=px.bar(
            recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index(),
            x='unemployment_rate', y='Automobile_Sales',
            color='Vehicle_Type',
            labels={'unemployment_rate': 'Unemployment Rate'},
            title="Unemployment Rate vs Vehicle Sales"
        ))

        return [html.Div(children=[chart], style={'width': '100%', 'padding': '10px'}) for chart in [chart1, chart2, chart3, chart4]]

    elif stat_type == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        chart1 = dcc.Graph(figure=px.line(
            data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
            x='Year', y='Automobile_Sales',
            title="Yearly Average Automobile Sales"
        ))

        chart2 = dcc.Graph(figure=px.line(
            yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index(),
            x='Month', y='Automobile_Sales',
            title=f"Monthly Automobile Sales in {selected_year}"
        ))

        chart3 = dcc.Graph(figure=px.bar(
            yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
            x='Vehicle_Type', y='Automobile_Sales',
            title=f"Avg Vehicles Sold by Type in {selected_year}"
        ))

        chart4 = dcc.Graph(figure=px.pie(
            yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index(),
            values='Advertising_Expenditure', names='Vehicle_Type',
            title=f"Ad Expenditure by Type in {selected_year}"
        ))

        return [html.Div(children=[chart], style={'width': '100%', 'padding': '10px'}) for chart in [chart1, chart2, chart3, chart4]]

    return html.Div("No data to display. Please make a selection.")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)