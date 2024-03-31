from flask import Flask, render_template, request, redirect, url_for, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from math import ceil
from bson import ObjectId
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode, quote_plus
from auth0api import delete_user, update_user_password

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


ITEMS_PER_PAGE = 10

#This is the route for home page. It is accessible by everyone.
@app.route('/')
def home():
    if 'user' in session:
        user_id = session['user']['userinfo']['sub']
        if session['user']['userinfo']['user_metadata']['is_admin']:
            items = list(client.cengdendb.items.find())
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * ITEMS_PER_PAGE
            end = start + ITEMS_PER_PAGE
            total_pages = ceil(len(items) / ITEMS_PER_PAGE)
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category="All Items", is_admin=True, user_id=user_id)
        else:
            items = list(client.cengdendb.items.find({"is_active": True}))
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * ITEMS_PER_PAGE
            end = start + ITEMS_PER_PAGE
            total_pages = ceil(len(items) / ITEMS_PER_PAGE)
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category="All Items", is_admin=False, user_id=user_id)
    else:
        items = list(client.cengdendb.items.find({"is_active": True}))
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        total_pages = ceil(len(items) / ITEMS_PER_PAGE)
        return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=False, category="All Items", is_admin=False, user_id=False)

#This is the route for categories. It is accessible by everyone.
@app.route('/categories/<string:category>')
def category(category):
    if 'user' in session:
        user_id = session['user']['userinfo']['sub']
        if session['user']['userinfo']['user_metadata']['is_admin']:
            items = list(client.cengdendb.items.find({"category" : category}))
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * ITEMS_PER_PAGE
            end = start + ITEMS_PER_PAGE
            total_pages = ceil(len(items) / ITEMS_PER_PAGE)
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category=category, is_admin=True, user_id=user_id)
        else:
            items = list(client.cengdendb.items.find({"is_active": True, "category": category}))
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * ITEMS_PER_PAGE
            end = start + ITEMS_PER_PAGE
            total_pages = ceil(len(items) / ITEMS_PER_PAGE)
            return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True, category=category, is_admin=False, user_id=user_id)
    else:
        items = list(client.cengdendb.items.find({"is_active": True, "category": category}))
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        total_pages = ceil(len(items) / ITEMS_PER_PAGE)
        return render_template('index.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=False, category=category, is_admin=False, user_id=False)


#This is the route for item details page. It is accessible by everyone.
@app.route('/item/<string:item_id>')
def item_detail(item_id):
    item  = client.cengdendb.items.find_one({"_id" : ObjectId(item_id)})
    owner_email = client.cengdendb.users.find_one({"_id": item['owner_id']})['email']
    owner_phone = client.cengdendb.users.find_one({"_id": item['owner_id']})['phone']
    owner_is_public = client.cengdendb.users.find_one({"_id": item['owner_id']})['profile_visibility']
    if item:
        if 'user' in session:
            if session['user']['userinfo']['sub'] == item['owner_id']:
                return render_template('item-details.html', item=item, is_owner=True, signed_in=True, is_admin=False, owner_email=owner_email, owner_phone=owner_phone)
            elif session['user']['userinfo']['user_metadata']['is_admin']:
                return render_template('item-details.html', item=item, is_owner=False, signed_in=True, is_admin=True, owner_email=owner_email, owner_phone=owner_phone)
            else:
                return render_template('item-details.html', item=item, is_owner=False, signed_in=True, is_admin=False, owner_email=owner_email, owner_phone=owner_phone)
        elif owner_is_public == 'public':
            return render_template('item-details.html', item=item, is_owner=False, signed_in=False, is_admin=False, owner_email=owner_email, owner_phone=owner_phone)
        else:
            return render_template('item-details.html', item=item, is_owner=False, signed_in=False, is_admin=False)
    else:
        return "Item not found", 404

#This is the route for editing an item. It is only accessible by the owner of the item.
@app.route('/item/<string:item_id>', methods=['POST'])
def item_detail_submit(item_id):
    #Get the form inputs and put them into mongodb to update the existing item
    form_fields = {}
    empty_items = {}
    for key in request.form:
        value = request.form[key]
        if value is not None and value != "":
            form_fields[key] = value  # Adding non-empty items to form_fields
        else:
            empty_items[key] = value  # Adding empty items to empty_items
    client.cengdendb.items.update_one({"_id": ObjectId(item_id)}, {"$set": form_fields})
    client.cengdendb.items.update_one({"_id": ObjectId(item_id)}, {"$unset": empty_items})
    return redirect('/item/' + item_id)

#This is the route for profile page. It is only accessible by the owner of the profile.
@app.route('/profile')
def profile():
    user_id = session['user']['userinfo']['sub']
    user_details = client.cengdendb.users.find_one({"_id": user_id})
    if 'user' in session:
        return render_template('profile.html', user=user_details, signed_in=True)
    else:
        return redirect(url_for('login'))

@app.route('/profile', methods=['GET','POST'])
def profile_submit():
    user_id = session['user']['userinfo']['sub']
    if request.form['password']:
        update_user_password(user_id, request.form['password'])
    form_fields = {}
    for key in request.form:
        if key == 'password':
            continue
        form_fields[key] = request.form[key]
    form_fields = {k: v for k, v in form_fields.items() if v is not None and v != ""}
    client.cengdendb.users.update_one({"_id": user_id}, {"$set": form_fields})
    return redirect('/profile')


@app.route("/add-item")
def add_item():
    return render_template('add-item.html', signed_in=True)

# Route for handling form submission and adding item to MongoDB
@app.route("/add-item", methods=["POST"])
def handle_add_item():
    form_fields = {}
    form_fields["owner_id"] = client.cengdendb.users.find_one({"email": session.get('user')["userinfo"]["email"]})["_id"]
    form_fields["favorites"] = []
    form_fields["is_active"] = True  

    if(request.form.get("category") == "phones"):
        form_fields["camera-specifications"] = {}
        for key in request.form:
            if key.startswith("camera_specs_"):
                #Split the key to get the camera_specs_ part and the key part
                key_parts = key.split("_", 2)[2]
                form_fields["camera-specifications"][key_parts] = request.form[key]
            else:
                form_fields[key] = request.form[key]

    elif(request.form.get("category") == "computers"):
        form_fields["storage"] = {}
        for key in request.form:
            if key.startswith("storage_"):
                #Split the key to get the storage_ part and the key part
                key_parts = key.split("_", 1)[1]
                form_fields["storage"][key_parts] = request.form[key]
            else:
                form_fields[key] = request.form[key]
    
    elif(request.form.get("category") == "private-lessons"):
        form_fields["lessons"] = []
        for key in request.form:
            if key == 'lessons':
                form_fields[key] = request.form[key].split(",")
            else:
                form_fields[key] = request.form[key]
    
    else:
        for key in request.form:
            form_fields[key] = request.form[key]

    form_fields = {k: v for k, v in form_fields.items() if v is not None and v != ""}

    try:

        client.cengdendb.items.insert_one(form_fields)
        message = "Item added successfully!"
    except Exception as e:
        message = "An error occurred, please try again."

    return redirect('/users-items')

#This is the route for users items page. It is only accessible by the owner of the items.
@app.route("/users-items")
def users_items():
    user_id = session['user']['userinfo']['sub']
    items = list(client.cengdendb.items.find({"owner_id": user_id}))
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)
    return render_template('users-items.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True)

#This is the route for deleting an item. It is only accessible by the owner of the item and the admin.
@app.route("/delete-item/<string:item_id>" , methods=["POST"])
def delete_item(item_id):
    #Remove item id from the user fav list if it is in there
    item_fav_list = client.cengdendb.items.find_one({"_id": ObjectId(item_id)})["favorites"]
    for user_id in item_fav_list:
        client.cengdendb.users.update_one({"_id": user_id}, {"$pull": {"favorites": ObjectId(item_id)}})
    client.cengdendb.items.delete_one({"_id": ObjectId(item_id)})
    if session['user']['userinfo']['user_metadata']['is_admin']:
        return redirect('/')
    else:
        return redirect('/users-items')

@app.route("/toggle-active/<string:item_id>", methods=["POST"])
def toggle_active(item_id):
    item = client.cengdendb.items.find_one({"_id": ObjectId(item_id)})
    client.cengdendb.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"is_active": not item["is_active"]}})
    return redirect('/users-items')

