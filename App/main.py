
from flask import Flask, render_template

app = Flask(import_name='BI da Sesa', template_folder='templates', static_folder='static')

@app.route('/bi')
def hello_world():
    return render_template('login/login.html')


@app.route('/bi/home')
def home():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)

