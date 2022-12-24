import dash
from dash import dcc
from dash import html
import pandas as pd

# Load the census data into a Pandas DataFrame
df = pd.read_csv('https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/national/totals/nst-est2019-alldata.csv')

# Select the columns to display
df = df[['NAME', 'POPESTIMATE2019']]

# Create the Dash app
app = dash.Dash()

# Set up the layout of the app
app.layout = html.Div(children=[
    # Add a title
    html.H1(children='US Census Statistics'),

    # Add a dropdown to select the state
    dcc.Dropdown(
        id='state-select',
        options=[{'label': name, 'value': name} for name in df['NAME'].unique()],
        value='California'
    ),

    # Add a bar chart to display the population of the selected state
    dcc.Graph(
        id='population-chart',
        figure={
            'data': [{
                'x': df[df['NAME'] == 'California']['NAME'],
                'y': df[df['NAME'] == 'California']['POPESTIMATE2019'],
                'type': 'bar'
            }]
        }
    )
])

# Set up a callback to update the chart when the state is changed
@app.callback(
    dash.dependencies.Output('population-chart', 'figure'),
    [dash.dependencies.Input('state-select', 'value')]
)
def update_chart(selected_state):
    # Filter the DataFrame by the selected state
    filtered_df = df[df['NAME'] == selected_state]

    # Return the chart data for the selected state
    return {
        'data': [{
            'x': filtered_df['NAME'],
            'y': filtered_df['POPESTIMATE2019'],
            'type': 'bar'
        }]
    }

# Run the app
if __name__ == '__main__':
    app.run_server()
