import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("MLVizDash: Interactive Machine Learning Visualizer"),
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Dataset'),
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(id='data-visualization')
])

# Callback to handle the uploaded data
@app.callback(
    Output('output-data-upload', 'children'),
    Output('data-visualization', 'figure'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return "Please upload a dataset.", {}

    # Parse the uploaded file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Display basic stats
    stats = df.describe().to_string()
    children = [
        html.H5("Dataset Statistics:"),
        html.Pre(stats)
    ]

    # Simple data visualization (histogram of the first numerical column)
    numerical_columns = df.select_dtypes(include='number').columns
    if len(numerical_columns) == 0:
        return "No numerical data found in the dataset.", {}

    fig = px.histogram(df, x=numerical_columns[0], title=f'Histogram of {numerical_columns[0]}')
    return children, fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)