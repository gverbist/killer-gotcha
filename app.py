from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register')
# def register():
#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)', (first_name, last_name, email))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        return render_template('register.html')

@app.route('/game-rules')
def game_rules():
    return render_template('game_rules.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)

