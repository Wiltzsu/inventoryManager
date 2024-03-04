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

@app.route('/categories')
def show_categories():
    client = MongoClient(MONGO_URI)
    db = client.inventory
    try:
        # Query the 'category' collection in the database to find all documents (categories),
        # sort them in descending order by their '_id' to show the newest items first.
        category_cursor = db.category.find().sort('_id', -1)
        # Convert the cursor returned by the find() method into a list of items.
        categories = list(category_cursor)
    except Exception as e:
        print(e)
        categories = []  # Provide an empty list in case of an error
    finally:
        client.close()

    return render_template('categories.html', categories=categories)

@app.route('/suppliers')
def show_suppliers():
    client = MongoClient(MONGO_URI)
    db = client.inventory
    try:
        # Query the 'supplier' collection in the database to find all documents (suppliers),
        # sort them in descending order by their '_id' to show the newest items first.
        suppliers_cursor = db.supplier.find().sort('_id', -1)
        # Convert the cursor returned by the find() method into a list of items.
        suppliers = list(suppliers_cursor)
    except Exception as e:
        print(e)
        suppliers = []  # Provide an empty list in case of an error
    finally:
        client.close()

    return render_template('suppliers.html', suppliers=suppliers)

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

# Route for deleting categories
@app.route('/delete-categories', methods=['POST'])
def delete_categories():
    # Retrieve a list of category IDs to delete from the form
    category_ids_to_delete = request.form.getlist('category_ids')

    client = MongoClient(MONGO_URI)
    db = client.inventory

    try:
        #Convert string IDs to ObjectId and delete categories from the database
        for category_id in category_ids_to_delete:
            db.category.delete_one({'_id': ObjectId(category_id)})
        # Redirect to the items list page after deletion
        return redirect(url_for('show_categories'))
    except Exception as e:
        print(e)
    finally:
        client.close()

# Route for deleting suppliers
@app.route('/delete-suppliers', methods=['POST'])
def delete_suppliers():
    # Retrieve a list of supplier IDs to delete from the form
    supplier_ids_to_delete = request.form.getlist('supplier_ids')

    client = MongoClient(MONGO_URI)
    db = client.inventory

    try:
        #Convert string IDs to ObjectId and delete suppliers from the database
        for supplier_id in supplier_ids_to_delete:
            db.supplier.delete_one({'_id': ObjectId(supplier_id)})
        # Redirect to the items list page after deletion
        return redirect(url_for('show_suppliers'))
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

# Route for adding a category, which accepts GET and POST requests
@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    # Check if current request is a POST requests (form submission)
    if request.method == 'POST':
        try:
            client = MongoClient(MONGO_URI) # Establish database connection
            db = client.inventory # Access 'inventory' database

            # Create a new category document from the form data
            new_category = {
                'category': request.form['category'],
                'description': request.form['description'],
            }

            # Insert the new item into the database
            db.category.insert_one(new_category)

            # Redirect to page with all categories
            return redirect(url_for('show_categories'))
        except Exception as e:
            print(e)
            # Handle the error, possibly showing a user-friendly message
        finally:
            client.close()
    # If it's a GET request, just render the empty form
    return render_template('add_category.html')

# Route for adding a supplier, which accepts GET and POST requests
@app.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    # Check if current request is a POST requests (form submission)
    if request.method == 'POST':
        try:
            client = MongoClient(MONGO_URI) # Establish database connection
            db = client.inventory # Access 'inventory' database

            # Create a new supplier document from the form data
            new_supplier = {
                'name': request.form['name'],
                'contact': request.form['contact'],
                'phone': request.form['phone']
            }

            # Insert the new item into the database
            db.supplier.insert_one(new_supplier)

            # Redirect to page with all suppliers
            return redirect(url_for('show_suppliers'))
        except Exception as e:
            print(e)
            # Handle the error, possibly showing a user-friendly message
        finally:
            client.close()
    # If it's a GET request, just render the empty form
    return render_template('add_supplier.html')

# Route for updating items
@app.route('/update-item/<item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    client = MongoClient(MONGO_URI)
    db = client.inventory

    # If it's a POST request, process the form data
    if request.method == 'POST':
        try:
            # Prepare the update data
            update_data = {
                'name': request.form['name'],
                'description': request.form['description'],
                'quantity': int(request.form['quantity']),
                'categoryId': request.form['categoryId'],
                'supplierId': request.form['supplierId']
            }

            # Find the item by ID and update it with the new data
            db.item.update_one({'_id': ObjectId(item_id)}, {'$set': update_data})
            return redirect(url_for('show_items'))

        except Exception as e:
            print(e)
        finally:
            client.close()

    else:
        # If it's a GET request, find the item by ID and render the form with the item's current data
        try:
            item_to_update = db.item.find_one({'_id': ObjectId(item_id)})
        except Exception as e:
            print(e)
            item_to_update = None
        finally:
            client.close()

        return render_template('update_item.html', item=item_to_update)

    return redirect(url_for('show_items'))

# Route for updating categories
@app.route('/update-category/<category_id>', methods=['GET', 'POST'])
def update_category(category_id):
    client = MongoClient(MONGO_URI)
    db = client.inventory

    # If it's a POST request, process the form data
    if request.method == 'POST':
        try:
            # Prepare the update data
            update_data = {
                'category': request.form['category'],
                'description': request.form['description'],
            }

            # Find the item by ID and update it with the new data
            db.category.update_one({'_id': ObjectId(category_id)}, {'$set': update_data})
            return redirect(url_for('show_categories'))

        except Exception as e:
            print(e)
        finally:
            client.close()

    else:
        # If it's a GET request, find the category by ID and render the form with the category's current data
        try:
            category_to_update = db.category.find_one({'_id': ObjectId(category_id)})
        except Exception as e:
            print(e)
            category_to_update = None
        finally:
            client.close()

        return render_template('update_category.html', category=category_to_update)

    return redirect(url_for('show_items'))

# Route for updating suppliers
@app.route('/update-supplier/<supplier_id>', methods=['GET', 'POST'])
def update_supplier(supplier_id):
    client = MongoClient(MONGO_URI)
    db = client.inventory

    # If it's a POST request, process the form data
    if request.method == 'POST':
        try:
            # Prepare the update data
            update_data = {
                'name': request.form['name'],
                'contact': request.form['contact'],
                'phone': request.form['phone']
            }

            # Find the item by ID and update it with the new data
            db.supplier.update_one({'_id': ObjectId(supplier_id)}, {'$set': update_data})
            return redirect(url_for('show_suppliers'))

        except Exception as e:
            print(e)
        finally:
            client.close()

    else:
        # If it's a GET request, find the category by ID and render the form with the category's current data
        try:
            supplier_to_update = db.supplier.find_one({'_id': ObjectId(supplier_id)})
        except Exception as e:
            print(e)
            supplier_to_update = None
        finally:
            client.close()

        return render_template('update_supplier.html', supplier=supplier_to_update)

    return redirect(url_for('show_suppliers'))

if __name__ == '__main__':
    app.run(debug=True)
