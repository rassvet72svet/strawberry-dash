import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "🍓 Strawberry Elephant ×4"

app.layout = dbc.Container([
    dcc.Store(id='stats', data={'correct': 0, 'total': 0}),
    dbc.Row([
        dbc.Col([
            html.H1("🍓 Strawberry Elephant", className="text-center mt-4", style={'color': '#e75480'}),
            html.P("Учим таблицу умножения на 4!", className="text-center h4 text-muted mb-4"),
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📖 Таблица", className="h5"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H5(f"4 × {i} = ?", className="text-primary"),
                                html.Button("Ответ", id={'type': 'answer-btn', 'index': i},
                                           className="btn btn-outline-success btn-sm mt-2",
                                           n_clicks=0),
                                html.H4(f"{4*i}", id={'type': 'answer', 'index': i},
                                       style={'display': 'none', 'color': '#e75480', 'marginTop': '8px'})
                            ], style={'textAlign': 'center', 'padding': '15px', 'borderRadius': '10px', 'backgroundColor': '#f8f9fa'})
                        ], width=2) for i in range(1, 11)
                    ])
                ])
            ], className="mb-4")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("✏️ Тренажёр", className="h5"),
                dbc.CardBody([
                    html.H3(id='question', children="4 × 1 = ?", className="text-center mb-4"),
                    dbc.Row([
                        dbc.Col(dbc.Input(id='user-input', type='number', placeholder="Твой ответ...",
                                          className="text-center"), width=6, className="mx-auto")
                    ]),
                    html.Div([
                        dbc.Button("✅ Проверить", id='check-btn', color="primary", className="m-2"),
                        dbc.Button("🎲 Новый пример", id='new-btn', color="secondary", className="m-2")
                    ], className="text-center mt-3"),
                    html.Hr(),
                    html.Div(id='result', className="h4 text-center mt-2"),
                    html.Div([
                        dbc.Badge("Правильно: ", color="light", className="h5 mr-2"),
                        dbc.Badge(id='correct-counter', children="0", color="success", className="h5 mr-4"),
                        dbc.Badge("Всего: ", color="light", className="h5 mr-2"),
                        dbc.Badge(id='total-counter', children="0", color="info", className="h5 mr-4"),
                        dbc.Badge("Успех: ", color="light", className="h5 mr-2"),
                        dbc.Badge(id='success-rate', children="0%", color="warning", className="h5")
                    ], className="text-center mt-4")
                ])
            ])
        ])
    ])
], fluid=True)

for i in range(1, 11):
    @app.callback(
        Output({'type': 'answer', 'index': i}, 'style'),
        Input({'type': 'answer-btn', 'index': i}, 'n_clicks'),
        prevent_initial_call=True
    )
    def show_answer(n_clicks):
        if n_clicks:
            return {'display': 'block', 'color': '#e75480', 'marginTop': '8px'}
        raise dash.exceptions.PreventUpdate

@app.callback(
    [Output('question', 'children'),
     Output('user-input', 'value'),
     Output('result', 'children'),
     Output('stats', 'data')],
    [Input('check-btn', 'n_clicks'),
     Input('new-btn', 'n_clicks')],
    [State('question', 'children'),
     State('user-input', 'value'),
     State('stats', 'data')],
    prevent_initial_call=True
)
def handle_game(check_clicks, new_clicks, current_q, user_answer, stats):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == 'new-btn':
        num = random.randint(1, 10)
        new_question = f"4 × {num} = ?"
        return new_question, '', '', stats
    elif trigger_id == 'check-btn' and user_answer is not None:
        try:
            current_num = int(current_q.split('×')[1].split('=')[0].strip())
            correct_answer = 4 * current_num
            stats['total'] += 1
            if int(user_answer) == correct_answer:
                stats['correct'] += 1
                result_msg = html.Span("🍓 Верно! Умничка!", style={'color': 'green'})
            else:
                result_msg = html.Span(f"😢 Почти! Правильно: {correct_answer}", style={'color': 'red'})
            return dash.no_update, '', result_msg, stats
        except:
            return dash.no_update, dash.no_update, html.Span("Введи число!", style={'color': 'orange'}), stats
    raise dash.exceptions.PreventUpdate

@app.callback(
    [Output('correct-counter', 'children'),
     Output('total-counter', 'children'),
     Output('success-rate', 'children')],
    Input('stats', 'data')
)
def update_stats(data):
    correct = data['correct']
    total = data['total']
    rate = int((correct / total * 100)) if total > 0 else 0
    return str(correct), str(total), f"{rate}%"

if __name__ == '__main__':
    app.run(debug=False, port=8050)
