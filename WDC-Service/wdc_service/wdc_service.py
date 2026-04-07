"""This module provides various services to the
Wood Delivery Calculator client app using the delivery database."""

from sqlite3 import connect
from decimal import Decimal
from datetime import date
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

# Create the Flask app and API objects.
app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
user_data = {"client": "Pa22w0rd"}

class Products(Resource):
    """Gets product data from products table."""

    @auth.verify_password
    def verify(username, password):
        if username in user_data and user_data[username] == password:
            return username
    @auth.login_required

    def get(self):
        """Get product data."""
        self.conn = connect("delivery.db")
        self.cursor = self.conn.cursor()

        self.products = []
        self.cursor.execute("SELECT prod_name FROM products")
        self.row = self.cursor.fetchall()
        for row in self.row:
            self.products.append(row[0])
        self.conn.close()

        return jsonify({"products": self.products})

class Prices(Resource):
    """Gets prices data from products table."""

    def get(self):
        """Get prices data."""
        self.conn = connect("delivery.db")
        self.cursor = self.conn.cursor()

        self.prices = []
        self.cursor.execute("SELECT price FROM products")
        self.row = self.cursor.fetchall()
        for row in self.row:
            self.prices.append(Decimal(row[0]))
        self.conn.close()

        self.prices_str = [str(price) for price in self.prices]
        return jsonify({"prices": self.prices_str})

class Submit(Resource):
    """Inserts order data into orders table."""

    def post(self):
        post_ship = request.json.get("ship")
        post_total = request.json.get("total")

        self.conn = connect("delivery.db")
        self.cursor = self.conn.cursor()

        query = """
                INSERT INTO orders
                (order_date, ship_method, total_price)
                VALUES (?, ?, ?)
                """
        today = date.today()
        vals = (today.isoformat(), post_ship, post_total)

        self.cursor.execute(query, vals)
        self.conn.commit()
        self.conn.close()

        return jsonify(self.cursor.lastrowid)

# Add the resource endpoints.
api.add_resource(Products, "/products")
api.add_resource(Prices, "/prices")
api.add_resource(Submit, "/submit")

app.run()