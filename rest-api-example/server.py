from flask import abort, Flask, make_response, request
from operator import itemgetter
import uuid

app = Flask(__name__)

users = [
    {
        'id': '123',
        'username': 'dylan',
        'password': 'ABC123!',
        'number_of_articles': 5,
        'security_question_answer': 'abc',
    },
    {
        'id': '234',
        'username': 'dylbob',
        'password': 'XYZ789!',
        'number_of_articles': 100,
        'security_question_answer': 'fido',
    },
    {
        'id': '345',
        'username': 'sue',
        'password': '321ABC!',
        'number_of_articles': 14,
        'security_question_answer': 'smith',
    }
]

def sanitize_user(user):
    keys_to_copy = ['id', 'username', 'number_of_articles']
    sanitized_user = {}
    for key in keys_to_copy:
        sanitized_user[key] = user[key]

    return sanitized_user

# Create new users
@app.post('/users')
def create_user():
    username, password, security_qa = itemgetter(
        'username',
        'password',
        'security_question_answer',
        )(request.json)
    
    new_user = {
        'username': username,
        'password': password,
        'security_question_answer': security_qa,
        'id': uuid.uuid4(),
        'number_of_articles': 0,
    }
    users.append(new_user)
    return sanitize_user(new_user)

# Read (Load) -> List, "Read One", Search
@app.get('/users')
def list_users():
    # Make DB query
    search_string = request.args.get('name')

    if  search_string:
        matching_users = [user for user in users if search_string in user['username']]
        return list(map(sanitize_user, matching_users))

    return list(map(sanitize_user, users))

@app.get('/users/<string:user_id>')
def get_user(user_id):
    try:
        user = next(user for user in users if user['id'] == user_id)
        return sanitize_user(user)
    except StopIteration:
        abort(404)

@app.errorhandler(404)
def not_found(err):
    print(err)
    return make_response('That user does not exist', 404)

# Update 
@app.put('/users/<string:user_id>')
def update_user(user_id):
    update_fields = ['username', 'number_of_articles']
    try:
        user = next(user for user in users if user['id'] == user_id)
        for field in update_fields:
            if field in request.json:
                new_value = request.json[field]
                user[field] = new_value

        return sanitize_user(user)
    except StopIteration:
        abort(404)

# Delete
@app.delete('/users/<string:user_id>')
def delete_user(user_id):
    for user in users:
        if user['id'] == user_id:
            users.remove(user)
            break
    return list(map(sanitize_user, users))