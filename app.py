import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px


df_month = pd.read_csv('./monthly_temp.csv')
df_week = pd.read_csv('./weekly_temp.csv')

df_month['date'] = pd.to_datetime(df_month['date'], format='%m-%Y')
df_month = df_month.sort_values(by='date')

df_2023 = df_month[df_month['year'] == 2023]
df_2023_week = df_week[df_week['year'] == 2023]

df_station = df_2023[df_2023['city'] == 'Berlin']
df_station = df_station.sort_values(by='date')


############## bar_graph
fig_eu = px.bar(df_2023[df_2023['country'].isin(['Germany', 'Spain', 'Italy', 'Estonia', 'Portugal'])], 
             y='avg_temp_monthly', 
             x='date',  
             color='city',
             barmode='group',
             title='Monthly Average Temperatures by European Cities',
             labels={'avg_temp_monthly': 'Average Temperature (°C)', 'date': 'Month'},
             orientation= 'v',
             height=400)

fig_eu.update_yaxes(range=[-10, 40])

bar_graph = dcc.Graph(figure=fig_eu)

############## line_graph
fig = px.line(df_2023, 
              x='month-year', 
              y='max_temp_monthly', 
              color='city',
              title='Monthly Average Temperatures',
             labels={'avg_temp_monthly': 'Average Temperature (°C)', 'date': 'Month'},
              height=600, 
              #range_x=[min_date, max_date],  # ajuste del rango x
              range_y=[0,50])

line_graph = dcc.Graph(figure=fig)

############## scatter_map
fig_scatter = px.scatter_mapbox(
    df_2023, 
    lat='lat', 
    lon='lon', 
    color="avg_humidity_monthly",
    size="max_temp_monthly",
    hover_data={
        "city": True,
        "max_temp_monthly": True,
        "min_temp_monthly": True,
        "avg_temp_monthly": True
    },
    animation_frame="date",
    color_continuous_scale=px.colors.sequential.Blues,
    title="Humidity & Temperature",
    mapbox_style="carto-positron",
    labels={'avg_humidity_monthly': 'Average Humidity (%)', 'avg_temp_monthly': 'Avg Temp', 'max_temp_monthly': 'Max Temp', 'min_temp_monthly': 'Min Temp'},
    zoom=1.5,
    center={"lat": 10, "lon": -30},  # Coordenadas centradas entre Sudamérica y Europa
    width=1000,
    height=600    
)

scatter_map = dcc.Graph(figure= fig_scatter)

############## stripes week
stripes_fig_week = px.bar(df_station, 
             x='date', 
             y='avg_temp_week', 
             color='avg_temp_week',
             color_continuous_scale='RdBu_r',
             title="Warming Stripes for Berlin",
             labels={'avg_temp_week': 'Average Temperature'},
             orientation='v',
             height=400, 
             width=1000)
stripes_graph_week= dcc.Graph(figure= stripes_fig_week)

############## stripes month
stripes_fig = px.bar(df_station, 
             x='date', 
             y='avg_temp_monthly', 
             color='avg_temp_monthly',
             color_continuous_scale='RdBu_r',
             title="Warming Stripes for Berlin",
             labels={'avg_temp_monthly': 'Average Temperature'},
             orientation='v',
             height=400, 
             width=1000)
stripes_graph = dcc.Graph(figure= stripes_fig)

########## DASH APP ########
pp = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])

# Dropdown for table
dropdown_table_city = dcc.Dropdown(
    id='dropdown_table_city',
    options=[{'label': city, 'value': city} for city in df_month['city'].unique()],
    value='Berlin',
    style={'backgroundColor': "#E9ECEF", "color": "#212529"}
)

# Dropdown multiple for line_graph
dropdown_line_graph_city = dcc.Dropdown(
    id='dropdown_line_graph_city',
    options=[{'label': city, 'value': city} for city in df_month['city'].unique()],
    value=['Berlin'],
    multi=True,
    style={'backgroundColor': "#E9ECEF", "color": "#212529"}
)

