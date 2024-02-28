from flask import Flask, render_template
from pymongo import MongoClient
from bson import ObjectId
from db_config import MONGO_URI

app = Flask(__name__)

@app.route('/')
def index():
    client = MongoClient(MONGO_URI)
    db = client.inventory
    try:
        # Sort items by '_id' in descending order and limit to 5
        items_cursor = db.item.find().sort('_id', -1).limit(5)
        items = list(items_cursor)

        # Sort categories by '_id' in descending order and limit to 5
        categories_cursor = db.category.find().sort('_id', -1).limit(5)
        categories = list(categories_cursor)

        # Sort suppliers by '_id' in descending order and limit to 5
        suppliers_cursor = db.supplier.find().sort('_id', -1).limit(5)
        suppliers = list(suppliers_cursor)

        return render_template('index.html', items=items, categories=categories, suppliers=suppliers)
    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__ == '__main__':
    app.run(debug=True)
