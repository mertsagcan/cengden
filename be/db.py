# External dependencies
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://mertsagcan:QSd1qTO6ETj2ETKy@cengdendb.sznqoxa.mongodb.net/?retryWrites=true&w=majority&appName=cengdendb"

class DB:
    def __init__(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['cengdendb']
        self.users = self.db['users']
        self.items = self.db['items']
        

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)