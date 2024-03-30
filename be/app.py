from flask import Flask, render_template, request, redirect, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from math import ceil
from bson import ObjectId
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode, quote_plus

AUTH0_CLIENT_ID = 'GMUL2XNE7KctLcwwRNmsE8Yorj1uv1mB'
AUTH0_DOMAIN = 'dev-bgni6r2aiwkt4xgt.us.auth0.com'
AUTH0_CLIENT_SECRET = 'WIWh9Qgs5Bu8P5P9m_hOdF27pnOinSRa1QQ2SMRucmQySsUFh9B25SDmDUNp0pTC'
APP_SECRET_KEY = 'YOUR_SECRET'

app = Flask(__name__)

app.secret_key = APP_SECRET_KEY

oauth = OAuth(app)

oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

uri = "mongodb+srv://mertsagcan:QSd1qTO6ETj2ETKy@cengdendb.sznqoxa.mongodb.net/?retryWrites=true&w=majority&appName=cengdendb"
client = MongoClient(uri, server_api=ServerApi('1'))



#items = [
#    {"id": i, "title": f"Item {i}", "description": f"Description for Item {i}", "category": "Category"}
#    for i in range(1, 101)  # Generating 100 items for demonstration
#]

ITEMS_PER_PAGE = 10

@app.route('/')
def home():
    items = list(client.cengdendb.items.find())
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)
    if 'user' in session:
        if session['user']['userinfo']['user_metadata']['is_admin']:
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category="All Items", is_admin=True)
        else:
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category="All Items", is_admin=False)
    else:
        return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=False, category="All Items", is_admin=False)

@app.route('/categories/<string:category>')
def category(category):
    if(category == "vehicles"):
        category1 = "Vehicles"
    elif(category == "phones"):
        category1 = "Phones"
    elif(category == "computers"):
        category1 = "Computers"
    elif(category == "private-lessons"):
        category1 = "Private Lessons"
    items = list(client.cengdendb.items.find({"category" : category1}))
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)
    if 'user' in session:
        if session['user']['userinfo']['user_metadata']['is_admin']:
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category=category1, is_admin=True)
        else:
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category=category1, is_admin=False)
    else:
        return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=False, category=category1, is_admin=False)

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(url_for('callback', _external=True))

@app.route('/signup')
def signup():
    return oauth.auth0.authorize_redirect(url_for('callback', _external=True), screen_hint='signup')

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    nonce = session.get('nonce')
    user = oauth.auth0.parse_id_token(token, nonce=nonce)
    session['user'] = token
    user_id = user['sub']
    user_name = user['user_metadata']['fullName']
    user_email = user['email']
    user_phone = user['user_metadata']['phoneNumber']
    user_data = {"_id": user_id, "name": user_name, "email": user_email , "phone": user_phone}
    if not client.cengdendb.users.find_one({"_id": user_id}):
        client.cengdendb.users.insert_one(user_data)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?' + urlencode(params, quote_via=quote_plus))

@app.route('/item/<string:item_id>')
def item_detail(item_id):
    item  = client.cengdendb.items.find_one({"_id" : ObjectId(item_id)})
    print
    if item:
        return render_template('item-details.html', item=item)
    else:
        return "Item not found", 404

@app.route('/profile')
def profile():
    user_id = session['user']['userinfo']['sub']
    user_details = client.cengdendb.users.find_one({"_id": user_id})
    if 'user' in session:
        return render_template('profile.html', user=user_details, signed_in=True)
    else:
        return redirect(url_for('login'))

@app.route("/add-item")
def add_item():
    return render_template('add-item.html', signed_in=True)

# Route for handling form submission and adding item to MongoDB
@app.route("/add-item", methods=["POST"])
def handle_add_item():
    form_fields = {}
    form_fields["owner_id"] = client.cengdendb.users.find_one({"email": session.get('user')["userinfo"]["email"]})["_id"]
    form_fields["favoured_users"] = []

    for key in request.form:
        form_fields[key] = request.form[key]

    form_fields = {k: v for k, v in form_fields.items() if v is not None and v != ""}

    try:
        client.cengdendb.items.insert_one(form_fields)
        message = "Item added successfully!"
    except Exception as e:
        message = "An error occurred, please try again."

    return redirect('/')

@app.route("/users-items")
def users_items():
    user_id = session['user']['userinfo']['sub']
    items = list(client.cengdendb.items.find({"owner_id": user_id}))
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)
    return render_template('users-items.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True)


if __name__ == '__main__':
    app.run(debug=True)
