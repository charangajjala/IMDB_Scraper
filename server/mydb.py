import pymongo
from dotenv import load_dotenv
import os

load_dotenv()


class MyDB:
    _DB_NAME = "IMDB_Db"
    _Reviews_COLLECTION_NAME = "IMDB_Reviews"
    _BasicDetials_COLLECTION_NAME = "IMDB_BasicDetials"

    def __init__(self):
        db = self.give_db()
        self._basic_details_collection = self.give_collection(
            db, MyDB._BasicDetials_COLLECTION_NAME
        )
        self._reviews_collection = self.give_collection(
            db, MyDB._Reviews_COLLECTION_NAME
        )

    def give_client(self):
        print(os.environ.get("db_connection_url"))
        client = pymongo.MongoClient(os.environ.get("db_connection_url"))
        return client

    def give_db(self):
        client = self.give_client()
        db = None
        if MyDB._DB_NAME in client.list_database_names():
            # databse already exists
            db = client[MyDB._DB_NAME]
        else:
            # create a new database
            db = client[MyDB._DB_NAME]
        return db

    def give_collection(self, db, collection_name):

        collection = None
        if collection_name in db.list_collection_names():
            # collection exists in database
            collection = db[collection_name]
        else:
            # create new collection
            collection = db[collection_name]
        return collection

    @property
    def basic_details(self):
        return self._basic_details_collection

    @property
    def reviews(self):
        return self._reviews_collection

    def handle_basic_details(self, title, basic_details=None):
        details = self._basic_details_collection.find_one({"title": title},{"_id":0})
        if basic_details is not None:
            self._basic_details_collection.insert_one(basic_details)
        else:
            return details

    def save_reviews(self, title, parsed_reviews):
        collection = self._reviews_collection
        collection.update_one({"title": title}, {"$set": {"reviews": parsed_reviews}})

    def get_reviews(self, title, num_reviews):
        num = int(num_reviews)
        collection = self._reviews_collection
        existing_reviews = collection.find({"title": title},{"reviews._id":0},{"reviews":{"$slice":num}})   
        if len(existing_reviews) < num_reviews:
            return None
        return existing_reviews['reviews']