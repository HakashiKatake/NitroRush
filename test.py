import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://I4cqvSIL5f0uP5Ls:saurabhyadav9850@nitrorush.w3tg202.mongodb.net/?retryWrites=true&w=majority")
db = cluster["SecureDb"]
collection = db["value storage"]

post = {"_id": 0, "coins": 200, "score": 1000}

collection.insert_one(post)