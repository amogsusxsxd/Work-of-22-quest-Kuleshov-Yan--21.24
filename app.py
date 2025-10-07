from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('guestbook.db')
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    if not os.path.exists('guestbook.db'):
        conn = get_db_connection()
        conn.execute('''
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    init_db() 
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route('/sign', methods=['POST'])
def sign():
    author = request.form['author']
    message = request.form['message']
    timestamp = datetime.now().isoformat()

    if author and message:
        conn = get_db_connection()
        conn.execute('INSERT INTO messages (author, message, timestamp) VALUES (?, ?, ?)',
                     (author, message, timestamp))
        conn.commit()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)