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

# Define a route for the endpoint '/items' that will display the items in the inventory.
@app.route('/items')
def show_items():
    client = MongoClient(MONGO_URI)
    db = client.inventory
    try:
        # Query the 'item' collection in the database to find all documents (items),
        # sort them in descending order by their '_id' to show the newest items first.
        items_cursor = db.item.find().sort('_id', -1)
        # Convert the cursor returned by the find() method into a list of items.
        items = list(items_cursor)
    except Exception as e:
        print(e)
        items = []  # Provide an empty list in case of an error
    finally:
        client.close()

    return render_template('items.html', items=items)


# Route for deleting an item
@app.route('/delete-items', methods=['POST'])
def delete_items():
    # Retrieve a list of item IDs to delete from the form
    item_ids_to_delete = request.form.getlist('item_ids')

    client = MongoClient(MONGO_URI)
    db = client.inventory

    try:
        #Convert string IDs to ObjectId and delete items from the database
        for item_id in item_ids_to_delete:
            db.item.delete_one({'_id': ObjectId(item_id)})
        # Redirect to the items list page after deletion
        return redirect(url_for('show_items'))
    except Exception as e:
        print(e)
    finally:
        client.close()

# Route for adding an item, which accepts GET and POST requests
@app.route('/add-item', methods=['GET', 'POST'])
def add_item():
    # Check if current request is a POST requests (form submission)
    if request.method == 'POST':
        try:
            client = MongoClient(MONGO_URI) # Establish database connection
            db = client.inventory # Access 'inventory' database

            # Create a new item document from the form data
            new_item = {
                'name': request.form['name'],
                'description': request.form['description'],
                'quantity': int(request.form['quantity']),
                'categoryId': request.form['categoryId'],
                'supplierId': request.form['supplierId']
            }

            # Insert the new item into the database
            db.item.insert_one(new_item)

            # Redirect to a different page, e.g., the list of items, on success
            return redirect(url_for('show_items'))
        except Exception as e:
            print(e)
            # Handle the error, possibly showing a user-friendly message
        finally:
            client.close()
    # If it's a GET request, just render the empty form
    return render_template('add_item.html')


if __name__ == '__main__':
    app.run(debug=True)
