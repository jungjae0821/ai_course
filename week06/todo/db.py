import sqlite3
import os


def get_db_connection():
    db_path = os.environ.get('DATABASE_URL', 'todo.db')
    conn = sqlite3.connect(db_path)
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


def get_todos():
    with get_db_connection() as conn:
        return conn.execute(
            'SELECT * FROM todos ORDER BY created_at DESC, id DESC'
        ).fetchall()


def add_todo(title):
    with get_db_connection() as conn:
        conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
        conn.commit()


def toggle_todo(todo_id):
    with get_db_connection() as conn:
        todo = conn.execute(
            'SELECT is_completed FROM todos WHERE id = ?', (todo_id,)
        ).fetchone()

        if todo is None:
            return False

        new_status = 0 if todo['is_completed'] else 1
        conn.execute(
            'UPDATE todos SET is_completed = ? WHERE id = ?', (new_status, todo_id)
        )
        conn.commit()
        return True


def update_todo_title(todo_id, new_title):
    with get_db_connection() as conn:
        todo = conn.execute('SELECT id FROM todos WHERE id = ?', (todo_id,)).fetchone()
        if todo is None:
            return False

        conn.execute(
            'UPDATE todos SET title = ? WHERE id = ?', (new_title, todo_id)
        )
        conn.commit()
        return True


def delete_todo(todo_id):
    with get_db_connection() as conn:
        todo = conn.execute('SELECT id FROM todos WHERE id = ?', (todo_id,)).fetchone()
        if todo is None:
            return False

        conn.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        return True


# For testing compatibility in app.py
DB_PATH = os.environ.get('DATABASE_URL', 'todo.db')
