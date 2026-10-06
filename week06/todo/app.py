import db
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Expose DB_PATH for testing compatibility
DB_PATH = db.DB_PATH

# Expose init_db for testing compatibility
def init_db():
    db.init_db()

@app.route('/')
def index():
    todos = db.get_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    
    if not title:
        return redirect(url_for('index'))

    db.add_todo(title)
    return redirect(url_for('index'))


@app.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle(todo_id):
    success = db.toggle_todo(todo_id)

    if not success:
        return 'Not Found', 404

    return redirect(url_for('index'))


@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    success = db.delete_todo(todo_id)

    if not success:
        return 'Not Found', 404

    return redirect(url_for('index'))


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
