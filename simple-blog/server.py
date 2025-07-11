from flask import abort, Flask, render_template

articles = [
    { "slug": "python", "title": "Learn Python", "content": "Blah blah blah blah" },
    { "slug": "flask", "title": "Learn Flask",  "content": "Blah blah blah blah" },
    { "slug": "jinja", "title": "Learn Jinja",  "content": "Blah blah blah blah" },
]

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/articles')
def articles_list_page():
    return render_template('articles-list.html', articles=articles)

@app.route('/articles/<article_slug>')
def individual_article_page(article_slug):
    try:
        article = next((a for a in articles if a.get('slug') == article_slug))
        title = article.get('title')
        content = article.get('content')
    except StopIteration:
        abort(404)
    return render_template('article.html', title=title, content=content)

@app.errorhandler(404)
def not_found_page(err):
    return render_template('not-found.html')