"""This module updates product prices in the delivery database."""

from tkinter import (Tk, Frame, Button, Entry, Label, END)
from sqlite3 import connect

class Application(Frame):
    """Creates the application window."""

    def __init__(self, master):
        super().__init__(master)
        self.grid()

        # Retrieve product data from delivery database.
        self.conn = connect("delivery.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT prod_name, price FROM products")
        self.row = self.cursor.fetchall()

        self.prices, self.products = [], []
        for row in self.row:
            self.products.append(row[0])
            self.prices.append(row[1])

        self.create_widgets()

    def create_widgets(self):
        """Create interactive widgets."""
        self.lbl_prod, self.ent_price = {}, {}

        row = 1
        self.lbl_col1 = Label(self, text="Product")
        self.lbl_col1.grid(row=row, column=0, sticky="W")
        self.lbl_col2 = Label(self, text="Price")
        self.lbl_col2.grid(row=row, column=1, sticky="W")

        # Name and entry fields for each product.
        for i in range(len(self.products)):
            row += 1
            self.lbl_prod[i] = Label(self, text=self.products[i])
            self.ent_price[i] = Entry(self, width=5)

            self.lbl_prod[i].grid(row=row, column=0, sticky="W")
            self.ent_price[i].grid(row=row, column=1, sticky="W")
            self.ent_price[i].insert(END, self.prices[i])

        self.lbl_empty = Label(self, text="")
        self.lbl_empty.grid(row=row, column=0)

        row += 1
        self.btn_update = Button(self, text="Update prices",
                                 command=self.update)
        self.btn_update.grid(row=row, column=0, sticky="W")

        self.ent_update = Entry(self, width=10)
        self.ent_update.grid(row=row, column=1)

    def update(self):
        for i in range(len(self.products)):
            self.prices[i] = self.ent_price[i].get()
            query = """
                    UPDATE products
                    SET price = ?
                    WHERE prod_name = ?
                    """
            vals = (self.prices[i], self.products[i])
            self.cursor.execute(query, vals)
            self.conn.commit()

        self.conn.close()
        self.ent_update.delete(0, END)
        self.ent_update.insert(END, "Updated!")

window = Tk()
window.title("Wood Prices Updater")
window.geometry("450x300")
app = Application(window)
app.mainloop()