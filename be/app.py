from flask import Flask, render_template, request, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from math import ceil

app = Flask(__name__)


items = [
    {"id": i, "title": f"Item {i}", "description": f"Description for Item {i}", "category": "Category"}
    for i in range(1, 101)  # Generating 100 items for demonstration
]

ITEMS_PER_PAGE = 10

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)

    return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return render_template('item_details.html', item=item)
    else:
        return "Item not found", 404


if __name__ == '__main__':
    app.run(debug=True)
