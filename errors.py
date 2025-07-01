from flask import Flask, abort, request

app = Flask(__name__)

people = [
    {'id': '123', 'name': 'dylan'},
    {'id': '234', 'name': 'bob'},
    {'id': '345', 'name': 'sue'}, 
]

@app.get('/people/<string:person_id>')
def load_person_by_id(person_id):
    try:
        person = next(person for person in people if person.get('id') == person_id)
        return person
    except StopIteration:
        abort(404)

fruits = [
    'apple',
    'banana',
    'cherry',
    'date',
    'eggplant',
    'fig'
]

@app.get('/fruits')
def filter_fruits():
    search_string = request.args.get('s')
    
    if not search_string:
        abort(400)
    else:
        matching_fruits = [f for f in fruits if search_string in f]
    
    return matching_fruits

@app.errorhandler(400)
def handle_bad_request(error):
    print(error)
    return 'You forgot something in your request!'

@app.errorhandler(404)
def handle_not_found(error):
    print(error)
    return 'Nope! Can\'t find it'

@app.errorhandler(Exception)
def handle_everything(error):
    print(error)
    return 'Something bad happened...'
