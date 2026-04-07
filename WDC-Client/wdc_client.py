"""This module creates an interface for ordering
products from Woodworkers Wheelhouse."""

import requests
import json
from decimal import Decimal
from tkinter import (Tk, Frame, Button, Entry, Label,
                     Menu, Radiobutton, StringVar, END)

class Application(Frame):
    """Creates the application window."""

    def __init__(self, master):
        """Construct class instance with product data."""
        super().__init__(master)
        self.total = 0
        self.grid()
        self.products, self.prices = [], []
        self.ship_days = {"1 day": 20.00, "2 days": 15.00, "3 days": 10.00}

        get_prod_names = requests.get("http://127.0.0.1:5000/products",
                                      auth=("client", "Pa22w0rd"))

        if get_prod_names.status_code == 401:
            print(f"401 {get_prod_names.text}")
            exit()

        tmp_prod_names = json.loads(get_prod_names.text)
        self.products = tmp_prod_names["products"]

        get_prices = requests.get("http://127.0.0.1:5000/prices")
        tmp_prices = json.loads(get_prices.text)
        self.prices = [Decimal(price) for price in tmp_prices["prices"]]

        self.create_widgets()

    def create_widgets(self):
        """Create interactive widgets."""
        row = 1
        self.lbl_head = Label(self, text="Order Wood Products:")
        self.lbl_head.grid(row=row, column=1, sticky="W")

        self.lbl_prod, self.lbl_price, self.ent_quant = {}, {}, {}

        for i in range(len(self.products)):
            row += 1
            self.lbl_prod[i] = Label(self, text=self.products[i])
            self.lbl_price[i] = Label(self, text=f"{self.prices[i]:.2f}")
            self.ent_quant[i] = Entry(self, width=3)

            self.ent_quant[i].grid(row=row, column=0)
            self.lbl_prod[i].grid(row=row, column=1, sticky="W")
            self.lbl_price[i].grid(row=row, column=2, sticky="W")

        self.lbl_ship = Label(self, text="Shipping:")
        row += 1
        self.lbl_ship.grid(row=row, column=0, sticky="W")

        self.str_ship = StringVar()
        row += 1

        self.rad_one = Radiobutton(self, text="1 day",
                                   variable=self.str_ship, value="1 day")
        self.rad_one.grid(row=row, column=0, sticky="W")
        self.rad_one.select()

        self.rad_two = Radiobutton(self, text="2 days",
                                   variable=self.str_ship, value="2 days")
        self.rad_two.grid(row=row, column=1)

        self.rad_three = Radiobutton(self, text="3 days",
                                     variable=self.str_ship, value="3 days")
        self.rad_three.grid(row=row, column=2, sticky="W")

        row += 1
        self.btn_reset = Button(self, text="Reset",
                                command=self.reset)
        self.btn_reset.grid(row=row, column=0)
        self.btn_calc = Button(self, text="Calculate Price",
                               command=self.calculate)
        self.btn_calc.grid(row=row, column=1)

        row += 1
        self.lbl_empty = Label(self, text="")
        self.lbl_empty.grid(row=row, column=0)

        row += 1
        self.lbl_total = Label(self, text="Total:")
        self.lbl_total.grid(row=row, column=0, sticky="E")
        self.ent_result = Entry(self, width=10)
        self.ent_result.grid(row=row, column=1, sticky="W")

        row += 1
        self.str_submit = StringVar()
        self.btn_submit = Button(self, text="Submit Order",
                                 command=self.submit)
        self.btn_submit.grid(row=row, column=0)
        self.lbl_result = Label(self, textvariable=self.str_submit)
        self.lbl_result.grid(row=row, column=1, sticky="W")

        menu_bar = Menu(self)
        file_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_command(label="Quit", command=window.quit)

        file_menu.add_command(label="Reset", command=self.reset)
        file_menu.add_command(label="Calculate Price", command=self.calculate)
        window.config(menu=menu_bar)

    def reset(self):
        """Reset shipping options and quantity entries."""
        self.rad_one.select()
        for i in range(len(self.products)):
           self.ent_quant[i].delete(0, END)

        self.ent_result.delete(0, END)

    def calculate(self):
        """Calculate the total amount of the order."""
        self.total = 0
        self.qty = 0
        for i in range(len(self.products)):
            if self.ent_quant[i].get():
                try:
                    int(self.ent_quant[i].get())
                except ValueError:
                    self.str_submit.set(f"'{self.ent_quant[i].get()}' "
                                        f"is invalid. Must be whole number.")
                    return
                else:
                    self.total += self.prices[i] * int(self.ent_quant[i].get())
                    self.qty += int(self.ent_quant[i].get())

        if self.str_ship.get() == "1 day":
            self.total += Decimal(self.ship_days["1 day"])
        elif self.str_ship.get() == "2 days":
            self.total += Decimal(self.ship_days["2 days"])
        elif self.str_ship.get() == "3 days":
            self.total += Decimal(self.ship_days["3 days"])

        str_price = f"{self.total:.2f}"
        self.ent_result.delete(0, END)
        self.ent_result.insert(END, str_price)

    def submit(self):
        """Submit order information to web service."""
        ship = self.str_ship.get()
        total = str(self.total)
        if self.total <= 0:
            self.str_submit.set("Calculate price before submitting order.")
        elif self.qty <= 0:
            self.str_submit.set("Must specify products to order.")
        else:
            send = {"ship": ship, "total": total}
            post_total = requests.post("http://127.0.0.1:5000/submit",
                                       json=send)
            self.str_submit.set(f"Order no. {post_total.text} submitted.")

window = Tk()
window.title("Wood Delivery Calculator")
window.geometry("475x375")
app = Application(window)
app.mainloop()