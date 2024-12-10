import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True) 


df = pd.read_csv("updated_wine.csv")

df['Country'] = df['Country'].str.strip().str.title()
food_columns = df.loc[:, 'Lamb':'Aperitif'].columns
unique_countries = df['Country'].unique()

correlation_fig2 = np.corrcoef(df['Price'], df['Rating'])[0, 1]
correlation_fig4 = np.corrcoef(df['Alcohol content'], df['Rating'])[0, 1]


columns_to_plot = ['Bold', 'Tannin', 'Sweet', 'Acidic']
unique_countries = df['Country'].unique()


def create_charts(selected_column,selected_country):

    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()
    avg_rating_by_flavour = df.groupby('Rating', as_index=False)[selected_column].mean()
    avg_rating_by_alcohol = df.groupby('Alcohol content')['Rating'].mean().reset_index()
    filtered_df = df[df['Country'] == selected_country]
    avg_rating_country = df.groupby('Country')['Rating'].mean().reset_index()
    avg_rating_country.columns = [col.strip() for col in avg_rating_country.columns]
    #top_styles = df['Wine style'].value_counts().head(10).reset_index()
    
    food_columns = df.loc[:, 'Lamb':'Aperitif'].columns
    food_counts = filtered_df[food_columns].sum().reset_index()
    food_counts.columns = ['Food Pairing','Count']
    food_counts = food_counts[food_counts['Count'] > 0]

    top_styles_country = (
        filtered_df.groupby('Wine style')
        .agg(Count=('Wine style', 'size'), Avg_Rating=('Rating', 'mean'))
        .reset_index()
        .sort_values(by='Count', ascending=False)
        .head(10)
    )
      
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
        mode='lines+markers',  
        name='Price Trend',
        line=dict(color='#6A0DAD', width=3), 
        marker=dict(size=8, color='#6A0DAD', symbol='circle') 
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
        color='Rating',
        title=f"Average Wine Rating by {selected_column}",
        labels={'Rating': 'Wine Rating', selected_column: selected_column},
        color_continuous_scale=px.colors.sequential.Inferno
    )

    fig4 = px.scatter(
        avg_rating_by_alcohol,
        x='Alcohol content',
        y='Rating',
        color='Rating',
        title='Rating vs Alcohol Content',
        labels={'Alcohol content': 'Alcohol Content', 'Rating': 'Rating'},
        color_continuous_scale=px.colors.sequential.Turbo
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
        nbins = 20,
        color_discrete_sequence=['#BB3754']
    )

    avg_rating_country = df.groupby('Country')['Rating'].mean().reset_index()
    fig7 = px.bar(
        avg_rating_country,
        x='Rating',
        y='Country',
        color='Rating',
        orientation='h', 
        title='Average Rating by Country', 
        color_continuous_scale=px.colors.sequential.Greens
    )

    fig8 = px.bar(
        top_styles_country,
        x='Wine style',
        y='Avg_Rating',
        color='Count',
        title=f'Top 10 Wine Styles in {selected_country}',
        labels={'Wine style': 'Wine Style', 'Avg_Rating': 'Average Rating'},
        color_continuous_scale=px.colors.sequential.Viridis

    )
    fig8.update_layout(
    bargap=0.4
)

    return fig1, fig2, fig3, fig4,fig5, fig6,fig7,fig8

