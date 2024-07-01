import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv'
data = pd.read_csv(url)
data.columns = ['date', 'passengers']

# Get year and month columns
data['date'] = pd.to_datetime(data['date'])
data['year'] = data['date'].dt.year
data['month'] = data['date'].dt.month
data_1949= data[data["year"]==1949] #create one year dataframe
passengers_per_year = data.groupby('year')['passengers'].sum().reset_index()

#visualisation

fig1=px.line(data_1949, x='month', y='passengers', title='1949 Airline Passengers Over Time')
fig2 = px.bar(passengers_per_year, x='year', y='passengers',  range_y=[0, 8000])


#creating dcc components
graph1 = dcc.Graph(figure=fig1)
graph2 = dcc.Graph(figure=fig2) 


# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Airline Passengers Data"),

    html.Div([
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in data['year'].unique()],
            value=data['year'].min(),
            style={'width': '200px'}
        ),
        dcc.Graph(id='passengers-graph'),
    ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '20px'}),

    html.Div([
        dcc.Graph(figure=fig1),
        dcc.Graph(figure=fig2),
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px'})
])

# Callback to update main graph based on selected year
@app.callback(
    Output('passengers-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_figure(selected_year):
    filtered_data = data[data['year'] == selected_year]
    fig = px.line(filtered_data, x='month', y='passengers', title=f'Monthly Airline Passengers for {selected_year}',
                  labels={'month': 'Month', 'passengers': 'Number of Passengers'})
    fig.update_layout(
        yaxis=dict(range=[data['passengers'].min(), data['passengers'].max()])  # Fixed y-axis range
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)