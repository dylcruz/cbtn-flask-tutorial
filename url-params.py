from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/hello/<string:first_name>/<string:last_name>')
def say_hello_to(first_name, last_name):
    return f'Hello, {escape(first_name)} {escape(last_name)}!'

months = ['January', 'February']

@app.get('/events/<int:month>/<int:day>/<int:year>')
def load_events_for_date(month, day, year):
    month_name = months[month-1]
    return f'Here are your events for {month_name} {day}, {year}!'

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
        return 'Person not found'