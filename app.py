from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import sqlite3
import random
import smtplib
from email.mime.text import MIMEText



app = Flask(__name__)
Bootstrap(app)


gameState = "running"

@app.route('/')
def index():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get the current game state from the game_state table
    c.execute('SELECT game_state FROM game_state')
    gameState = c.fetchone()[0]

    conn.close()

    return render_template('index.html', gameState=gameState)

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

@app.route('/delete_data', methods=['POST'])
def delete_data():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users')
    conn.commit()
    conn.close()
    return ''


@app.route('/generate_targets', methods=['POST'])
def generate_targets():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get a list of all first names in the database
    c.execute('SELECT id, first_name FROM users')
    rows = c.fetchall()
    firstNames = [row[1] for row in rows]

    # Shuffle the list of first names randomly
    random.shuffle(firstNames)

    # Update the target column of each row with the corresponding shuffled name
    for i, firstName in enumerate(firstNames):
        # Get the current row ID
        currentId = rows[i][0]

        # Get the ID of the next row (taking into account the possibility of wrapping around to the beginning of the list)
        nextId = rows[(i + 1) % len(rows)][0]

        # Skip over the current row when updating the target column
        if currentId == nextId:
            continue

        # Update the target column of the current row with the corresponding shuffled name
        c.execute('UPDATE users SET target = ? WHERE id = ?', (firstNames[(i + 1) % len(firstNames)], currentId))

    conn.commit()
    conn.close()
    return ''

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

@app.route('/send_emails')
def send_emails():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Get the first name, last name, and email address for each user
    c.execute('SELECT first_name, last_name, email, target FROM users')
    rows = c.fetchall()

    # Send an email to each user with their target information
    for row in rows:
        firstName = row[0]
        lastName = row[1]
        emailAddress = row[2]
        target = row[3]

        # Create the email message
        message = f"Hello {firstName} {lastName}, your target is {target}."

        # Create the email object
        email = MIMEText(message)
        email['From'] = 'gamemaster@bist.be'
        email['To'] = emailAddress
        email['Subject'] = 'Your Target Information'

        # Send the email using SMTP
        with smtplib.SMTP('yoursmtpserver', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login('usenrame', 'password')
            smtp.sendmail('yoursenderemail', emailAddress, email.as_string())

    conn.close()

    return 'Emails sent!'
# def admin():
#     conn = sqlite3.connect('users.db')
#     c = conn.cursor()
#     c.execute('SELECT * FROM users')
#     records = c.fetchall()
#     conn.close()
#     return render_template('admin.html', records=records)






if __name__ == '__main__':
    app.run(debug=True)

