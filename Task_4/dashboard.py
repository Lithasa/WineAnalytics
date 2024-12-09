import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True)

# Load dataset
df = pd.read_csv("updated_wine.csv")


df['Country'] = df['Country'].str.strip().str.title()

# Precompute correlation coefficients
correlation_fig2 = np.corrcoef(df['Price'], df['Rating'])[0, 1]
correlation_fig4 = np.corrcoef(df['Alcohol content'], df['Rating'])[0, 1]

# Columns for dropdown
columns_to_plot = ['Bold', 'Tannin', 'Sweet', 'Acidic']
unique_countries = df['Country'].unique()

def create_charts(selected_column, selected_country):
    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()
    avg_rating_by_flavour = df.groupby('Rating', as_index=False)[selected_column].mean()
    avg_rating_by_alcohol = df.groupby('Alcohol content')['Rating'].mean().reset_index()

    filtered_df = df[df['Country'] == selected_country]

    food_columns = df.loc[:, 'Lamb':'Aperitif'].columns
    food_counts = filtered_df[food_columns].sum().reset_index()
    food_counts.columns = ['Food Pairing','Count']
    food_counts = food_counts[food_counts['Count'] > 0]

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

    fig3 = px.bar(
        avg_rating_by_flavour,
        x='Rating',
        y=selected_column,
        color_discrete_sequence=['#07e03d'],
        title=f"Average Wine Rating by {selected_column}",
        labels={'Rating': 'Wine Rating', selected_column: selected_column}
    )

    fig4 = px.scatter(
        avg_rating_by_alcohol,
        x='Alcohol content',
        y='Rating',
        color='Rating',
        title='Rating vs Alcohol Content',
        labels={'Alcohol content': 'Alcohol Content', 'Rating': 'Rating'}
    )
    fig4.add_annotation(
        x=max(avg_rating_by_alcohol['Alcohol content']),
        y=max(avg_rating_by_alcohol['Rating']),
        text=f"Correlation: {correlation_fig4:.2f}",
        showarrow=False,
        font=dict(size=12)
    )
    fig5 = px.pie(
        food_counts,
        names='Food Pairing',
        values='Count',
        title=f'Most Common Food Pairings in {selected_country}',
        hole=0.3
    )

    
    fig6 = px.histogram(
        df,
        x = 'Rating',
        title='Distrinution of Ratings',
        nbins = 60,
        color_discrete_sequence=['#11ad74']
    )

    return fig1, fig2, fig3, fig4, fig5, fig6


app.layout = html.Div([
    html.H1("Wine Data Analysis", id="heading"),

    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Price vs Year', value='tab1'),
        dcc.Tab(label='Price vs Rating', value='tab2'),
        dcc.Tab(label='Rating vs Flavour', value='tab3'),
        dcc.Tab(label='Rating vs Alcohol Content', value='tab4')
    ]),

    html.Div(id='tabs-content')
])


@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def update_tab_content(selected_tab):
    if selected_tab == 'tab1':
        fig1, _, _, _ = create_charts('Bold')  
        return dcc.Graph(figure=fig1)
    elif selected_tab == 'tab2':
        _, fig2, _, _ = create_charts('Bold')  
        return dcc.Graph(figure=fig2)
    elif selected_tab == 'tab3':
        return html.Div([
            html.Label("Select Attribute:", style={'margin-top': '20px'}),
            dcc.Dropdown(
                id="attribute-dropdown",
                options=[{"label": col, "value": col} for col in columns_to_plot],
                value=columns_to_plot[0],  
                clearable=False
            ),
            html.Div(id='tab3-content')
        ])
    elif selected_tab == 'tab4':
        _, _, _, fig4 = create_charts('Bold')  
        return dcc.Graph(figure=fig4)


@app.callback(
    Output('tab3-content', 'children'),
    [Input('attribute-dropdown', 'value')]
)
def update_column_graph(selected_column):
    _, _, fig3, _ = create_charts(selected_column)
    return dcc.Graph(figure=fig3) 



if __name__ == '__main__':
    app.run_server(debug=True)

