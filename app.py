import dash
import dash_core_components as dcc
import colorlover as cl
import dash_html_components as html
import pandas as pd
import os
import numpy as np
import shutil
import datetime
import dateutil

currency = 'EUR_USD'
date = '20180601'
month = date[:6]

colorscale = cl.scales['9']['qual']['Paired']
app = dash.Dash()
base_path = os.path.join(os.path.dirname(__file__), 'data/')


def get_daily_graph(graph_currency, graph_date):
    figure = get_daily_figure(graph_currency, graph_date)
    reference_graph = dcc.Graph(
        id='day-evolution',
        figure=figure
    )

    return reference_graph


def get_daily_figure(graph_currency, graph_date):
    file_name = graph_date + '.csv'
    rates = pd.read_json('data/candlerates/EUR_USD/2018-06/' + graph_date + '.json')
    rate_values = pd.Series()
    for index in rates.index:
        rate_values = rate_values.append(pd.Series([rates['ask'][index]['c']], [index]))
    rates = rates.assign(ask_close=rate_values)

    figure_data = [{'x': rates['time'], 'y': rates['ask_close'], 'type': 'line', 'name': 'Rate'}]

    reference_file = os.path.join(base_path, 'potential/' + file_name)
    figure_data, total_reference = add_evolution_figure(figure_data, reference_file,
                                                        "Reference",
                                                        colorscale[0], colorscale[8])
    performance_file = os.path.join(base_path, 'performance/' + file_name)
    figure_data, total_performance = add_evolution_figure(figure_data, performance_file,
                                                          "Performance", colorscale[1], colorscale[4])
    figure = {'data': figure_data,
              'layout': {'title': graph_currency + ' ' + graph_date}}
    return figure


def add_evolution_figure(figure_data, file_path, label, color_increasing, color_decreasing):
    total = 0
    if os.path.isfile(file_path):
        data = pd.read_csv(file_path,
                           names=['start_date', 'end_date', 'profit', 'start_rate', 'end_rate', 'wait', 'type',
                                  'budget'])
        total = np.round(data['profit'].sum())
        figure_data += [{
            'x': data['start_date'],
            'open': data['start_rate'],
            'high': data['end_rate'],
            'low': data['start_rate'],
            'close': data['end_rate'],
            'type': 'candlestick',
            'increasing': {'line': {'color': color_increasing}},
            'decreasing': {'line': {'color': color_decreasing}},
            'name': label + " " + str(total)
        }]
    return figure_data, total


default_graph = get_daily_graph(currency, date)


def get_monthly_graph():
    return dcc.Graph(
        id='month-evolution',
        figure=get_monthly_figure()
    )


def get_monthly_figure():
    potential_totals = get_monthly_data('potential/')
    performance_totals = get_monthly_data('performance/')
    for date, performance_total in performance_totals.iteritems():
        if date not in potential_totals or performance_total > potential_totals[date]:
            potential_totals[date] = performance_total
            name_date = date.replace('-', '')
            shutil.copy(base_path + 'performance/' + name_date + '.csv',
                        base_path + 'potential/' + name_date + '.csv')

    return {
        'data':
            [
                {'x': potential_totals.index, 'y': potential_totals.values, 'type': 'line',
                 'name': 'Reference ' + str(potential_totals.values.sum()),
                 'mode': 'markers',
                 'marker': {
                     'size': 20,
                     'color': colorscale[0]
                 }
                 },
                {'x': performance_totals.index, 'y': performance_totals.values, 'type': 'line',
                 'name': 'Performance ' + str(performance_totals.values.sum()),
                 'mode': 'markers',
                 'marker': {
                     'color': colorscale[1],
                     'size': 16,
                 }
                 }
            ],
        'layout': {
            'title': "Monthly potential "
        }
    }


def get_monthly_data(potential_folder):
    totals = pd.Series()
    total_frames = []
    for totals_file in os.listdir(os.path.join(base_path, potential_folder)):
        frame = pd.read_csv(os.path.join(base_path, potential_folder + totals_file),
                            names=['start_date', 'end_date', 'profit', 'start_rate', 'end_rate', 'wait', 'type',
                                   'budget'])
        total_frames.append(frame)
    if total_frames:
        frames = pd.concat(total_frames)
        frames['date'] = frames.start_date.apply(dateutil.parser.parse)
        frames['day'] = frames.date.apply(datetime.date.strftime, args=('%Y-%m-%d',))
        totals = frames.groupby(['day'])['profit'].aggregate(sum)
    return totals


app.layout = html.Div(children=[
    html.Div([html.H4("RL agent interacting with the gopherfx environment.")]),
    html.Div(id='graph-container', children=[
        get_daily_graph(currency, date),
        get_monthly_graph(),
        dcc.Interval(
            id='interval-day-update',
            interval=5 * 1000,
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-month-update',
            interval=30 * 1000,
            n_intervals=0
        )
    ])
])


@app.callback(
    dash.dependencies.Output('day-evolution', 'figure'),
    [dash.dependencies.Input('month-evolution', 'clickData'),
     dash.dependencies.Input('interval-day-update', 'n_intervals')])
def update_output(value, n_intervals):
    global date
    if value:
        date = pd.to_datetime(value['points'][0]['x']).strftime('%Y%m%d')

    return get_daily_figure(currency, date)


@app.callback(
    dash.dependencies.Output('month-evolution', 'figure'),
    [dash.dependencies.Input('interval-month-update', 'n_intervals')])
def update_output(n_intervals):
    return get_monthly_figure()


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
