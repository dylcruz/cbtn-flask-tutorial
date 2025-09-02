from flask import abort, Flask, render_template, request

articles = [
    {
        "slug": "python",
        "title": "Learn Python",
        "content": "Blah blah blah blah",
        "upvotes": 0,
        "comments": [],
    },
    {
        "slug": "flask",
        "title": "Learn Flask",
        "content": "Blah blah blah blah",
        "upvotes": 0,
        "comments": [],
    },
    {
        "slug": "jinja",
        "title": "Learn Jinja",
        "content": "Blah blah blah blah",
        "upvotes": 0,
        "comments": [],
    },
]

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template(
        "home.html",
        most_popular_articles=sorted(
            articles, key=lambda x: x["upvotes"], reverse=True
        ),
    )


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/articles")
def articles_list_page():
    return render_template("articles-list.html", articles=articles)


@app.route("/articles/<article_slug>")
def individual_article_page(article_slug):
    try:
        article = next((a for a in articles if a.get("slug") == article_slug))
    except StopIteration:
        abort(404)
    return render_template(
        template_name_or_list="article.html",
        title=article.get("title"),
        content=article.get("content"),
        upvotes=article.get("upvotes"),
        slug=article.get("slug"),
        comments=article.get("comments"),
    )


@app.post("/api/articles/<article_slug>/upvotes")
def add_upvote_to_article(article_slug):
    try:
        article = next((a for a in articles if a.get("slug") == article_slug))
        article["upvotes"] += 1
        return article
    except StopIteration:
        abort(404)


@app.post("/api/articles/<article_slug>/comments")
def add_comment_to_article(article_slug):
    try:
        article = next((a for a in articles if a.get("slug") == article_slug))
        author = request.json["author"]
        text = request.json["text"]

        new_comment = {
            "author": author,
            "text": text,
        }
        article["comments"].append(new_comment)

        return article

    except StopIteration:
        abort(404)


@app.errorhandler(404)
def not_found_page(err):
    return render_template("not-found.html")
