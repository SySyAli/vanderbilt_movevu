from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Setting up Nashville's Bus Route as a Dictionary
WEGO_FREQUENT_SERVICE = {
    3: "West_End",
    5: "West_End/Bellevue",
    22: "Bordeaux",
    23: "Dickerson_Pike",
    50: "Charlotte_Pike",
    52: "Nolansville_Pike",
    55: "Murfreesboro_Pike",
    56: "Gallatin_Pike"
}

WEGO_LOCAL_SERVICE = {
    4: "Shelby",
    6: "Lebanon_Pike",
    7: "Hillsboro_Pike",
    8: "8th_Avenue_South",
    9: "MetroCenter",
    14: "Whites_Creek",
    17: "12th_Avenue_South",
    18: "Airport",
    19: "Herman",
    28: "Meridian",
    29: "Jefferson",
    34: "Opry Mills",
    41: "Golden Valley",
    42: "St._Cecilia/Cumberland"
}

WEGO_CONNECTOR_SERVICE = {
    25: "Midtown",
    70: "Bellevue",
    75: "Midtown",
    76: "Madison",
    77: "Thompson/Wedgewood",
    79: "Skyline"
}

WEGO_EXPRESS_SERVICE = {
    84: "Murfreesboro",
    86: "Smyrna/La_Vergne",
    87: "Gallatin/Hendersonville",
    88: "Dickson",
    89: "Springfield/Joelton",
    94: "Clarksville",
    95: "Spring_Hill/Franklin"
}

WEGO_TRAIN_SERVICE = {
    64: "Star_Downtown_Shuttle",
    93: "Star_West_End_Shuttle"
}

WEGO_ALL_ROUTES = {**WEGO_FREQUENT_SERVICE, **WEGO_LOCAL_SERVICE, **WEGO_CONNECTOR_SERVICE, **WEGO_EXPRESS_SERVICE, **WEGO_TRAIN_SERVICE}
list_WE_GO_ALL_ROUTES = list(WEGO_ALL_ROUTES.keys())
list_WE_GO_ALL_ROUTES.sort()
print("Listed Routes:", list_WE_GO_ALL_ROUTES)
print("Number of Routes:", len(list_WE_GO_ALL_ROUTES))

df = pd.read_parquet('movevu.parquet')
# Data cleaning and preparation steps
df['RIDE_DATE'] = pd.to_datetime(df['RIDE_DATE'])
df['MONTH_YEAR'] = df['RIDE_DATE'].dt.strftime('%Y-%m')
df['Hour'] = df['RIDE_DATE'].dt.hour

# print("Max Date MM-YY", df['MONTH_YEAR'].max())
# print(df['MONTH_YEAR'].unique())

# Calculate the total ridership for each route per month - Using MONTH and RIDE_DATE FROM ABOVE
# print(df.tail())
total_route_month_count = df.groupby(['ROUTE', 'MONTH_YEAR']).size().reset_index(name='COUNT')
# print("Max Date MM-YY TRMC:", total_route_month_count['MONTH_YEAR'].max())
# print(total_route_month_count['MONTH_YEAR'].unique())
# print(total_route_month_count.tail())

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Top 6 Routes'),

    # Dropdown or DatePickerRange for selecting the time period
    dcc.DatePickerRange(
        id='topsix-date-picker-range',
        min_date_allowed=df['MONTH_YEAR'].min(),
        max_date_allowed=df['MONTH_YEAR'].max(),
        start_date=df['MONTH_YEAR'].min(),
        end_date=df['MONTH_YEAR'].max(),
        display_format='YYYY-MM'
    ),
    # Graph for displaying the routes plot
    dcc.Graph(id='routes-plot'),
    html.H1("Swipes per Month"),
    dcc.DatePickerRange(
        id='swipes-date-picker-range',  # Changed ID to be unique
        start_date=df['MONTH_YEAR'].min(),
        end_date=df['MONTH_YEAR'].max(),
        display_format='YYYY-MM'
    ),
    dcc.Graph(id='monthly-rides-graph'), 
    
    html.H1("Ridership by Time of Day"),
    
    html.Div([
        html.Label("Select Date Range:"),
        dcc.DatePickerRange(
            id='timedayhr-date-picker-range',
            min_date_allowed=df['MONTH_YEAR'].min(),
            max_date_allowed=df['MONTH_YEAR'].max(),
            start_date=df['MONTH_YEAR'].min(),
            end_date=df['MONTH_YEAR'].max(),
            display_format='YYYY-MM'
        ),
    ]),
    
    dcc.Graph(id='ridership-time-graph'),

    html.H1("Unique Users per Month"),
    
    html.Div([
        html.Label("Select Date Range for Unique Users:"),
        dcc.DatePickerRange(
            id='unique-users-date-picker-range',
            start_date=df['MONTH_YEAR'].min(),
            end_date=df['MONTH_YEAR'].max(),
            display_format='YYYY-MM'
        ),
    ]),
    
    dcc.Graph(id='unique-users-graph'),
])

