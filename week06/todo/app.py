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
    # 미완료와 완료된 항목을 분리
    incomplete_todos = [t for t in todos if not t['is_completed']]
    completed_todos = [t for t in todos if t['is_completed']]
    return render_template('index.html', incomplete_todos=incomplete_todos, completed_todos=completed_todos)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()

    if not title:
        return redirect(url_for('index'))

    db.add_todo(title[:200])
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


@app.route('/edit/<int:todo_id>', methods=['POST'])
def edit(todo_id):
    new_title = request.form.get('title', '').strip()
    if not new_title:
        return redirect(url_for('index'))

    success = db.update_todo_title(todo_id, new_title[:200])
    if not success:
        return 'Not Found', 404

    return redirect(url_for('index'))


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
