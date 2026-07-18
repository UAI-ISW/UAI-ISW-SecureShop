from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        
        conn = sqlite3.connect('secure_shop.db')
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE usuario = ? AND password = ?',
                 (usuario, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            return redirect(url_for('estadisticas'))
        else:
            return 'Credenciales incorrectas'
    return render_template('login.html')

@app.route('/estadisticas')
def estadisticas():
    response = requests.get('http://localhost:5001/mascotas')
    mascotas = response.json()
    return render_template('estadisticas.html', mascotas=mascotas)

if __name__ == '__main__':
    app.run(debug=True, port=5002) 