# TOP 6 ROUTES GRAPH
@app.callback(
    Output('routes-plot', 'figure'),
    [Input('topsix-date-picker-range', 'start_date'),
     Input('topsix-date-picker-range', 'end_date')]
)

def update_routes_plot(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    print("Start Date:", start_date, "End Date:", end_date)
    filtered_df = total_route_month_count[(total_route_month_count['MONTH_YEAR'] >= start_date) & (total_route_month_count['MONTH_YEAR'] <= end_date)]
    # Generate the plot using the filtered DataFrame
    fig = plot_all_routes_with_plotly(filtered_df)
    return fig

# SWIPES PER MONTH HISTOGRAM
@app.callback(
    Output('monthly-rides-graph', 'figure'),
    [Input('swipes-date-picker-range', 'start_date'),
     Input('swipes-date-picker-range', 'end_date')]
)

def update_graph(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    filtered_df = df[(df['MONTH_YEAR'] >= start_date) & (df['MONTH_YEAR'] <= end_date)]
    
    # Group by 'MONTH_YEAR' and count the number of rides, then reset the index to make 'RIDE_COUNT' a column
    ride_counts = filtered_df.groupby('MONTH_YEAR').size().reset_index(name='RIDE_COUNT')
    
    # Create a bar chart using Plotly Express
    fig = px.bar(ride_counts, x='MONTH_YEAR', y='RIDE_COUNT', 
                 title='Monthly Analysis of Rides',
                 labels={'MONTH_YEAR': 'Month', 'RIDE_COUNT': 'Number of Rides'})
    fig.update_xaxes(tickangle=-45)
    
    return fig

# HELPER FUNCTIONS
def plot_all_routes_with_plotly(route_month_counts):
    fig = go.Figure()
    # print("Max Date inside plot_all_routes_with_plotly:", route_month_counts['MONTH_YEAR'].max())
    # print(route_month_counts['MONTH_YEAR'].unique())
    route_ridership = route_month_counts.groupby('ROUTE')['COUNT'].sum().reset_index(name='RIDERSHIP')
    # Find the top 6 routes by total ridership
    top_6_routes = route_ridership.sort_values('RIDERSHIP', ascending=False).head(6)
    print("Top 6 Routes by Ridership from 2017 to Dec. 2023")
    print(top_6_routes)

    # Make a list of the top 6 routes
    top_6_routes_list = list(top_6_routes['ROUTE'])

    for route in route_month_counts['ROUTE'].unique():
        if route in top_6_routes_list:
            if int(route) in WEGO_ALL_ROUTES:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                                 mode='lines', name=route + ": " + WEGO_ALL_ROUTES[int(route)]))
            else:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                    mode='lines', name=str(route) + ": " + "Missing Route"))

    fig.update_layout(title='Monthly Analysis of Routes',
                      xaxis_title='Month',
                      yaxis_title='Number of Rides',
                      xaxis_tickangle=-45)
    return fig


#EMPLOYEE OR STUDENT GRAPH
@app.callback(
    Output('ridership-time-graph', 'figure'),
    [Input('timedayhr-date-picker-range', 'start_date'),
     Input('timedayhr-date-picker-range', 'end_date')]
)
def update_graph(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    filtered_df = df[(df['MONTH_YEAR'] >= start_date) & (df['MONTH_YEAR'] <= end_date)]
    
    # Aggregate rides by hour and status
    peak_usage = filtered_df.groupby(['Hour', 'EMPLOYEE_OR_STUDENT']).size().unstack(fill_value=0)

    # Create traces for each rider category
    data = []
    for column in peak_usage.columns:
        data.append(go.Scatter(x=peak_usage.index, y=peak_usage[column], mode='lines', name=column))
    
    # Create the figure
    fig = go.Figure(data=data)
    fig.update_layout(
        title="Peak Usage Times by Group",
        xaxis_title="Hour of the Day",
        yaxis_title="Number of Rides",
        hovermode="x"
    )
    
    return fig

# Unique Users per Month Graph Callback
# UNIQUE USERS GRAPH CALLBACK
@app.callback(
    Output('unique-users-graph', 'figure'),
    [Input('unique-users-date-picker-range', 'start_date'),
     Input('unique-users-date-picker-range', 'end_date')]
)
def update_unique_users_graph(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    filtered_df = df[(df['RIDE_DATE'] >= start_date) & (df['RIDE_DATE'] <= end_date)]

    # Process to get unique users per month
    unique_users_per_month = (
        filtered_df.drop_duplicates(subset=['CAMPUS_ID', 'MONTH_YEAR'])
        .groupby(['MONTH_YEAR'])
        .size()
        .reset_index(name='UNIQUE_USERS')
    )
    
    # Create the line plot
    fig = px.line(unique_users_per_month, x='MONTH_YEAR', y='UNIQUE_USERS',
                  title='Unique Users per Month',
                  labels={'MONTH_YEAR': 'Month', 'UNIQUE_USERS': 'Number of Unique Users'})
    fig.update_xaxes(tickangle=-45)
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)