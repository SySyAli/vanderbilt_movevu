from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Setting up Nashville's Bus Route as a Dictionary
WEGO_FREQUENT_SERVICE = {
    3: "West_End",
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

def plot_all_routes_with_plotly(route_month_counts):
    fig = go.Figure()

    route_ridership = route_month_counts.groupby('ROUTE')['COUNT'].sum().reset_index(name='RIDERSHIP')
    # Find the top 6 routes by total ridership
    top_6_routes = route_ridership.sort_values('RIDERSHIP', ascending=False).head(6)
    print("Top 6 Routes by Ridership from 2017 to Oct. 2023")
    print(top_6_routes)

    # Make a list of the top 6 routes
    top_6_routes_list = list(top_6_routes['ROUTE'])

    # for route in route_month_counts['ROUTE'].unique():
    #     route_data = route_month_counts[route_month_counts['ROUTE'] == route]
    #     fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
    #                              mode='lines', name=str(route) + ": " + WEGO_ALL_ROUTES.get(route, "Missing Route")))

    for route in route_month_counts['ROUTE'].unique():
        if route in top_6_routes_list:
            if route in WEGO_ALL_ROUTES:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                                 mode='lines', name=str(route) + ": " + WEGO_ALL_ROUTES[route]))
            else:
                route_data = route_month_counts[route_month_counts['ROUTE'] == route]
                fig.add_trace(go.Scatter(x=route_data['MONTH_YEAR'], y=route_data['COUNT'],
                    mode='lines', name=str(route) + ": " + "Missing Route"))

    fig.update_layout(title='Monthly Analysis of Routes',
                      xaxis_title='Month',
                      yaxis_title='Number of Rides',
                      xaxis_tickangle=-45)
    return fig


# Calculate the total ridership for each route per month - Using MONTH and RIDE_DATE FROM ABOVE
total_route_month_count = df.groupby(['ROUTE', 'MONTH_YEAR']).size().reset_index(name='COUNT')



app = Dash(__name__)

app.layout = html.Div([
    html.H1('Top 6 Routes'),

    # Dropdown or DatePickerRange for selecting the time period
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=total_route_month_count['MONTH_YEAR'].min(),
        end_date=total_route_month_count['MONTH_YEAR'].max(),
        display_format='YYYY-MM'
    ),

    # Graph for displaying the routes plot
    dcc.Graph(id='routes-plot'),

    # Add more components as needed
])


@app.callback(
    Output('routes-plot', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_routes_plot(start_date, end_date):
    # Filter the DataFrame based on the selected dates
    filtered_df = total_route_month_count[(total_route_month_count['MONTH_YEAR'] >= start_date) & (total_route_month_count['MONTH_YEAR'] <= end_date)]

    # Generate the plot using the filtered DataFrame
    fig = plot_all_routes_with_plotly(filtered_df)
    return fig

if __name__ == '__main__':
    app.run(debug=True)