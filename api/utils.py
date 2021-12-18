from pymongo import MongoClient

def get_db():
    return MongoClient('localhost', 27017).roles

