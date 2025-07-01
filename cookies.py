from flask import Flask, make_response, request

app = Flask(__name__)

@app.get('/hello')
def keep_track_of_requests():
    current_count = request.cookies.get('number_of_requests')

    if not current_count:
        current_count = 0

    current_count = int(current_count)

    response = make_response(f'You have sent {current_count + 1} requests!')
    response.set_cookie('number_of_requests', f'{current_count + 1}')
    
    return response
