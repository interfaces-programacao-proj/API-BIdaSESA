import os
from flask import Flask, render_template, request, redirect


# Impostando Dashboards
from templates.dash1.main import dashboard1

# Descricao enfermidades
from templates.descricao_page.decricao_page import descricao_page

app = Flask(import_name='BI da Sesa')

# Inicialize o dashboard dentro do contexto da aplicação
with app.app_context():
    # A função dashboard1 já registra o blueprint no app
    # Não precisa armazenar o resultado em uma variável
    dashboard1(app)

with app.app_context():
    # A função dashboard1 já registra o blueprint no app
    # Não precisa armazenar o resultado em uma variável
    descricao_page(app)


# Pagina incial de login na aplicação
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            return redirect('/home')
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


@app.route('/descricao_page')
def descricao_page():
    return redirect('/home/descricao_page/')

@app.route('/config_user')
def config_user():
    return render_template('config_user/config_user.html')

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True)
    

