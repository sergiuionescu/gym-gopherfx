import dash
import dash_core_components as dcc
import colorlover as cl
import dash_html_components as html
import pandas as pd
import os

currency = 'USDJPY'
date = '20180401'

colorscale = cl.scales['9']['qual']['Paired']
app = dash.Dash()
base_path = os.path.join(os.path.dirname(__file__), 'gym_gopherfx/envs/data/')


def get_daily_graph(graph_currency, graph_date):
    figure = get_daily_figure(graph_currency, graph_date)
    reference_graph = dcc.Graph(
        id='day-evolution',
        figure=figure
    )

    return reference_graph


def get_daily_figure(graph_currency, graph_date):
    file_name = graph_currency + graph_date + '.csv'
    rates = pd.read_csv(os.path.join(base_path, 'rates/' + file_name), names=['date', 'rate'])
    potential = pd.read_csv(os.path.join(base_path, 'potential/' + file_name),
                            names=['start_date', 'end_date', 'profit', 'start_rate', 'end_rate', 'wait'])
    figure_data = [{'x': rates['date'], 'y': rates['rate'], 'type': 'line', 'name': 'Rate'}] + \
                  [{
                      'x': potential['start_date'],
                      'open': potential['start_rate'],
                      'high': potential['end_rate'],
                      'low': potential['start_rate'],
                      'close': potential['end_rate'],
                      'type': 'candlestick',
                      'increasing': {'line': {'color': colorscale[0]}},
                      'decreasing': {'line': {'color': colorscale[8]}},
                      'name': 'Potential'
                  }]
    performance_file_name = os.path.join(os.path.dirname(__file__), 'performance/' + file_name)
    if os.path.isfile(performance_file_name):
        performance = pd.read_csv(performance_file_name,
                                  names=['start_date', 'end_date', 'profit', 'start_rate', 'end_rate', 'wait'])
        figure_data += [{
            'x': performance['start_date'],
            'open': performance['start_rate'],
            'high': performance['end_rate'],
            'low': performance['start_rate'],
            'close': performance['end_rate'],
            'type': 'candlestick',
            'increasing': {'line': {'color': colorscale[1]}},
            'decreasing': {'line': {'color': colorscale[4]}},
            'name': 'Performance'
        }]
    figure = {'data': figure_data, 'layout': {'title': graph_currency + ' ' + graph_date}}
    return figure


default_graph = get_daily_graph(currency, date)


def get_monthly_graph():
    total_frames = []
    for totals_file in os.listdir(os.path.join(base_path, 'potential/')):
        if 'total' in totals_file:
            frame = pd.read_csv(os.path.join(base_path, 'potential/' + totals_file),
                                names=['date', 'total_profit', 'total_loss', 'rolls'])
            total_frames.append(frame)

    totals = pd.concat(total_frames)

    return dcc.Graph(
        id='month-evolution',
        figure={
            'data':
                [{'x': totals['date'], 'y': totals['total_profit'], 'type': 'line', 'name': 'Profit',
                  'mode': 'markers',
                  'marker': {
                      'size': 10,
                  }}],
            'layout': {
                'title': "Monthly potential " + str(totals['total_profit'].sum()) + " " + str(
                    totals['total_loss'].sum())
            }
        }
    )


app.layout = html.Div(children=[
    html.Div([html.H4("Demo of a random agent interacting with the gopherfx environment.")]),
    html.Div(id='graph-container', children=[
        get_daily_graph(currency, date),
        get_monthly_graph(),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000,
            n_intervals=0
        )
    ])
])


@app.callback(
    dash.dependencies.Output('day-evolution', 'figure'),
    [dash.dependencies.Input('month-evolution', 'clickData'),
     dash.dependencies.Input('interval-component', 'n_intervals')])
def update_output(value, n_intervals):
    global date
    if value:
        date = pd.to_datetime(value['points'][0]['x']).strftime('%Y%m%d')

    return get_daily_figure(currency, date)


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
