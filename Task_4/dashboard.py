import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True) 

df = pd.read_csv("Updated_wine.csv")

df['Country'] = df['Country'].str.strip().str.title()
food_columns = df.loc[:, 'Lamb':'Aperitif'].columns
unique_countries = df['Country'].unique()
columns_to_plot = ['Bold', 'Tannin', 'Sweet', 'Acidic']
unique_countries = df['Country'].unique()

correlation_fig2 = np.corrcoef(df['Price'], df['Rating'])[0, 1]
correlation_fig4 = np.corrcoef(df['Alcohol content'], df['Rating'])[0, 1]

def create_charts(selected_column,selected_country):
    avg_price_by_year = df.groupby('Year')['Price'].mean().reset_index()
    avg_rating_by_flavour = df.groupby('Rating', as_index=False)[selected_column].mean()
    avg_rating_by_alcohol = df.groupby('Alcohol content')['Rating'].mean().reset_index()
    avg_rating_by_country = df.groupby('Country')['Rating'].mean().reset_index()
    avg_rating_by_country.columns = [col.strip() for col in avg_rating_by_country.columns]
    filtered_df = df[df['Country'] == selected_country]
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
    
    fig7 = px.bar(
        avg_rating_by_country,
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
    html.H1("Wine Data Analysis", style={'textAlign': 'center', 'color':'white'}),
    html.Div(
        id='background-image',
    ),

    dcc.Tabs(id="tab-container", value='tab1', children=[
        dcc.Tab(label='Price vs Year', value='tab1', className='tab'),
        dcc.Tab(label='Price vs Rating', value='tab2', className='tab'),
        dcc.Tab(label='Rating vs Flavour', value='tab3', className='tab'),
        dcc.Tab(label='Rating vs Alcohol Content', value='tab4', className='tab'),
        dcc.Tab(label='Wine Food pairing analysis',value='tab5', className='tab'),
        dcc.Tab(label='Distribution of Ratings',value='tab6', className='tab'),
        dcc.Tab(label='Average Rating by Country', value= 'tab7', className='tab'),
        dcc.Tab(label='Top 10 Wine Styles', value= 'tab8', className='tab')  
    ]),

    html.Div(id='tabs-content'),
    html.Div(id='dynamic-content'),
])

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tab-container', 'value')]
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

        description = html.P(children=
    [
        "Interpretation for Average Wine Price vs Manufacture Year",
        html.Br(),
        "Type of Chart: Trends over time.",
        html.Br(),
        "Purpose: The chart illustrates the variation in average price due to the manufacture year.",
        html.Br(),
        "Timeframe: This chart shows data from 1988 to 2022.",
        html.Br(),
        "Description: According to the time series chart:",
        html.Br(),
        "• From 1988 to 1993, prices increased steadily.",
        html.Br(),
        "• From 1993 to 2003, we see that average prices were still increasing each year.",
        html.Br(),
        "• From 2003 to 2022, prices decreased over time.",
        html.Br(),
        "• Highest price: The highest price of a bottle was in 2003, and its price was $55.97.",
        html.Br(),
        "• Lowest price: The lowest price of a bottle was in 2022, and its price was $19.99.",
        html.Br(),
        "• nv - Non vintage, these wine bottles don't show a manufactured year.",
    ],
    className="description-text"
)

        return html.Div([dcc.Graph(figure=fig1),table,description])
    
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

        description = html.P(children=
            [

            "Interpretation of Average Price vs Ratings",
            html.Br(),
            "Type of Chart: Scatter Plot.",
            html.Br(),
            "Purpose: The chart displays the relationship between wine ratings and their prices.",
            html.Br(),
            "Description:",
            html.Br(),
	            "•	According to the scatter plot, there is a moderate positive linear correlation. This means that, in general, as the price of wine increases, the wine rating also increases.",
                html.Br(),
	            "•	Most wine prices are below average, with the majority of ratings close to 4.",
                html.Br(),
	            "•	There are some outliers in the plot, but in general, higher wine prices tend to have higher ratings, though the variation is significant.",
            ],
                className="description-text"
        )
        
        return html.Div([dcc.Graph(figure=fig2),table,description])
    
    elif selected_tab == 'tab3':
         return html.Div([
        html.Div(className='dropdown-container', children=[
            html.Label("Select Attribute : ", className='dropdown-text'),
            dcc.Dropdown(
                id="attribute-dropdown",
                options=[{"label": col, "value": col} for col in columns_to_plot],
                value=columns_to_plot[0],  
                clearable=False,
                className='dropdown-menu'
            )
        ]),
        html.Div(id='tab3-content'),

        html.P(children=
            [
                "Interpretation for Average Wine Rating by the Flavour",
                html.Br(),
                "For Example - Boldness",
                html.Br(),
                "Type of Chart: Bar Chart",
                html.Br(),
                "Purpose: The chart shows how the average wine rating varies according to the boldness of the wine.",
                html.Br(),
                "Description:",
                html.Br(),
                "• In this bar chart, wines with a boldness level of 3.7 have the highest average rating of 81.83.",
                html.Br(),
                "• Wines with a boldness level of 4.2 have the lowest average rating, which is 53.64767."
            ],
            className="description-text"
        )
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

        description = html.P(children=
            [

            "Interpretation for Average Variation of Rating Corresponding to Alcohol Content",
            html.Br(),
            "Type of Chart: Scatter Plot",
            html.Br(),
            "Purpose:",
            html.Br(),
            "The chart represents the variation in wine ratings corresponding to alcohol content.",
            html.Br(),
            "Description:",
            html.Br(),
	            "•	Based on the scatter plot, there is a weak positive linear correlation.",
                html.Br(),
	            "•	This means that alcohol content does not appear to significantly influence the ratings.",
                html.Br(),
	            "•	Most wines are rated between 3.8 and 4.2, regardless of their alcohol content.",
                html.Br(),
	            "•	The alcohol content of the wines ranges from 4% to approximately 20%.",
            ],

                className="description-text"
        )

        return html.Div([dcc.Graph(figure=fig4),table,description])
    
    elif selected_tab == 'tab5':
        return html.Div([
            html.Div(className='dropdown-container', children=[
                html.Label("Select Country : ", className='dropdown-text'),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": country, "value": country} for country in unique_countries],
                    value=default_country, 
                    clearable=False,
                    className='dropdown-menu' 
                )
            
            ]),
            dcc.Graph(id="pie-chart"),

            html.P(children=
                [

                "The pie chart titled ""Most Common Food Pairings in Australia"" depicts the distribution of various food types paired with meals in Australia. Here's a detailed breakdown of the chart:",
                html.Br(),
                    "• Beef (21.4%): The largest segment of the chart shows that beef is the most common food pairing in Australia, making up 21.4% of the total food pairings.",
                    html.Br(),
                    "• Poultry (21.3%): Following closely behind, poultry constitutes 21.3% of the food pairings, indicating its popularity in Australian cuisine.",
                    html.Br(),
                    "• Lamb (21.1%): Lamb is another major component, accounting for 21.1% of the food pairings, highlighting its significance in Australian diets. etc...",
                    html.Br(),
                ],

                    className="description-text"
            )
        ])
    
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

        description = html.P(children=
            [

            "The chart reveals that the most common ratings, 3.8 and 3.9, each received just over 1000 votes, indicating that these ratings are reliable due to the high number of votes. As the rating increases beyond 4.0, the count of votes decreases, suggesting fewer products achieve higher average ratings. ",
            html.Br(),
            "This distribution implies that while a good number of products are rated favorably, achieving higher ratings (above 4.3) is less common and likely reflects higher consumer satisfaction levels but fewer products meeting that threshold.",
            html.Br(),
            "Conversely, lower ratings (3.7) are rare, indicating that most products are at least satisfactory to the voters."
            "Therefore, the high number of votes for ratings 3.8 and 3.9 suggests these ratings are the most reliable, representing a significant portion of voter opinions. Products with these average ratings can be considered dependably reviewed by a larger audience, giving a more accurate representation of their quality.",
            ],

                className="description-text"
        )

        return html.Div([dcc.Graph(figure=fig6),table,description])
    
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

        description = html.P(children=
            [

            "Interpretation for Average Rating by Country",
            html.Br(),
                "Type of Chart: Horizontal Bar Chart",
                html.Br(),
                "Purpose:",
                html.Br(),
                "The chart reflects the variation in average wine ratings across different countries.",
                html.Br(),
                "Description:",
                html.Br(),
	                "•	According to the horizontal bar chart, most countries have an average rating close to 4, indicating consistently high-quality wines across these regions.",
                    html.Br(),
	                "•	Countries like Valtellina and Valpolicella Ripasso Classico appear to have slightly higher average ratings compared to others.",
                    html.Br(),
            ],

                className="description-text"
        ) 

        return html.Div([dcc.Graph(figure=fig7),table,description])
    
    elif selected_tab =='tab8':
        return html.Div([

            html.Div(className='dropdown-container', children=[
                html.Label("Select the Country : ", className='dropdown-text'),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": country, "value": country} for country in unique_countries],
                    value=unique_countries[0],
                    clearable=False,
                    className='dropdown-menu' 
                )
            ]),
            html.Div(id='tab8-content'),

            html.P(children=
                [

                "Interpretation for Top 10 Wine Styles",
                html.Br(),
                "Type of Chart: Vertical Bar Chart",
                html.Br(),
                "Purpose:",
                html.Br(),
                "To identify and compare the popularity of the top 10 wine styles based on their frequency.",
                html.Br(),
                "Description:",
                html.Br(),
	                "•	According to the vertical bar chart, Tuscan Red is the most popular wine style with the highest count.",
                    html.Br(),
	                "•	Australian Shiraz, Southern Italy Red, and Northern Italy Red are also highly preferred.",
                    html.Br(),
                ],
                    className="description-text"
            )
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
