import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Database configuration
# In a real app, this would be in a config file or env var.
# For testing purposes, we can override this.
DB_PATH = os.environ.get('DATABASE_URL', 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                is_completed INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db_connection()
    todos = conn.execute(
        'SELECT * FROM todos ORDER BY created_at DESC, id DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    
    if not title:
        # Spec says: POST /add (title="") -> HTTP 302 or Error page and failure to add
        # To keep it simple and follow common practice, we can just return an error or redirect.
        # Let's just not add anything and redirect back to index.
        # However, for the test to pass "failure to add", we must ensure nothing is added.
        return redirect(url_for('index'))

    conn = get_db_connection()
    conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    conn = get_db_connection()
    todo = conn.execute(
        'SELECT is_completed FROM todos WHERE id = ?', (todo_id,)
    ).fetchone()

    if todo is None:
        conn.close()
        return 'Not Found', 404

    new_status = 0 if todo['is_completed'] else 1
    conn.execute(
        'UPDATE todos SET is_completed = ? WHERE id = ?', (new_status, todo_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    conn = get_db_connection()
    todo = conn.execute('SELECT id FROM todos WHERE id = ?', (todo_id,)).fetchone()
    
    if todo is None:
        conn.close()
        return 'Not Found', 404

    conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
