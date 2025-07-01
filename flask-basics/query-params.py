from flask import Flask, request

app = Flask(__name__)

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
        return fruits
    else:
        matching_fruits = [f for f in fruits if search_string in f]
    
    return matching_fruits
