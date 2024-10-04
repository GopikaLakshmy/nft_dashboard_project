import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample data (replace this with your real-time data source)
data = {
    "Date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "Sales_USD": [100000 + i * 1000 for i in range(30)],
    "Average_Price": [500 + i * 10 for i in range(30)],
    "Volume_USD": [500000 + i * 2000 for i in range(30)],
    "Active_Wallets": [1500 + i * 5 for i in range(30)],
}
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1("NFT Market Trends Dashboard", style={"textAlign": "center"}),

        # Dropdown for selecting different metrics
        html.Div([
            html.Label("Select Metric"),
            dcc.Dropdown(
                id="metric_dropdown",
                options=[
                    {"label": "Sales (USD)", "value": "Sales_USD"},
                    {"label": "Average Price (USD)", "value": "Average_Price"},
                    {"label": "Volume (USD)", "value": "Volume_USD"},
                    {"label": "Active Wallets", "value": "Active_Wallets"},
                ],
                value="Sales_USD",  # Default value
                clearable=False,
                style={"width": "50%"},
            ),
        ], style={"textAlign": "center"}),

        # Graph for visualizing the selected metric
        dcc.Graph(id="line_chart"),

        # Second graph showing a comparison between sales and average price
        dcc.Graph(id="comparison_chart"),
    ]
)

# Callback to update the line chart based on the selected metric
@app.callback(
    Output("line_chart", "figure"),
    [Input("metric_dropdown", "value")]
)
def update_graph(selected_metric):
    fig = px.line(
        df,
        x="Date",
        y=selected_metric,
        title=f"{selected_metric} over Time",
        labels={"Date": "Date", selected_metric: selected_metric}
    )
    return fig

# Callback to show comparison between Sales and Average Price
@app.callback(
    Output("comparison_chart", "figure"),
    [Input("metric_dropdown", "value")]
)
def update_comparison_chart(selected_metric):
    fig = px.scatter(
        df,
        x="Sales_USD",
        y="Average_Price",
        title="Sales vs Average Price",
        labels={"Sales_USD": "Sales (USD)", "Average_Price": "Average Price (USD)"}
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