app.layout = html.Div([
    html.H1("Wine Data Analysis", style={'textAlign': 'center'}),
    html.Div(
    
        style={
            'background-image': 'url(/assets/wine.png)',  
            'background-size': 'cover',
            'background-repeat': 'no-repeat',
            'background-attachment': 'fixed',
            'opacity': '0.5',  
            'position': 'absolute',
            'top': '0',
            'left': '0',
            'width': '100%',
            'height': '100%',
            'z-index': '-1'
        }
    ),

    dcc.Tabs(id="tabs", value='tab1', children=[
        dcc.Tab(label='Price vs Year', value='tab1'),
        dcc.Tab(label='Price vs Rating', value='tab2'),
        dcc.Tab(label='Rating vs Flavour', value='tab3'),
        dcc.Tab(label='Rating vs Alcohol Content', value='tab4'),
        dcc.Tab(label='Wine Food pairing analysis',value='tab5'),
        dcc.Tab(label='Distribution of Ratings',value='tab6'),
        dcc.Tab(label='Average Rating by Country', value= 'tab7'),
        dcc.Tab(label='Top 10 Wine Styles', value= 'tab8')  
    ]),

    html.Div(id='tabs-content'),
    html.Div(id='dynamic-content'),
])

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_tab_content(selected_tab):
    default_country = unique_countries[0]
    if selected_tab == 'tab1':
        fig1, _, _, _, _, _, _, _= create_charts('Bold',default_country) 
        insights = [
            {"Metric": "Mean Price", "Value": round(df['Price'].mean(), 2)},
            {"Metric": "Max Price", "Value": round(df['Price'].max(), 2)},
            {"Metric": "Min Price", "Value": round(df['Price'].min(), 2)},
        ]
        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Metric", "Value"]],
            data=insights,
             style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontSize': '14px',
    },
    style_header={
        'backgroundColor': 'lightgrey',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        ) 
        return dcc.Graph(figure=fig1),table
    elif selected_tab == 'tab2':
        _, fig2, _, _ , _, _, _, _= create_charts('Bold',default_country)  
        insights = [
            {"Metric": "Correlation (Price & Rating)", "Value": round(correlation_fig2, 2)}
        ]
        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Metric", "Value"]],
            data=insights,
            style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontSize': '14px',
    },
    style_header={
        'backgroundColor': 'lightgrey',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        )
        return dcc.Graph(figure=fig2),table
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
        _, _, _, fig4, _, _, _, _ = create_charts('Bold',default_country)
        insights = [
            {"Metric": "Correlation (Alcohol & Rating)", "Value": round(correlation_fig4, 2)}
        ]
        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Metric", "Value"]],
            data=insights,
            style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontSize': '14px',
    },
    style_header={
        'backgroundColor': 'lightgrey',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        )  
        return dcc.Graph(figure=fig4),table
    elif selected_tab == 'tab5':
        return html.Div([
            html.Label("Select Country:", style={'margin-top': '20px'}),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": country, "value": country} for country in unique_countries],
                value=default_country,  
            ),
            dcc.Graph(id="pie-chart")

        ])
    
        return dcc.Graph(id="pie-chart", figure=fig5), dropdown
    elif selected_tab == 'tab6':
        _, _, _, _, _, fig6, _, _ = create_charts('Bold',default_country)
        insights = [
            {"Metric": "Mean Rating", "Value": round(df['Rating'].mean(), 2)},
            {"Metric": "Most Common Rating", "Value": df['Rating'].mode()[0]}
        ]
        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Metric", "Value"]],
            data=insights,
            style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontSize': '14px',
    },
    style_header={
        'backgroundColor': 'lightgrey',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        )
        return dcc.Graph(figure=fig6),table
    elif selected_tab =='tab7':
        _, _, _, _, _, _, fig7, _ = create_charts('Bold',default_country)
        avg_rating_country = df.groupby('Country')['Rating'].mean().reset_index()
        top_country = avg_rating_country.loc[avg_rating_country['Rating'].idxmax(), 'Country']
        insights = [
            {"Metric": "Top Country", "Value": top_country},
            {"Metric": "Average Rating", "Value": round(avg_rating_country['Rating'].mean(), 2)}
        ]
        table = dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in ["Metric", "Value"]],
            data=insights,
            style_cell={
        'textAlign': 'left', 
        'padding': '10px',
        'fontSize': '14px',
    },
    style_header={
        'backgroundColor': 'lightgrey',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
        )  
        return dcc.Graph(figure=fig7),table
    elif selected_tab =='tab8':
        return html.Div([
            html.Label("Select the Country:", style={'margin-top': '20px'}),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label":country, "value": country} for country in unique_countries],
                value=unique_countries[0],
                clearable=False
            ),
            html.Div(id='tab8-content')
        ])
        

@app.callback(
    Output('tab3-content', 'children'),
    [Input('attribute-dropdown', 'value')]
)
def update_column_graph(selected_column):
    default_country = unique_countries[0]
    _, _, fig3, _, _, _, _, _ = create_charts(selected_column,default_country )
    return dcc.Graph(figure=fig3)  

@app.callback(
    Output('pie-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_pie_chart(selected_country):
    _, _, _, _, fig5, _, _, _= create_charts('Bold', selected_country)
    return fig5

@app.callback(
    Output('tab8-content', 'children'),
    [Input('country-dropdown', 'value')]
)
def update_bar_graph(selected_country):
    _, _, _, _, _, _, _, fig8 = create_charts('Bold', selected_country)
    return dcc.Graph(figure=fig8)  


if __name__ == '__main__':
    app.run_server(debug=True)
