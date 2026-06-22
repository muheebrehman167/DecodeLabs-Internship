"""
============================================================
PROJECT 2 (ADVANCED): EXPENSE TRACKER - GUI EDITION
============================================================
Organization :  DecodeLabs
Batch        :  2026
Developer    :  Muheeb-ur-Rehman
Description  :  A professional desktop Expense Tracker
                application built with Tkinter. Features
                include adding, editing, deleting, and
                managing expenses, real-time dashboard
                statistics, expense summaries, category-based
                tracking, and persistent data storage using
                JSON for automatic saving and loading.
Tech Stack   :  Python, Tkinter (standard library),
                JSON (standard library)
============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os

# =====================================
# WINDOW
# =====================================

root = tk.Tk()
root.title("Expense Tracker Pro")
root.geometry("1200x750")
root.configure(bg="#0F172A")
root.resizable(False, False)

# =====================================
# COLORS
# =====================================

BG = "#0F172A"
CARD = "#1E293B"
TEXT = "#F8FAFC"
ACCENT = "#10B981"
BLUE = "#3B82F6"
GRAY = "#94A3B8"

# =====================================
# VARIABLES
# =====================================

total_expense = 0

# =====================================
# JSON STORAGE
# =====================================

FILE_NAME = "expenses.json"


def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except:
            return []
    return []


def save_data():
    data = []
    for item in tree.get_children():
        values = tree.item(item)["values"]
        data.append({"date": values[0], "category": values[1], "amount": values[2]})
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def load_expenses():
    global total_expense
    data = load_data()
    for expense in data:
        tree.insert("", "end", values=(expense["date"], expense["category"], expense["amount"]))
        total_expense += float(expense["amount"])
    update_dashboard()

# =====================================
# FUNCTIONS
# =====================================

def update_dashboard():
    total_label.config(
        text=f"Rs. {total_expense:,.2f}"
    )

    transaction_label.config(
        text=str(len(tree.get_children()))
    )


def add_expense():
    global total_expense

    amount = amount_entry.get().strip()

    if amount == "":
        messagebox.showerror(
            "Error",
            "Enter amount"
        )
        return

    try:
        amount = float(amount)
    except:
        messagebox.showerror(
            "Error",
            "Amount must be numeric"
        )
        return

    category = category_var.get()

    date = datetime.now().strftime(
        "%d-%m-%Y %H:%M"
    )

    tree.insert(
        "",
        "end",
        values=(
            date,
            category,
            f"{amount:.2f}"
        )
    )

    total_expense += amount

    update_dashboard()

    save_data()

    amount_entry.delete(0, tk.END)


def delete_expense():
    global total_expense

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select an expense first"
        )
        return

    values = tree.item(selected[0])["values"]

    amount = float(values[2])

    total_expense -= amount

    tree.delete(selected[0])

    update_dashboard()
    save_data()


def clear_all():
    global total_expense

    confirm = messagebox.askyesno(
        "Confirm",
        "Delete all expenses?"
    )

    if not confirm:
        return

    for item in tree.get_children():
        tree.delete(item)

    total_expense = 0

    update_dashboard()
    save_data()


def edit_expense():
    global total_expense

    selected = tree.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Select an expense"
        )
        return

    item = tree.item(selected[0])

    values = item["values"]

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, values[2])

    category_var.set(values[1])

    total_expense -= float(values[2])

    tree.delete(selected[0])

    update_dashboard()
    save_data()


def show_summary():

    summary = tk.Toplevel(root)
    summary.title("Expense Summary")
    summary.geometry("350x250")
    summary.configure(bg=CARD)

    tk.Label(
        summary,
        text="Expense Summary",
        bg=CARD,
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        summary,
        text=f"Total Expenses\nRs. {total_expense:,.2f}",
        bg=CARD,
        fg=ACCENT,
        font=("Segoe UI", 14)
    ).pack(pady=10)

    tk.Label(
        summary,
        text=f"Transactions\n{len(tree.get_children())}",
        bg=CARD,
        fg=BLUE,
        font=("Segoe UI", 14)
    ).pack(pady=10)


# =====================================
# HEADER
# =====================================

header = tk.Frame(
    root,
    bg=BLUE,
    height=80
)

header.pack(fill="x")

header.pack_propagate(False)

tk.Label(
    header,
    text="Expense Tracker Dashboard",
    bg=BLUE,
    fg="white",
    font=("Segoe UI", 24, "bold")
).pack(pady=18)

# =====================================
# DASHBOARD CARDS
# =====================================

cards_frame = tk.Frame(
    root,
    bg=BG
)

cards_frame.pack(
    fill="x",
    padx=25,
    pady=20
)

# Total Card

card1 = tk.Frame(
    cards_frame,
    bg=CARD,
    width=550,
    height=130
)

card1.pack(
    side="left",
    padx=(0, 20)
)

card1.pack_propagate(False)

tk.Label(
    card1,
    text="Total Expenses",
    bg=CARD,
    fg=GRAY,
    font=("Segoe UI", 14)
).pack(
    pady=(25, 5)
)

total_label = tk.Label(
    card1,
    text="Rs. 0.00",
    bg=CARD,
    fg=ACCENT,
    font=("Segoe UI", 24, "bold")
)

total_label.pack()

# Transaction Card

card2 = tk.Frame(
    cards_frame,
    bg=CARD,
    width=550,
    height=130
)

card2.pack(side="left")

card2.pack_propagate(False)

tk.Label(
    card2,
    text="Transactions",
    bg=CARD,
    fg=GRAY,
    font=("Segoe UI", 14)
).pack(
    pady=(25, 5)
)

transaction_label = tk.Label(
    card2,
    text="0",
    bg=CARD,
    fg=BLUE,
    font=("Segoe UI", 24, "bold")
)

transaction_label.pack()

# =====================================
# INPUT SECTION
# =====================================

input_frame = tk.Frame(
    root,
    bg=CARD,
    height=90
)

input_frame.pack(
    fill="x",
    padx=25
)

input_frame.pack_propagate(False)

# Configure equal columns
for i in range(3):
    input_frame.grid_columnconfigure(i, weight=1)

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    padding=8,
    font=("Segoe UI", 12)
)

# Amount Entry
amount_entry = tk.Entry(
    input_frame,
    font=("Segoe UI", 12),
    relief="flat",
    fg="gray"
)

amount_entry.insert(0, "Enter Amount")


def on_entry_click(event):
    if amount_entry.get() == "Enter Amount":
        amount_entry.delete(0, tk.END)
        amount_entry.config(fg="black")


def on_focus_out(event):
    if amount_entry.get().strip() == "":
        amount_entry.insert(0, "Enter Amount")
        amount_entry.config(fg="gray")


amount_entry.bind("<FocusIn>", on_entry_click)
amount_entry.bind("<FocusOut>", on_focus_out)

amount_entry.grid(
    row=0,
    column=0,
    padx=15,
    pady=22,
    ipady=12,
    sticky="ew"
)

# Category Dropdown
category_var = tk.StringVar()

category_box = ttk.Combobox(
    input_frame,
    textvariable=category_var,
    state="readonly",
    font=("Segoe UI", 12)
)

category_box["values"] = (
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Health",
    "Education",
    "Entertainment",
    "Other"
)

category_box.current(0)

category_box.grid(
    row=0,
    column=1,
    padx=15,
    pady=22,
    ipady=5,
    sticky="ew"
)

# Add Expense Button
add_btn = tk.Button(
    input_frame,
    text="+ Add Expense",
    bg=ACCENT,
    fg="white",
    relief="flat",
    font=("Segoe UI", 11, "bold"),
    command=add_expense,
    cursor="hand2"
)

add_btn.grid(
    row=0,
    column=2,
    padx=15,
    pady=22,
    ipady=10,
    sticky="ew"
)

# =====================================
# ACTION BUTTONS
# =====================================

action_frame = tk.Frame(
    root,
    bg=BG
)

action_frame.pack(
    fill="x",
    padx=25,
    pady=15
)

btn_style = {
    "font": ("Segoe UI", 10, "bold"),
    "relief": "flat",
    "fg": "white",
    "cursor": "hand2",
    "width": 12
}

tk.Button(
    action_frame,
    text="✏ Edit",
    bg="#F59E0B",
    command=edit_expense,
    **btn_style
).pack(side="left", padx=5)

tk.Button(
    action_frame,
    text="🗑 Delete",
    bg="#EF4444",
    command=delete_expense,
    **btn_style
).pack(side="left", padx=5)

tk.Button(
    action_frame,
    text="🧹 Clear All",
    bg="#6B7280",
    command=clear_all,
    **btn_style
).pack(side="left", padx=5)

tk.Button(
    action_frame,
    text="📊 Summary",
    bg=BLUE,
    command=show_summary,
    **btn_style
).pack(side="left", padx=5)

# =====================================
# TABLE
# =====================================

table_frame = tk.Frame(
    root,
    bg=BG
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 20)
)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD,
    foreground="white",
    fieldbackground=CARD,
    rowheight=35,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#334155",
    foreground="white",
    font=("Segoe UI", 11, "bold")
)

columns = (
    "Date",
    "Category",
    "Amount"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

tree.heading("Date", text="Date & Time")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount (Rs.)")

tree.column("Date", width=450, anchor="center")
tree.column("Category", width=300, anchor="center")
tree.column("Amount", width=250, anchor="center")

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scrollbar.set
)

tree.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

# =====================================
# START
# =====================================

load_expenses()

root.mainloop()