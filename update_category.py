from pymongo import MongoClient
from bson import ObjectId
import sys

from db_config import MONGO_URI

client = None
db = None

try:
    # Connect to the MongoDB server using the URI from db_config.py
    client = MongoClient(MONGO_URI)
    # Select the database. If it doesn't exist, it will be created on first document insertion
    db = client.inventory

    _id = input("Enter the category's ID to update: ")
    object_id = ObjectId(_id)  # Convert the input ID to an ObjectId

    # Prompt the user for the new values
    new_category = input("Enter new category name: ")
    new_description = input("Enter new description: ")


    # Construct the update document
    update_doc = {
        "$set": {
            "category": new_category,
            "description": new_description
        }
    }

    # Perform the update operation
    update_result = db.category.update_one({"_id": object_id}, update_doc)

    # If there is no item with the inserted id print error
    if update_result.matched_count == 0:
        print("No categories matched the given ID.")
    # If the id was found but item not modified
    elif update_result.modified_count == 0:
        print("The category was matched but not modified.")
    else:
        print("Category updated successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    if client:  # Only attempt to close the client if it's not None
        client.close()
