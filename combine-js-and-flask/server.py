from flask import Flask, render_template, request

app = Flask(__name__)

articles = [{
    'title': 'Learn Flask',
}, {
    'title': 'Learn JavaScript',
}, {
    'title': 'Learn TypeScript',
}]

@app.route('/')
def front_and_back_end():
    return render_template('front-and-back-end.html')

@app.route('/back-end')
def back_end_only():
    global articles
    if request.args.get('remove'):
        articles = list(filter(
            lambda a: a['title'] != request.args.get('remove'), 
            articles
        ))
    return render_template(
        'back-end-only.html',
        articles=articles
        )

@app.route('/articles')
def get_articles():
    return articles
