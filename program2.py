
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


# ---------- Database ----------
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT,
    price REAL,
    quantity INTEGER,
    total REAL
)
""")

conn.commit()


# ---------- Main Window ----------
root = tk.Tk()
root.title("Product Entry System")
root.geometry("780x520")
root.configure(bg="#f0f4f7")


# ---------- Variables ----------
product_id = tk.StringVar()
product_name = tk.StringVar()
price = tk.StringVar()
quantity = tk.StringVar()
total = tk.StringVar()


# ---------- Functions ----------

def calculate_total():
    try:
        p = float(price.get())
        q = int(quantity.get())
        total.set(str(p * q))
    except ValueError:
        total.set("")


def add_product():
    if product_id.get() == "":
        messagebox.showerror("Error", "Enter Product ID")
        return

    if product_name.get() == "":
        messagebox.showerror("Error", "Enter Product Name")
        return

    try:
        calculate_total()

        cursor.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
            (
                product_id.get(),
                product_name.get(),
                float(price.get()),
                int(quantity.get()),
                float(total.get())
            )
        )

        conn.commit()
        show_data()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Product Added Successfully"
        )

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Product ID already exists"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid Price and Quantity"
        )


def show_data():
    table.delete(*table.get_children())

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    for row in rows:
        table.insert("", "end", values=row)


def get_data(event):
    selected = table.focus()
    values = table.item(selected, "values")

    if values:
        product_id.set(values[0])
        product_name.set(values[1])
        price.set(values[2])
        quantity.set(values[3])
        total.set(values[4])


def update_product():
    if product_id.get() == "":
        messagebox.showerror(
            "Error",
            "Select Product"
        )
        return

    try:
        calculate_total()

        cursor.execute("""
        UPDATE products
        SET name = ?,
            price = ?,
            quantity = ?,
            total = ?
        WHERE id = ?
        """, (
            product_name.get(),
            float(price.get()),
            int(quantity.get()),
            float(total.get()),
            product_id.get()
        ))

        conn.commit()
        show_data()
        clear_fields()

        messagebox.showinfo(
            "Success",
            "Product Updated Successfully"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Enter valid Price and Quantity"
        )


def delete_product():
    if product_id.get() == "":
        messagebox.showerror(
            "Error",
            "Select Product"
        )
        return

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id.get(),)
    )

    conn.commit()
    show_data()
    clear_fields()

    messagebox.showinfo(
        "Success",
        "Product Deleted Successfully"
    )


def clear_fields():
    product_id.set("")
    product_name.set("")
    price.set("")
    quantity.set("")
    total.set("")


# ---------- Title ----------
title_label = tk.Label(
    root,
    text="Product Entry System",
    font=("Arial", 18, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=10
)

title_label.pack(fill="x")


# ---------- Entry Frame ----------
frame = tk.Frame(
    root,
    bg="#f0f4f7"
)

frame.pack(pady=15)


label_style = {
    "font": ("Arial", 11, "bold"),
    "bg": "#f0f4f7"
}


# ---------- Product ID ----------
tk.Label(
    frame,
    text="Product ID",
    **label_style
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)

tk.Entry(
    frame,
    textvariable=product_id
).grid(
    row=0,
    column=1
)


# ---------- Product Name ----------
tk.Label(
    frame,
    text="Product Name",
    **label_style
).grid(
    row=1,
    column=0,
    padx=10,
    pady=5
)

tk.Entry(
    frame,
    textvariable=product_name
).grid(
    row=1,
    column=1
)


# ---------- Price ----------
tk.Label(
    frame,
    text="Price",
    **label_style
).grid(
    row=2,
    column=0,
    padx=10,
    pady=5
)

price_entry = tk.Entry(
    frame,
    textvariable=price
)

price_entry.grid(
    row=2,
    column=1
)


# ---------- Quantity ----------
tk.Label(
    frame,
    text="Quantity",
    **label_style
).grid(
    row=3,
    column=0,
    padx=10,
    pady=5
)

quantity_entry = tk.Entry(
    frame,
    textvariable=quantity
)

quantity_entry.grid(
    row=3,
    column=1
)


# ---------- Total ----------
tk.Label(
    frame,
    text="Total Price",
    **label_style
).grid(
    row=4,
    column=0,
    padx=10,
    pady=5
)

tk.Entry(
    frame,
    textvariable=total,
    state="readonly"
).grid(
    row=4,
    column=1
)


# ---------- Auto Calculate ----------
price_entry.bind(
    "<KeyRelease>",
    lambda event: calculate_total()
)

quantity_entry.bind(
    "<KeyRelease>",
    lambda event: calculate_total()
)


# ---------- Buttons ----------
btn_frame = tk.Frame(
    root,
    bg="#f0f4f7"
)

btn_frame.pack(pady=10)


button_style = {
    "width": 10,
    "font": ("Arial", 10, "bold")
}


# Add Button
tk.Button(
    btn_frame,
    text="Add",
    bg="#27ae60",
    fg="white",
    command=add_product,
    **button_style
).grid(
    row=0,
    column=0,
    padx=5
)


# Update Button
tk.Button(
    btn_frame,
    text="Update",
    bg="#2980b9",
    fg="white",
    command=update_product,
    **button_style
).grid(
    row=0,
    column=1,
    padx=5
)


# Delete Button
tk.Button(
    btn_frame,
    text="Delete",
    bg="#c0392b",
    fg="white",
    command=delete_product,
    **button_style
).grid(
    row=0,
    column=2,
    padx=5
)


# Show Button
tk.Button(
    btn_frame,
    text="Show",
    bg="#8e44ad",
    fg="white",
    command=show_data,
    **button_style
).grid(
    row=0,
    column=3,
    padx=5
)


# Clear Button
tk.Button(
    btn_frame,
    text="Clear",
    bg="#7f8c8d",
    fg="white",
    command=clear_fields,
    **button_style
).grid(
    row=0,
    column=4,
    padx=5
)


# ---------- Table ----------
table_frame = tk.Frame(root)
table_frame.pack(pady=10)


columns = (
    "ID",
    "Name",
    "Price",
    "Quantity",
    "Total"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)


for col in columns:
    table.heading(
        col,
        text=col
    )

    table.column(
        col,
        width=130
    )


table.pack()


# Select row from table
table.bind(
    "<ButtonRelease-1>",
    get_data
)


# ---------- Initial Data Load ----------
show_data()


# ---------- Run App ----------
root.mainloop()


# ---------- Close Database ----------
conn.close()