#This is the route for favorites page. It is only accessible by the users.
@app.route("/favorites")
def favorites():
    user_id = session['user']['userinfo']['sub']
    user = client.cengdendb.users.find_one({"_id": user_id})
    items = list(client.cengdendb.items.find({"_id": {"$in": user["favorites"]}}))
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    total_pages = ceil(len(items) / ITEMS_PER_PAGE)
    return render_template('favorites.html', items=items[start:end], page=page, total_pages=total_pages, signed_in=True)

@app.route("/toggle-favorites/<string:item_id>", methods=["POST"])
def toggle_favorites(item_id):
    user_id = session['user']['userinfo']['sub']
    item = client.cengdendb.items.find_one({"_id": ObjectId(item_id)})
    user = client.cengdendb.users.find_one({"_id": user_id})
    if item["_id"] in user["favorites"]:
        client.cengdendb.users.update_one({"_id": user_id}, {"$pull": {"favorites": item["_id"]}})
        client.cengdendb.items.update_one({"_id": item["_id"]}, {"$pull": {"favorites": user_id}})
    else:
        client.cengdendb.users.update_one({"_id": user_id}, {"$push": {"favorites": item["_id"]}})
        client.cengdendb.items.update_one({"_id": item["_id"]}, {"$push": {"favorites": user_id}})
    return redirect('/')

#This is the route for all users page. It is only accessible by admins.
@app.route("/all-users")
def all_users():
    users = list(client.cengdendb.users.find())
    if 'user' in session:
        if session['user']['userinfo']['user_metadata']['is_admin']:
            return render_template('all-users.html', users=users, is_owner=True, signed_in=True, is_admin=True)
        else:
            return redirect(url_for('home'))

@app.route("/delete-user/<string:user_id>", methods=["POST"])
def delete_user_submit(user_id):
    #delete all items of the user
    items = list(client.cengdendb.items.find({"owner_id": user_id}))
    for item in items:
        #Delete the itesm from users fav lists
        for user_id in item["favorites"]:
            client.cengdendb.users.update_one({"_id": user_id}, {"$pull": {"favorites": item["_id"]}})
        client.cengdendb.items.delete_one({"_id": item["_id"]})
    delete_user(user_id)
    client.cengdendb.users.delete_one({"_id": user_id})
    return redirect('/all-users')

#This part is for handle authenticaotin with Auth0.
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
    user_data = {"_id": user_id, "name": user_name, "email": user_email , "phone": user_phone, "is_public": True, "favorites": []}
    if not client.cengdendb.users.find_one({"_id": user_id}):
        client.cengdendb.users.insert_one(user_data)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect('https://' + AUTH0_DOMAIN + '/v2/logout?' + urlencode(params, quote_via=quote_plus))

if __name__ == '__main__':
    app.run(debug=True)
