from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# Setting up Nashville's Bus Route as a Dictionary
WEGO_FREQUENT_SERVICE = {
    3: "West_End - White Bridge",
    5: "West_End - Bellevue",
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
    70: "Bellevue",
    25: "Midtown",
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
# incorporate data
csv_files = ["./csv/MoveVU_2017_2020.csv", "./csv/MoveVU_2020_2022.csv", "./csv/MoveVU_2022_Oct2023.csv"]

df1 = pd.read_csv(
    csv_files[0],
    usecols=["ROUTE", "CARDOFFICE_CARD_NUMBER", "CARD_ID_STATUS", "RIDE_DATE", "BUS", "ROUTE", "RUN", "RT_AREA", "FIRST_NAME", "LAST_NAME", "EMPLOYEE_OR_STUDENT", "CAMPUS_ID"],
    dtype={
        "ROUTE": str,
        "CARDOFFICE_CARD_NUMBER": str,
        "CARD_ID_STATUS": str,
        "RIDE_DATE": str,  # You'll convert this to datetime later
        "BUS": str,
        "RUN": str,
        "RT_AREA": str,
        "FIRST_NAME": str,
        "LAST_NAME": str,
        "EMPLOYEE_OR_STUDENT": str,
        "CAMPUS_ID": str
    }
)

df2 = pd.read_csv(
    csv_files[1],
    usecols=["ROUTE", "CARDOFFICE_CARD_NUMBER", "CARD_ID_STATUS", "RIDE_DATE", "BUS", "ROUTE", "RUN", "RT_AREA", "FIRST_NAME", "LAST_NAME", "EMPLOYEE_OR_STUDENT", "CAMPUS_ID"],
    dtype={
        "ROUTE": str,
        "CARDOFFICE_CARD_NUMBER": str,
        "CARD_ID_STATUS": str,
        "RIDE_DATE": str,  # You'll convert this to datetime later
        "BUS": str,
        "RUN": str,
        "RT_AREA": str,
        "FIRST_NAME": str,
        "LAST_NAME": str,
        "EMPLOYEE_OR_STUDENT": str,
        "CAMPUS_ID": str
    }
)

df3 = pd.read_csv(
    csv_files[2],
    usecols=["ROUTE", "CARDOFFICE_CARD_NUMBER", "CARD_ID_STATUS", "RIDE_DATE", "BUS", "ROUTE", "RUN", "RT_AREA", "FIRST_NAME", "LAST_NAME", "EMPLOYEE_OR_STUDENT", "CAMPUS_ID"],
    dtype={
        "ROUTE": str,
        "CARDOFFICE_CARD_NUMBER": str,
        "CARD_ID_STATUS": str,
        "RIDE_DATE": str,  # You'll convert this to datetime later
        "BUS": str,
        "RUN": str,
        "RT_AREA": str,
        "FIRST_NAME": str,
        "LAST_NAME": str,
        "EMPLOYEE_OR_STUDENT": str,
        "CAMPUS_ID": str
    }
)

frames = [df1, df2, df3]
df = pd.concat(frames, ignore_index=True)

# Converting the "RIDE_DATE" columns to datetime objects
df['RIDE_DATE'] = pd.to_datetime(df['RIDE_DATE'])
# Extract month and year and create a new column
df['MONTH_YEAR'] = df['RIDE_DATE'].dt.strftime('%Y-%m')

bins = [0, 1, 5, 10, 20, 50, 100, 500, 1192]
labels = ['1 ride', '2-5 rides', '6-10 rides', '11-20 rides', '21-50 rides', '51-100 rides', '101-500 rides', '501-1192 rides']
# Calculate ride counts per route
columns_to_check = ['CAMPUS_ID', 'FIRST_NAME', 'LAST_NAME', 'EMPLOYEE_OR_STUDENT']
df_cleaned = df.dropna(subset=columns_to_check)
ride_counts_df = df_cleaned.groupby('ROUTE')['CARDOFFICE_CARD_NUMBER'].count().reset_index(name='RIDE_COUNT')


def plot_all_routes_with_plotly(route_month_counts):
    fig = go.Figure()

    route_ridership = route_month_counts.groupby('ROUTE')['COUNT'].sum().reset_index(name='RIDERSHIP')
    # Find the top 6 routes by total ridership
    top_6_routes = route_ridership.sort_values('RIDERSHIP', ascending=False).head(6)
    print("Top 6 Routes by Ridership from 2017 to Oct. 2023")
    print(top_6_routes)

    # Make a list of the top 6 routes
    top_6_routes_list = list(top_6_routes['ROUTE'])

    for route in route_month_counts['ROUTE'].unique():
        if route in top_6_routes_list:
            if int(route) in WEGO_ALL_ROUTES:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                                 mode='lines', name=str(route) + ": " + WEGO_ALL_ROUTES[int(route)]))
            else:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                    mode='lines', name=str(route) + ": " + "Missing Route"))

    fig.update_layout(title='Monthly Analysis of Routes',
                      xaxis_title='Month',
                      yaxis_title='Number of Rides',
                      xaxis_tickangle=-45)
    return fig

