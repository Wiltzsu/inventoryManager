from bson import ObjectId
from pymongo import MongoClient
from db_config import MONGO_URI  # Import the connection string

client = None
db = None

try:
    # Connect to the MongoDB server using the URI from db_config.py
    client = MongoClient(MONGO_URI)
    # Select the database. If it doesn't exist, create it on first document insertion
    db = client.inventory

    _id = input("Enter category id: ")

    # Find the category with the given id and convert the string input to an ObjectId
    category = db.category.delete_one({"_id": ObjectId(_id)})
    # If the category doesn't exist, raise an exception
    if category.deleted_count == 0:
        raise Exception("Category does not exist")

    # Also deletes all items with the same ObjectId
    db.item.delete_many({'categoryId': ObjectId(_id)})

except Exception as e:
    print(e)

finally:
    if client is not None:
        client.close()
