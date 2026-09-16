import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime, date
import matplotlib.pyplot as plt

FILENAME = "expenses.csv"
FIELDNAMES = ["ID", "Date", "Amount", "Category", "Description"]

if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

def add_expense():
    amt_text = amount_entry.get().strip()
    cat = category_var.get().strip()
    desc = desc_entry.get().strip()
    dt_text = date_entry.get().strip()

    if not amt_text or not cat:
        messagebox.showwarning("Input error", "Please enter amount and category.")
        return

    try:
        amt = float(amt_text)
    except ValueError:
        messagebox.showerror("Input error", "Amount must be a number.")
        return

    try:
        dt = datetime.strptime(dt_text, "%Y-%m-%d").date()
    except Exception:
        dt = date.today()

    row_id = datetime.now().isoformat(timespec='seconds')
    row = {"ID": row_id, "Date": dt.isoformat(), "Amount": f"{amt:.2f}", "Category": cat, "Description": desc}

    with open(FILENAME, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow(row)

    messagebox.showinfo("Success", "Expense added.")
    clear_inputs()
    load_expenses()

def load_expenses():
    for item in tree.get_children():
        tree.delete(item)

    with open(FILENAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            tree.insert("", tk.END, values=(r["ID"], r["Date"], r["Amount"], r["Category"], r["Description"]))

def delete_selected():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Delete", "Select an entry to delete.")
        return

    if not messagebox.askyesno("Delete", "Are you sure you want to delete the selected entry?"):
        return

    sel_ids = [tree.item(s)["values"][0] for s in sel]

    with open(FILENAME, "r", newline="") as f:
        reader = list(csv.DictReader(f))

    new_rows = [r for r in reader if r["ID"] not in sel_ids]

    with open(FILENAME, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(new_rows)

    load_expenses()
    messagebox.showinfo("Deleted", "Selected entry deleted.")

def show_chart():
    categories = {}
    with open(FILENAME, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            try:
                a = float(r["Amount"])
            except:
                continue
            cat = r["Category"]
            categories[cat] = categories.get(cat, 0) + a

    if not categories:
        messagebox.showinfo("No data", "No expense data to show.")
        return

    labels = list(categories.keys())
    sizes = list(categories.values())
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Expenses by Category")
    plt.show()

def clear_inputs():
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    if category_combo['values']:
        category_combo.current(0)
    date_entry.delete(0, tk.END)
    date_entry.insert(0, date.today().isoformat())

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")
root.resizable(False, False)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill=tk.X)

tk.Label(frame, text="Amount:").grid(row=0, column=0, sticky="w")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Category:").grid(row=1, column=0, sticky="w")
category_var = tk.StringVar()
common_cats = ["Food", "Transport", "Groceries", "Bills", "Entertainment", "Other"]
category_combo = ttk.Combobox(frame, textvariable=category_var, values=common_cats, state="readonly")
category_combo.grid(row=1, column=1, padx=5, pady=5)
category_combo.current(0)

tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=2, sticky="w")
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=3, padx=5, pady=5)
date_entry.insert(0, date.today().isoformat())

tk.Label(frame, text="Description:").grid(row=1, column=2, sticky="w")
desc_entry = tk.Entry(frame, width=30)
desc_entry.grid(row=1, column=3, padx=5, pady=5)

btn_frame = tk.Frame(root, pady=5)
btn_frame.pack(fill=tk.X)
tk.Button(btn_frame, text="Add Expense", command=add_expense, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Delete Selected", command=delete_selected, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Show Chart", command=show_chart, width=15).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Clear Inputs", command=clear_inputs, width=12).pack(side=tk.LEFT, padx=10)

cols = ("ID", "Date", "Amount", "Category", "Description")
tree = ttk.Treeview(root, columns=cols, show="headings", height=15)
for c in cols:
    tree.heading(c, text=c)
    if c == "ID":
        tree.column(c, width=0, stretch=False)
    elif c == "Description":
        tree.column(c, width=220)
    else:
        tree.column(c, width=100)
tree.pack(fill=tk.BOTH, padx=10, pady=10)

load_expenses()
root.mainloop()
