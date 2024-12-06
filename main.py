import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

df = pd.read_csv("updated_wine.csv")

unique_years = df["Year"].unique()
columns_to_plot = ['Bold', 'Tannin', 'Sweet', 'Acidic'] 

@app.callback(
    [
        Output("wine_price_vs_year", "figure"),
        Output("wine_price_vs_rating", "figure"),
        Output("Rating_vs_flavour", "figure")
    ],
    [Input("attribute-dropdown", "value")]
)

def plotCharts(selected_column):

    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()
    avg_price_by_rating = df.groupby('Rating')['Price'].mean().reset_index()
    avg_rating_by_flavour = df.groupby(selected_column)['Rating'].mean().reset_index()

    fig1 = px.histogram(
        avg_price_by_year,
        x='Year',
        y='Price',
        title='Variation of price respective to manufactured Year',
        nbins=80,
        color_discrete_sequence=['#a86b20'],
        labels={'Year': 'Manufactured Year', 'Price': 'Wine Price'},
    )

    fig2 = px.histogram(
        avg_price_by_rating,
        x='Rating',
        y='Price',
        title='Average price for the Rating',
        nbins=80,
        color_discrete_sequence=['#427ef5']
    )

    fig3 = px.histogram(
        avg_rating_by_flavour,
        x=selected_column,
        y='Rating',
        nbins=600,
        title=f"Average Wine Rating by {selected_column}",
        labels={selected_column: selected_column,'Rating':'Wine Rating'},
        color_discrete_sequence=['#ad1133']
    )

    fig3.update_layout(
        #xaxis_title = selected_column,
        yaxis_title = 'Average Rating' 
    )        

    fig1.update_layout(
        yaxis_title = 'Average wine price'
    )

    fig2.update_layout(
        yaxis_title = 'Wine Price'
    )
        
    return fig1,fig2,fig3

app.layout = html.Div([

    html.H1("Wine Data Analysis",style={'textAllign':'center'}),

    html.Div([
        dcc.Graph(
            id='wine_price_vs_year',
            
            ),
        
    ]),

    html.Div([
        dcc.Graph(
            id='wine_price_vs_rating',
            
            ),
        
    ]),

    html.Div([

        html.Label("Select Attribute:"),
        dcc.Dropdown(
            id="attribute-dropdown",
            options=[{"label": col, "value": col} for col in columns_to_plot],
            value=columns_to_plot[0],  
            clearable=False,
        ),
        dcc.Graph(
            id="Rating_vs_flavour",
            
            ),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=True)
