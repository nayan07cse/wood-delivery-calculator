"""This module tests two API endpoints from the WDC service."""

from unittest import TestCase
from wdc_service.get_wdc_data import GetWDCData
from sqlite3 import connect

conn = connect("delivery.db")
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM products")
row_count = int(cursor.fetchone()[0])
conn.close()

class TestGetWDCData(TestCase):
    def test_get_products(self):
        self.assertEqual(len(GetWDCData.get_products()), row_count)

    def test_get_prices(self):
        self.assertEqual(len(GetWDCData.get_prices()), row_count)
