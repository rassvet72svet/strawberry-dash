import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import random

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

app.layout = dbc.Container([
    html.H1("🍓 Strawberry Elephant: Вся таблица умножения", className="text-center mt-4 text-primary"),
    html.P("Решай примеры и собирай клубнички!", className="text-center text-muted mb-4 h5"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📚 Таблица умножения от 1 до 10", className="h4"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.H4(f"{i} × {j} = ?", className="text-center", style={'color': '#555'}),
                            html.H4(f"{i*j}", className="text-center text-success mt-2", style={'display': 'none'}, id=f'a-{i}-{j}')
                        ], className="border p-3 m-1 rounded"), width=2) for j in range(1, 11)
                    ]) for i in range(1, 11)
                ])
            ], className="mb-4")
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("✏️ Тренажёр", className="h4"),
                dbc.CardBody([
                    html.H2(id='question', children="", className="text-center mb-4 text-warning"),
                    dbc.Input(id='user-answer', type='number', placeholder="Введи ответ...", className="mb-3 text-center", size="lg"),
                    dbc.Row([
                        dbc.Col(dbc.Button("✅ Проверить", id='check-btn', color="primary", className="w-100"), width=6),
                        dbc.Col(dbc.Button("🎲 Новый пример", id='new-btn', color="secondary", className="w-100"), width=6)
                    ]),
                    html.Div(id='result', className="h3 text-center mt-3"),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(html.Div(["Правильно: ", html.Span("0", id="correct", className="text-success h3")]), className="text-center"),
                        dbc.Col(html.Div(["Всего: ", html.Span("0", id="total", className="text-info h3")]), className="text-center"),
                        dbc.Col(html.Div(["Успех: ", html.Span("0%", id="percent", className="text-warning h3")]), className="text-center")
                    ])
                ])
            ])
        ], width=12)
    ])
], fluid=True)

@app.callback(
    Output('question', 'children'),
    Input('new-btn', 'n_clicks'),
    Input('check-btn', 'n_clicks'),
    State('user-answer', 'value'),
    prevent_initial_call=True
)
def update_question(new_clicks, check_clicks, user_answer):
    ctx = dash.callback_context
    if not ctx.triggered or ctx.triggered_id == 'new-btn':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        return f"{a} × {b} = ?"
    return dash.no_update

@app.callback(
    [Output('user-answer', 'value'),
     Output('result', 'children'),
     Output('correct', 'children'),
     Output('total', 'children'),
     Output('percent', 'children')],
    Input('check-btn', 'n_clicks'),
    [State('question', 'children'),
     State('user-answer', 'value'),
     State('correct', 'children'),
     State('total', 'children')],
    prevent_initial_call=True
)
def check_answer(clicks, question, user_answer, correct_str, total_str):
    if user_answer is None:
        return "", html.Div("Введи число!", className="text-warning"), correct_str, total_str, dash.no_update

    try:
        a = int(question.split('×')[0].strip())
        b = int(question.split('×')[1].split('=')[0].strip())
        correct = a * b
        total = int(total_str) + 1

        if int(user_answer) == correct:
            correct_num = int(correct_str) + 1
            result = html.Div("🍓 Верно! Умничка!", className="text-success")
        else:
            correct_num = int(correct_str)
            result = html.Div(f"😢 Ой! Правильно: {correct}", className="text-danger")

        percent = f"{int((correct_num / total) * 100)}%" if total > 0 else "0%"
        return "", result, str(correct_num), str(total), percent

    except:
        return "", html.Div("Что-то пошло не так...", className="text-warning"), correct_str, total_str, dash.no_update

if __name__ == '__main__':
    app.run(debug=False, port=8050)
