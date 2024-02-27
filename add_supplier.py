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
    name = input('Enter supplier name: ')
    contact = input('Enter supplier contact: ')
    phone = input('Enter supplier phone: ')
    db.supplier.insert_one({'name': name, 'description': contact, 'phone': phone})

except Exception as e:
    print(e)

finally:
    if client is not None:
        client.close()
