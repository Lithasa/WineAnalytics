import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True)

# Load dataset
df = pd.read_csv("updated_wine.csv")

# Precompute correlation coefficients
correlation_fig2 = np.corrcoef(df['Price'], df['Rating'])[0, 1]
correlation_fig4 = np.corrcoef(df['Alcohol content'], df['Rating'])[0, 1]

# Columns for dropdown
columns_to_plot = ['Bold', 'Tannin', 'Sweet', 'Acidic']


def create_charts(selected_column):
    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()
    avg_rating_by_flavour = df.groupby('Rating', as_index=False)[selected_column].mean()
    avg_rating_by_alcohol = df.groupby('Alcohol content')['Rating'].mean().reset_index()

    fig1 = px.line(
        avg_price_by_year,
        x='Year',
        y='Price',
        title='Variation of Price Over Years',
        labels={'Year': 'Manufactured Year', 'Price': 'Wine Price'}
    )
    fig1.add_trace(go.Scatter(
        x=avg_price_by_year['Year'],
        y=avg_price_by_year['Price'],
        mode='lines',
        name='Price Trend',
        line=dict(color='#048ce0', width=2)
    ))

    return fig1

app.layout = html.Div([
    html.H1("Wine Data Analysis", style={'textAlign': 'center'}),

    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Price vs Year', value='tab1'),
        dcc.Tab(label='Price vs Rating', value='tab2'),
    ]),

    html.Div(id='tabs-content')
])

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)

def update_tab_content(selected_tab):
    return dcc.Graph(figure=fig1)
    
if __name__ == '__main__':
    app.run_server(debug=True)