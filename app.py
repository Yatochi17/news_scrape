from flask import Flask, render_template, jsonify
from scraper import scrape_news
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
        articles = scrape_news()
        if not articles:
            return render_template("index.html", articles=[], error="Unable to fetch news at this time.")
        return render_template("index.html", articles=articles)
    except Exception as e:
        return render_template("index.html", articles=[], error=str(e))

@app.route("/api/news")
def api_news():
    try:
        articles = scrape_news()
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
