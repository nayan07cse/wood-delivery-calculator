"""This module retrieves product and price info
from the WDC web service."""

import requests
import json

class GetWDCData:
    """Retrieves product and price info."""

    @classmethod
    def get_products(cls):
        """Get product data from web service."""
        get_prod_names = requests.get("http://127.0.0.1:5000/products",
                                      auth=('client', 'Pa22w0rd'))

        if get_prod_names.status_code == 401:
            print(f"401 {get_prod_names.text}")
            exit()

        tmp_prod_names = json.loads(get_prod_names.text)
        products = tmp_prod_names["products"]
        return products

    @classmethod
    def get_prices(cls):
        """Get price data from web service."""
        get_prices = requests.get("http://127.0.0.1:5000/prices")
        tmp_prices = json.loads(get_prices.text)
        prices = tmp_prices["prices"]
        return prices


