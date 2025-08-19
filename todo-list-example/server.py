from flask import Flask, render_template, request

app = Flask(__name__)

my_todos = [
    { 'text': 'Go to the grocery store' },
    { 'text': 'Feed the dog' },
    { 'text': 'Do the laundry' }
]

@app.route('/')
def todo_list_page():
    return render_template(
        'todo-list-page.html',
        todos=my_todos
    )

@app.route('/jinja')
def todo_list_page_jinja():
    return render_template(
        'todo-list-page-jinja.html', 
        todos=my_todos
    )

@app.get('/api/todos')
def load_todos():
    return my_todos

@app.post('/api/todos')
def create_todo():
    new_todo_text = request.json['text']
    new_todo = { 'text': new_todo_text }
    my_todos.append(new_todo)

    return new_todo

@app.delete('/api/todos/<todo_text>')
def delete_todo(todo_text):
    global my_todos
    my_todos = list(filter(
        lambda todo: todo['text'] != todo_text,
        my_todos
    ))

    return my_todos

@app.put('/api/todos/<todo_text>')
def mark_todo_as_complete(todo_text):
    global my_todos
    my_todos = list(map(
        lambda todo: todo if todo['text'] != todo_text else { **todo, 'is_complete': True },
        my_todos
    ))

    return my_todos
