from flask import Flask, render_template, jsonify
from scraper import scrape_news

app = Flask(__name__)

@app.route("/")
def index():
    articles = scrape_news()
    return render_template("index.html", articles=articles)

@app.route("/api/news")
def api_news():
    return jsonify(scrape_news())

if __name__ == "__main__":
    app.run(debug=True)