# RadioItems for line_graph
radio_items = dcc.RadioItems(
    id='radio_items',
    options=[
        {'label': 'Avg Temperature', 'value': 'avg_temp_monthly'}, 
        {'label': 'Max Temperature', 'value': 'max_temp_monthly'},
        {'label': 'Min Temperature', 'value': 'min_temp_monthly'}
    ],
    value='avg_temp_monthly',
    style={"color": "#212529"}
)

# Table
table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_month.columns],
    data=df_month.to_dict('records'),
    style_cell={'backgroundColor': 'black', 'color': 'white', 'border': '1px solid grey'},
    style_header={'fontWeight': 'bold', 'backgroundColor': 'grey'}
)

# Layout
app.layout = html.Div([
    html.H1('From Europe to South America: Best Cities to Work Remotely', style={'textAlign': 'center', 'color': '#0d47a1'}), 
    
    html.Div([
        html.H3('European Cities', style={'color': '#343A40'}),
        dcc.Markdown('''
            - **Berlin**: A hub for startups, rich in culture and history, with an affordable cost of living.
            - **Lisbon**: A coastal city with a mild climate, renowned for its welcoming community and growing tech scene.
            - **Barcelona**: Combines beach living with a vibrant city atmosphere, and a robust tech presence.
            - **Tallinn**: Known for its digital innovation, e-residency program, and picturesque old town.
            - **Rome**: Rich historical landmarks with a pleasant Mediterranean climate, and increasing tech opportunities.
        ''', style={'color': '#343A40'}),
        
        html.H3('South American Cities', style={'color': '#343A40'}),
        dcc.Markdown('''
            - **Medellin**: Known as the "City of Eternal Spring" for its climate, it's also an emerging tech hub in Latin America.
            - **Buenos Aires**: A blend of European and Latin American cultures, with bustling nightlife and a growing tech ecosystem.
            - **Lima**: Coastal location, rich culinary scene, and expanding opportunities for remote workers.
            - **Florianopolis**: A beautiful island city with beaches, great quality of life, and a budding tech community.
        ''', style={'color': '#343A40'}),
    
    
    ]),


    # line_graph
    html.Div([
        html.Label("Select cities:", style={"color": "#343A40"}),
        dropdown_line_graph_city,
        html.Label("Select temperature metric:", style={"color": "#343A40"}),
        radio_items,
        dcc.Graph(id="line_graph", figure=fig)
    ]),

    # Table
    html.Div([
        html.Label("Select a city for the table:", style={"color": "#343A40"}),
        dropdown_table_city,
        table
    ]),

    # scatter_map
    dcc.Graph(id="scatter_map", figure=fig_scatter),

    # bar_graph
    dcc.Graph(id="bar_graph", figure=fig_eu),

    #stripes_graph week
    dcc.Graph(id="stripes_graph_week",figure= stripes_fig_week),

    #stripes_graph
    dcc.Graph(id="stripes_graph",figure= stripes_fig)
])

# Callbacks
@app.callback(
    Output("table", "data"),
    [Input("dropdown_table_city", "value")]
)
def update_table(selected_city):
    filtered_df = df_month[df_month['city'] == selected_city]
    return filtered_df.to_dict('records')

@app.callback(
    Output("line_graph", "figure"),
    [Input("radio_items", "value"),
     Input("dropdown_line_graph_city", "value")]
)
def update_line_chart(temp_metric, cities):
    filtered_df = df_month[df_month['city'].isin(cities)]
    fig_updated = px.line(filtered_df, 
                          x='month-year', 
                          y=temp_metric, 
                          color='city',
                          title=f'Monthly {temp_metric.replace("_", " ").title()}',
                          height=600, 
                          range_y=[-20, 50])
    return fig_updated

if __name__ == "__main__":
    app.run_server(debug=True)