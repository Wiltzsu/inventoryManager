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

    # Ask user for category and description and add them to the database
    name = input('Enter item name: ')
    description = input('Enter item description: ')
    quantity = input('Enter quantity: ')
    categoryName = input('Enter category name: ')
    supplierName = input('Enter supplier name: ')

    # If no document for the category is found, an exception is raised to indicate there is no such category
    category = db.category.find_one({'category': categoryName})
    if category is None:
        raise Exception("No such category")

    # If no document for the supplier is found, an exception is raised to indicate there is no such supplier
    supplier = db.supplier.find_one({'name': supplierName})
    if supplier is None:
        raise Exception("No such supplier")

    # Converts the category's '_id' value to an ObjectId.
    # This is necessary because MongoDB uses ObjectId as the default type for unique identifier fields
    category_id = ObjectId(category['_id'])

    # Same process for supplier id
    supplier_id = ObjectId(supplier['_id'])

    db.item.insert_one({'name': name, 'description': description, 'quantity': quantity, 'categoryId': category_id, 'supplierId': supplier_id})

except Exception as e:
    print(e)

finally:
    if client is not None:
        client.close()
