from dash import html, dcc, Input, Output
from dashapp import app, server, database, bcrypt
from dashapps.models import usuario
from dash import State
from flask_login import login_user, logout_user

opcoes_dropdown = [
    {'label': 'Dia 1', 'value': 'Dia 1'},
    {'label': 'Dia 2', 'value': 'Dia 2'}
]

layout_homepage = html.Div([
    dcc.Location(id='homepage_url', refresh=True),
    html.H2('Criar Conta')
    html.Div([
        dcc.Input(id ='email', type = 'email', placeholder='Seu e-mail'),
        dcc.Input(id ='senha', type = 'password', placeholder='Sua senha'),
        html.Buttom('Criar conta', id='botao-criarconta'),
        dcc.Link('Ja tem uma conta? Faça seu login aqui', '/login')
    ], className='form-column')
])

layout_login = html.Div([
    dcc.Location(id='login_url', refresh=True),
    html.H2('Faça seu Login'),
    html.Div([
    dcc.Input(id ='email', type = 'email', placeholder='Seu e-mail'),
    dcc.Input(id ='senha', type = 'password', placeholder='Sua senha'),
    html.Buttom('Faça Login', id='botao-login')
    ], className='form-column')
])

layout_dashboard = html.Div(
    dcc.Location(id='dashboard_url', refresh=True),
    html.H2('Meu dashboard'),
    dcc.Dropdown(id = 'dropdown', options=opcoes_dropdown, value = 'Dia 1'),
    dcc.Graph(id='grafico'),
)

layout_erro = html.Div([
    dcc.Location(id='erro_url', refresh=True),
    html.H2('Erro de Acesso'),
    html.Div([
    dcc.Link('Clique aqui para acessar uma conta', '/'),
    dcc.Link('Clique aqui para fazer login', '/login')
    ], className='form-column')
])

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1('Dashapp'),
    html.Div(id='conteudo_pagina')
])

@app.callback(Output('conteudo_pagina','children'), Input('url', 'pathname')) 
              
def carregar_pagina(pathname):
    if pathname == '/':
        return layout_homepage
    elif pathname == '/dashboard':
        return layout_dashboard
    elif pathname == '/login':
        return layout_login
    elif pathname == '/erro':
        return layout_erro
    
@app.callback(Output('url','pathname'), Input('botao-criarconta', 'n_clicks'),
                    [State('email', 'value'), State('senha','value')])
def criar_conta(n_clicks, email, senha):
    if n_clicks:
        usuario = usuario.query.filter_by(email=email).first()
        if usuario:
            return '/erro'
        else:
            senha_criptografada = bcrypt.generate_password_hash(senha).decode('utf-8')
            usuario = usuario(email=email, senha=senha)
            database.session.add(usuario)
            database.session.commit()
            login_user(usuario)
            return '/dashboard'

@app.callback(Output('grafico', 'figure'), Input('dropdown', 'value'))
def atualizar_grafico(valor_dropdown):
    if valor_dropdown == 'Dia 1':
        pontos = {'x': [1,2,3,4], 'y': [4,1,2,1]}
        titulo = 'Gráfico Dia 1'
    else:
        pontos = {'x': [1,2,3,4], 'y': [4,1,2,1]}
        titulo = 'Gráfico Dia 2'
        return {'layout': {'title': titulo}, 'data':[pontos]}

@server.route('/nova_tela')
def nova_tela():
    return 'Você está na página criada pelo Flask'