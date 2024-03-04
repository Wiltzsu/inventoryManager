Project Documentation

Overview
This project is an inventory management system developed using Flask, a Python web framework, and MongoDB, a NoSQL database. It facilitates the management of items, categories, and suppliers through a user-friendly web interface.

System Requirements
  Python 3.x
  Flask
  MongoDB
  pip (Python package manager)

Installation

Setting Up the Environment
  Install Python 3.x: Ensure Python 3.x is installed on your system. It can be downloaded from python.org.
  
  Install MongoDB: Follow the MongoDB official documentation to install MongoDB on your system. MongoDB documentation can be found at docs.mongodb.com/manual/installation/.

Create and Activate a Virtual Environment (recommended):
Create a virtual environment:

  python -m venv venv
  Activate the virtual environment:
  
  Windows: venv\Scripts\activate
  macOS/Linux: source venv/bin/activate
  
Install Required Python Packages:

Install Flask and PyMongo using pip:

  pip install Flask pymongo
  Configuring MongoDB to Use Localhost
  MongoDB, by default, runs on localhost (127.0.0.1) on port 27017. If MongoDB is installed on your local machine, it should be ready to use without further configuration.

  Ensure the MongoDB service is started on your machine.

Application Configuration
  Configure the application to connect to your local MongoDB instance:
  
  MONGO_URI = "mongodb://127.0.0.1:27017/your_database_name"
  Replace your_database_name with the actual name of your MongoDB database.

Running the Application
  To run the application, navigate to the project directory in your terminal and execute:

  python app.py
  The Flask application will start and be accessible at http://localhost:5000.

Using the Application
  Accessing the Dashboard
  To access the dashboard, open a web browser and go to http://localhost:5000.

Managing Inventory
  Viewing Items: Click "Items" in the navigation menu to see a list of items.
  Adding an Item: Navigate to the "Add Item" form, fill it out, and submit it to add a new item.
  Updating an Item: Next to each item, there's an "Update" button—click it to edit item details.
  Deleting Items: Select one or more items and choose "Delete Selected" to remove them from the inventory.
