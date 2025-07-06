import os
from flask import Flask, render_template, request, redirect, jsonify, session
# Impostando Dashboards
from templates.dash1.main import dashboard1

# Descricao enfermidades
from templates.descricao_page.decricao_page import descricao_page

# mapa de distribuição de enfermidades
from templates.map_plot.map_plot import map_plot_dash

# Backend
from backend.create_user import create_user, user_exists, return_json_data, user_exists_login

app = Flask(import_name='BI da Sesa')
app.secret_key = 'sua_chave_secreta_aqui'  # Necessário para usar sessions

# Inicialize o dashboard dentro do contexto da aplicação
with app.app_context():
    dashboard1(app)

with app.app_context():
    descricao_page(app)

with app.app_context():
    map_plot_dash(app)

# Pagina incial de login na aplicação
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_   = request.form['email']
        password = request.form['password']
        
        if email_ == 'admin' and password == 'admin':
            # Armazena informações do usuário na sessão
            session['username'] = email_
            session['user_type'] = 'admin'
            return redirect('/home')
        else:
            if user_exists_login(email_, password):
                session['username'] = email_   
                return redirect('/home')
            else:
                return render_template('login/login.html', message = True)
    
    return render_template('login/login.html', message = False)


@app.route('/cadastro', methods=['POST'])
def cadastro():
    if request.method == 'POST':
        username  = request.form['username']
        email     = request.form['email']
        password  = request.form['password']
        passwordR = request.form['passwordR']
        
        if password == passwordR:
            if create_user(email, username, password):
                session['username'] = username
                return redirect('/home')
            
            return render_template('login/login.html', mensagen = 'true')
        else:
            return render_template('login/login.html', mensagen = 'true')
    
    return render_template('login/login.html')


# Pagina home após o login
@app.route('/home')
def home():
    return render_template('home/home.html')

@app.route('/dash1')
def dash1(): 
    return redirect('/home/dash1/')

@app.route('/map_plot')
def map_plot():
    return redirect('/home/map_plot/')

@app.route('/descricao_page')
def descricao_page(): 
    return redirect('/home/descricao_page/')

@app.route('/config_user', methods=['GET'])
def config_user(): 
    
    return render_template('config_user/config_user.html')


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    user = data.get('user')
    password = data.get('password')
    
    # Limpa a sessão
    session.clear()
    
    return jsonify(dict(
        user = user,
        password = password,
        message = 'Logout realizado com sucesso'
    )), 200



if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)