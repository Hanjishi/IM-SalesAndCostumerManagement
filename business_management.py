import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "business_management"
}

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management System")
        self.root.geometry("850x600")
        self.root.configure(bg="#f0f2f5")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.setup_ui()
        self.fetch_customers()

    def setup_ui(self):
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.billing_address_var = tk.StringVar()
        self.shipping_address_var = tk.StringVar()

        form_frame = ttk.LabelFrame(self.root, text="Customer Information", padding=20)
        form_frame.pack(padx=20, pady=10, fill="x")

        labels = ["Name", "Email", "Phone", "Billing Address", "Shipping Address"]
        vars = [self.name_var, self.email_var, self.phone_var, self.billing_address_var, self.shipping_address_var]

        for i, (label, var) in enumerate(zip(labels, vars)):
            ttk.Label(form_frame, text=label + ":").grid(row=i, column=0, sticky="w", pady=5)
            ttk.Entry(form_frame, textvariable=var, width=50).grid(row=i, column=1, pady=5, padx=10)

        button_frame = tk.Frame(self.root, bg="#f0f2f5")
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Customer", command=self.add_customer).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Update Customer", command=self.update_customer).grid(row=0, column=1, padx=10)
        ttk.Button(button_frame, text="Delete Customer", command=self.delete_customer).grid(row=0, column=2, padx=10)

        # Treeview
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(pady=20, fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Name", "Email", "Phone"), show="headings", selectmode="browse")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")

        # Configure column widths
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=200)
        self.tree.column("Email", width=200)
        self.tree.column("Phone", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree.bind("<ButtonRelease-1>", self.select_customer)

    def get_db_connection(self):
        return mysql.connector.connect(**DB_CONFIG)

    def fetch_customers(self):
        self.tree.delete(*self.tree.get_children())
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, name, email, phone FROM customers")
        for i, row in enumerate(cursor.fetchall()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=row, tags=(tag,))
        conn.close()

        # Alternate row colors
        self.tree.tag_configure('evenrow', background="#f9f9f9")
        self.tree.tag_configure('oddrow', background="#e0e0e0")

    def add_customer(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO customers (name, email, phone, billing_address, shipping_address) VALUES (%s, %s, %s, %s, %s)"
        val = (
            self.name_var.get(),
            self.email_var.get(),
            self.phone_var.get(),
            self.billing_address_var.get(),
            self.shipping_address_var.get()
        )
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        self.fetch_customers()
        messagebox.showinfo("Success", "Customer added successfully")

    def update_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a customer to update")
            return

        customer_id = self.tree.item(selected[0])["values"][0]

        conn = self.get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE customers SET name=%s, email=%s, phone=%s, billing_address=%s, shipping_address=%s WHERE customer_id=%s"
        val = (
            self.name_var.get(),
            self.email_var.get(),
            self.phone_var.get(),
            self.billing_address_var.get(),
            self.shipping_address_var.get(),
            customer_id
        )
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        self.fetch_customers()
        messagebox.showinfo("Success", "Customer updated successfully")

    def delete_customer(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a customer to delete")
            return

        customer_id = self.tree.item(selected[0])["values"][0]
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM customers WHERE customer_id=%s", (customer_id,))
        conn.commit()
        conn.close()
        self.fetch_customers()
        messagebox.showinfo("Deleted", "Customer deleted successfully")

    def select_customer(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        conn = self.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (values[0],))
        row = cursor.fetchone()
        conn.close()

        if row:
            self.name_var.set(row["name"])
            self.email_var.set(row["email"])
            self.phone_var.set(row["phone"])
            self.billing_address_var.set(row["billing_address"])
            self.shipping_address_var.set(row["shipping_address"])

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()
