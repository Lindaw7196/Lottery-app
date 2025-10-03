from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import random

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('lottery.db')
    conn.row_factory = sqlite3.Row
    return conn

with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        with get_db_connection() as conn:
            try:
                conn.execute('INSERT INTO participants (name, email) VALUES (?, ?)', (name, email))
                conn.commit()
            except sqlite3.IntegrityError:
                return "Email already entered!", 400
        return redirect(url_for('index'))

    with get_db_connection() as conn:
        participants = conn.execute('SELECT * FROM participants').fetchall()
    return render_template('index.html', participants=participants)

@app.route('/draw')
def draw():
    with get_db_connection() as conn:
        participants = conn.execute('SELECT * FROM participants').fetchall()
    if not participants:
        return "No participants yet!"
    winner = random.choice(participants)
    return f"Winner: {winner['name']} ({winner['email']})"

if __name__ == '__main__':
    app.run(debug=True)
