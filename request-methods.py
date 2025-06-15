from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def print_method():
    print(f'I just received a {request.method} request')
    return 'Thanks for the request!'

@app.get('/todos')
def list_todos():
    return 'Here are your TODOs...'

@app.post('/todos')
def create_todo():
    print(request.json)
    return f'Creating a new TODO with the text \'{request.json["text"]}\''

@app.put('/todos/123')
def update_todo():
    try:
        new_text = request.json['new_text']
        return f'Changing the text of todo 123 to "{new_text}"'
    except KeyError:
        return make_response('Must include a "new_text" property!', 400)

@app.delete('/todos/123')
def delete_todo():
    return 'Deleting TODO with id 123'


# @app.route('/todos', methods=['GET', 'POST'])
# def todos_route():
#     if request.method == 'GET':
#         return 'Here are your TODOs...'
#     elif request.method == 'POST':
#         return 'Creating a new TODO...'

# @app.route('/todos/123', methods=['PUT', 'DELETE'])
# def individual_todo_route():
#     if request.method == 'PUT':
#         return 'Updating TODO with id 123'
#     elif request.method == 'DELETE':
#         return 'Deleting TODO with id 123'
