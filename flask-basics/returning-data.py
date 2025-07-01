from flask import Flask, make_response, render_template

app = Flask(__name__)

@app.route('/users')
def get_users():
    user = { "id": "123", "name": "Dylan" }
    response = make_response(
        user,
        200,
    )
    response.headers['Content-Type'] = "application/json"

    return response

# @app.route('/article-1')
# def article1():
#     return render_template(
#         'article.html',
#         title='My First Article!',
#         content='Thank you for reading. This is my first article.'
#     )

# @app.route('/article-2')
# def article2():
#     return render_template(
#         'article.html',
#         title='My Second Article!',
#         content='Thank you for reading. This is my second article.'
#     )

# @app.route('/article-3')
# def article3():
#     return render_template(
#         'article.html',
#         title='My Third Article!',
#         content='Thank you for reading. This is my third article.'
#     )

@app.route('/', defaults={ "path": ""})
@app.route('/<path:path>')
def handle_request(path):
    if path == 'article-1':
        return render_template(
        'article.html',
        title='My First Article!',
        content='Thank you for reading. This is my first article.'
    )
    elif path == 'article-2':
        return render_template(
        'article.html',
        title='My Second Article!',
        content='Thank you for reading. This is my second article.'
    )
    elif path == 'article-3':
        return render_template(
        'article.html',
        title='My Third Article!',
        content='Thank you for reading. This is my third article.'
    )
    else:
        return 'Nope, that\'s not a route.'