def create_ridership_histogram(ride_counts_df, value):
    # Ensure 'Category' column exists and create it if necessary
    print("ride counts columnns",ride_counts_df.columns)

    if 'Year' not in ride_counts_df.columns:
        ride_counts_df['Year'] = ride_counts_df['RIDE_DATE'].dt.year

    if 'RIDE_DATE' in ride_counts_df.columns:
        ride_counts_df['Year'] = ride_counts_df['RIDE_DATE'].dt.year
    else:
        print("RIDE_DATE column not found in the DataFrame")

    # Filter the DataFrame for the selected year
    filtered_df = ride_counts_df[ride_counts_df['Year'] == value]

    # Ensure 'Category' column exists and create it if necessary
    if 'Category' not in filtered_df.columns:
        filtered_df['Category'] = pd.cut(filtered_df['RIDE_COUNT'], bins=bins, labels=labels, include_lowest=True)

    # Drop NaN values to avoid plotting issues
    filtered_df.dropna(subset=['Category', 'RIDE_COUNT'], inplace=True)

    # Group by 'Category' and count occurrences
    category_counts = filtered_df.groupby('Category').size().reset_index(name='Counts')

    # Create the histogram using Plotly Express
    fig = px.bar(category_counts, x='Category', y='Counts', title=f'Ridership Categories Histogram for {value}')

    return fig
# Calculate the total ridership for each route per month - Using MONTH and RIDE_DATE FROM ABOVE
total_route_month_count = df.groupby(['ROUTE', 'MONTH_YEAR']).size().reset_index(name='COUNT')

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Top 6 Routes'),
    dcc.DatePickerRange(
        id='start-date-picker-range',  # Changed ID to be unique
        start_date=total_route_month_count['MONTH_YEAR'].min(),
        end_date=total_route_month_count['MONTH_YEAR'].max(),
        display_format='YYYY-MM'
    ),
    dcc.Graph(id='routes-plot'),
    html.H1("Swipes per Month"),
    dcc.DatePickerRange(
        id='end-date-picker-range',  # Changed ID to be unique
        start_date=df['MONTH_YEAR'].min(),
        end_date=df['MONTH_YEAR'].max(),
        display_format='YYYY-MM'
    ),
    dcc.Graph(id='monthly-rides-graph'), 
    html.H1("Ridership Bucketing"),
    dcc.Dropdown(
    id='year-dropdown',
    options=[{'label': year, 'value': year} for year in range(2017, 2023)],
    value=2022  # Default value 
    ),
    dcc.Graph(id='ridership-histogram'),
])

@app.callback(
    Output('routes-plot', 'figure'),
    [Input('start-date-picker-range', 'start_date'),
     Input('start-date-picker-range', 'end_date')]
)
def update_routes_plot(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    filtered_df = total_route_month_count[(total_route_month_count['MONTH_YEAR'] >= start_date) & (total_route_month_count['MONTH_YEAR'] <= end_date)]

    # Generate the plot using the filtered DataFrame
    fig = plot_all_routes_with_plotly(filtered_df)
    return fig

# Callback to update the graph based on selected date range
@app.callback(
    Output('monthly-rides-graph', 'figure'),
    [Input('end-date-picker-range', 'start_date'),
     Input('end-date-picker-range', 'end_date')]
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

@app.callback(
    Output('ridership-histogram', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_histogram(value):
    fig = create_ridership_histogram(ride_counts_df, value)
    return fig

if __name__ == '__main__':
    app.run(debug=True)