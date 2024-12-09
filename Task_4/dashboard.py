import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True)

df = pd.read_csv("updated_wine.csv")

correlation_fig2 = np.corrcoef(df['Price'], df['Rating'])[0, 1]

def create_charts():
    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()

    fig1 = px.bar(
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

    fig2 = px.scatter(
        df,
        x='Price',
        y='Rating',
        title='Average Price vs Rating',
        color='Year'
    )
    fig2.add_annotation(
        x=max(df['Price']),
        y=max(df['Rating']),
        text=f"Correlation: {correlation_fig2:.2f}",
        showarrow=False,
        font=dict(size=12)
    )

    return fig1, fig2

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
    if selected_tab == 'tab1':
        fig1, _ = create_charts()  
        return dcc.Graph(figure=fig1)
    elif selected_tab == 'tab2':
        _, fig2 = create_charts()  
        return dcc.Graph(figure=fig2)
    
if __name__ == '__main__':
    app.run_server(debug=True)