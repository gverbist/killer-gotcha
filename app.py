from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
Bootstrap(app)


gameState = "running"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT game_state FROM game_state WHERE id = 1')
    gameState = c.fetchone()[0]
    
    if gameState == 'running':
        return redirect(url_for('game_running'))

    if request.method == 'POST':
        firstName = request.form['first_name']
        lastName = request.form['last_name']
        email = request.form['email']
        c.execute('INSERT INTO users (first_name, last_name, email) VALUES (?, ?, ?)', (firstName, lastName, email))
        conn.commit()
        conn.close()
        return redirect(url_for('thank_you'))
    
    conn.close()
    return render_template('register.html')

@app.route('/game_running')
def game_running():
    return render_template('game_running.html')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/game-rules')
def game_rules():
    return render_template('game_rules.html')

# @app.route('/admin')
# def admin():
#     return render_template('admin.html')


@app.route('/admin')
def admin():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    records = c.fetchall()
    c.execute('SELECT game_state FROM game_state WHERE id = 1')
    gameState = c.fetchone()[0]
    conn.close()
    return render_template('admin.html', records=records, gameState=gameState)

@app.route('/toggle_game_state')
def toggle_game_state():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT game_state FROM game_state WHERE id = 1')
    game_state = c.fetchone()[0]
    new_game_state = 'running' if game_state == 'stopped' else 'stopped'
    c.execute('UPDATE game_state SET game_state = ? WHERE id = 1', (new_game_state,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

@app.route('/update_game_state', methods=['POST'])
def update_game_state():
    gameState = request.form['gameState']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('UPDATE game_state SET game_state = ? WHERE id = 1', (gameState,))
    conn.commit()
    conn.close()
    return ''


# def admin():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users')
#     records = c.fetchall()
#     conn.close()
#     return render_template('admin.html', records=records)






if __name__ == '__main__':
    app.run(debug=True)

