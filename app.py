from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Membuat database dan tabel
conn = sqlite3.connect('tasks.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    subject TEXT,
    deadline TEXT,
    completed INTEGER DEFAULT 0
)
''')

conn.commit()
conn.close()


@app.route('/')
def index():

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute('SELECT * FROM tasks ORDER BY subject ASC')
    tasks = c.fetchall()

    total = len(tasks)
    completed = len([task for task in tasks if task[4] == 1])

    progress = 0

    if total > 0:
        progress = int((completed / total) * 100)

    conn.close()

    return render_template(
        'index.html',
        tasks=tasks,
        progress=progress
    )


@app.route('/add', methods=['POST'])
def add_task():

    title = request.form['title']
    subject = request.form['subject']
    deadline = request.form['deadline']

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute(
        'INSERT INTO tasks (title, subject, deadline) VALUES (?, ?, ?)',
        (title, subject, deadline)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/complete/<int:id>')
def complete_task(id):

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute(
        'UPDATE tasks SET completed = 1 WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_task(id):

    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()

    c.execute(
        'DELETE FROM tasks WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)