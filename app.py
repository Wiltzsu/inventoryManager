from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/items')
def show_items():
    client = MongoClient(MONGO_URI)
    db = client.inventory
    try:
        items_cursor = db.item.find().sort('_id', -1)
        items = list(items_cursor)
    except Exception as e:
        print(e)
        items = []  # Provide an empty list in case of an error
    finally:
        client.close()

    return render_template('items.html', items=items)


@app.route('/bulk-action', methods=['POST'])
def handle_bulk_action():
    action = request.form.get('action')
    item_ids = request.form.getlist('item_ids')  # Get list of selected item IDs

    if action == 'delete':
        try:
            client = MongoClient(MONGO_URI)
            db = client.inventory
            for item_id in item_ids:
                db.item.delete_one({'_id': ObjectId(item_id)})
        except Exception as e:
            print(e)
        finally:
            client.close()

    # Redirect back to the items list or handle other actions accordingly
    return redirect(url_for('show_items'))


if __name__ == '__main__':
    app.run(debug=True)
