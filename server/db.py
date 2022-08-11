import pymongo

class MyMongoDB:
    _DB_NAME = "IMDB_Db"
    _Reviews_COLLECTION_NAME = "IMDB_Reviews"
    _BasicDetials_COLLECTION_NAME = "IMDB_BasicDetials"
   

    def __init__(self):
        db = self.get_db()
        self._basic_details_collection = db.get_collection(db, MyMongoDB._BasicDetials_COLLECTION_NAME)
        self._reviews_collection = db.get_collection(db, MyMongoDB._Reviews_COLLECTION_NAME)
    
    def get_client(self):
        client = pymongo.MongoClient("url")
        return client

    
    def get_db(self):
        client = self.get_client()
        db = None
        if MyMongoDB._DB_NAME in client.list_database_names():
            # databse already exists
            db = client[MyMongoDB._DB_NAME]
        else:
            # create a new database
            db = client[MyMongoDB._DB_NAME]
        client.close()
        return db

    
    def get_collection(self, db, collection_name):    

        collection = None
        if collection_name in db.list_collection_names():
            # collection exists in database
            collection = db[collection_name]
        else:
            #create new collection
            collection = db[collection_name]
        return collection

    @property
    def basic_details(self):
        return self._basic_details_collection

    @property
    def reviews(self):
        return self._reviews_collection





