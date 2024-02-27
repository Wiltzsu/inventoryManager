from pymongo import MongoClient
from db_config import MONGO_URI  # Import the connection string

client = None
db = None

try:
    # Connect to the MongoDB server using the URI from db_config.py
    client = MongoClient(MONGO_URI)
    # Select the database. If it doesn't exist, create it on first document insertion
    db = client.inventory

    suppliers = db.supplier.find()

    # Print out each supplier
    for supplier in suppliers:
        print(supplier['_id'], supplier['name'], supplier['description'], supplier['phone'])

except Exception as e:
    print(e)

finally:
    if client is not None:
        client.close()
