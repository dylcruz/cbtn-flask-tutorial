from flask import Flask, g, make_response, request

app = Flask(__name__)

@app.before_request
def parse_number_of_requests():
    current_count_str = request.cookies.get('number_of_requests')
    g.current_count = int(current_count_str) if current_count_str else 0

@app.get('/hello')
def keep_track_of_requests():
    response = make_response(f'You have sent {g.current_count} requests!')
    g.current_count += 1
    return response

@app.get('/reset')
def reset_requests():
    g.current_count = 0
    return 'You have reset the number of requests.'

@app.after_request
def update_number_of_requests(response):
    response.set_cookie('number_of_requests', f'{g.current_count}')
    return response