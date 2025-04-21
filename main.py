from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

# Database connection
def get_db_connection():
    return sqlite3.connect("Expense_Tracker_System.db")

def get_user_id(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM User WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None


def save_to_excel(user_id, username):
    # Get the transaction history
    transactions = show_all_transactions(user_id)
    
    # Prepare data for Excel
    expense_data = []
    income_data = []
    
    # Flags to identify sections
    expense_section = False
    income_section = False
    for transaction in transactions:
        # Handle the expenses section
        if "===== Expenses =====" in transaction:
            expense_section = True
            income_section = False
            continue
        elif "===== Income =====" in transaction:
            expense_section = False
            income_section = True
            continue
        
        # Extract expense data if we're in the expenses section
        if expense_section:
            amount = transaction.split(",")[0].split(":")[1].strip().replace('$', '')
            category = transaction.split(",")[1].split(":")[1].strip()
            description = transaction.split(",")[2].split(":")[1].strip()
            date = transaction.split(",")[3].split(":")[1].strip()
            expense_data.append({
                "Amount": amount,
                "Category": category,
                "Description": description,
                "Date": date
            })
        
        # Extract income data if we're in the income section
        if income_section:
            amount = transaction.split(",")[0].split(":")[1].strip().replace('$', '')
            source = transaction.split(",")[1].split(":")[1].strip()
            date = transaction.split(",")[2].split(":")[1].strip()
            income_data.append({
                "Amount": amount,
                "Source": source,
                "Date": date
            })
    
    # Combine both expense and income data into separate DataFrames
    expense_df = pd.DataFrame(expense_data)
    income_df = pd.DataFrame(income_data)
    
    # Create a filename using the user's username
    filename = f"{username}_transaction_history.xlsx"

    # Create an Excel writer
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write each dataframe to a separate sheet
        if not expense_df.empty:
            expense_df.to_excel(writer, sheet_name='Expenses', index=False)
        if not income_df.empty:
            income_df.to_excel(writer, sheet_name='Income', index=False)

    print(f"Transaction history has been saved to '{filename}'.")


# Function to add an expense
def add_expense(user_id, amount, category, description, date):
    try:
        amount = float(amount)
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)", 
                       (user_id, amount, category, description, date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Expense added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered!")

# Function to add income
def add_income(user_id, amount, source, date):
    try:
        amount = float(amount)
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Income (user_id, amount, source, date) VALUES (?, ?, ?, ?)", 
                       (user_id, amount, source, date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Income added successfully!")
    except ValueError:
        messagebox.showerror("Error", "Invalid amount entered!")

# Function to fetch transactions
def show_all_transactions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetching Expense Data for the specific user
    cursor.execute("SELECT amount, category, description, date FROM Expenses WHERE user_id = ?", (user_id,))
    expense_data = cursor.fetchall()

    # Fetching Income Data for the specific user
    cursor.execute("SELECT amount, source, date FROM Income WHERE user_id = ?", (user_id,))
    income_data = cursor.fetchall()
    conn.close()

    # Combine both expense and income data
    transactions = []
    transactions.append("===== Expenses =====")
    for row in expense_data:
        transactions.append(f"Amount: ${row[0]:.2f}, Category: {row[1]}, Description: {row[2]}, Date: {row[3]}")
    
    transactions.append("\n===== Income =====")
    for row in income_data:
        transactions.append(f"Amount: ${row[0]:.2f}, Source: {row[1]}, Date: {row[2]}")

    return transactions

# Visualization function
def show_chart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM Expenses WHERE user_id = ? GROUP BY category", (user_id,))
    expense_data = cursor.fetchall()
    cursor.execute("SELECT source, SUM(amount) FROM Income WHERE user_id = ? GROUP BY source", (user_id,))
    income_data = cursor.fetchall()
    conn.close()

    if not expense_data or not income_data:
        messagebox.showinfo("Info", "No data available to visualize.")
        return
    
    # Plotting charts
    expense_categories = [row[0] if row[0] else "Unknown" for row in expense_data]
    expense_amounts = [row[1] for row in expense_data]
    income_sources = [row[0] if row[0] else "Unknown" for row in income_data]
    income_amounts = [row[1] for row in income_data]

    fig, axs = plt.subplots(1, 2, figsize=(14, 8))
    axs[0].bar(expense_categories, expense_amounts, color='#ff5757', edgecolor='black')
    axs[0].set_title("Expense Breakdown", fontsize=16)
    axs[0].set_xlabel("Category")
    axs[0].set_ylabel("Amount ($)")
    axs[0].tick_params(axis='x', rotation=45)

    axs[1].bar(income_sources, income_amounts, color='#4caf50', edgecolor='black')
    axs[1].set_title("Income Breakdown", fontsize=16)
    axs[1].set_xlabel("Source")
    axs[1].set_ylabel("Amount ($)")
    axs[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()

# Main app function
def open_main_app(username):
    user_id = get_user_id(username)  # Fetch user_id for logged-in user
    
    if user_id is None:
        print("Error: User not found!")
        return

    root = Tk()
    root.title("Expense Tracker")
    root.geometry("850x650")
    root.configure(background='#1c1c1e')

    # Left Panel (Expense & Income Entry)
    left_frame = Frame(root, bg='#2c2c2e', padx=20, pady=20, highlightbackground='#505050', highlightthickness=1)
    left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    Label(left_frame, text=f"👤 Welcome, {username}!", fg='white', bg='#2c2c2e', font=('Roboto', 14, 'bold')).pack(pady=10)

    # Expense Entry Fields
    Label(left_frame, text="💸 Expense Amount:", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_expense_amount = Entry(left_frame)
    entry_expense_amount.pack(fill=X, padx=5, pady=2)

    Label(left_frame, text="📂 Category:", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_expense_category = Entry(left_frame)
    entry_expense_category.pack(fill=X, padx=5, pady=2)

    Label(left_frame, text="📝 Description:", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_expense_description = Entry(left_frame)
    entry_expense_description.pack(fill=X, padx=5, pady=2)

    Label(left_frame, text="📅 Date (YYYY-MM-DD):", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_expense_date = Entry(left_frame)
    entry_expense_date.pack(fill=X, padx=5, pady=2)

    Button(left_frame, text="➕ Add Expense", bg='#ff5757', fg='white', 
           command=lambda: add_expense(user_id, entry_expense_amount.get(), entry_expense_category.get(), 
                                       entry_expense_description.get(), entry_expense_date.get())).pack(pady=5, fill=X)

    Label(left_frame, text="--------------------------------------", fg='white', bg='#2c2c2e').pack()

    # Income Entry Fields
    Label(left_frame, text="💰 Income Amount:", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_income_amount = Entry(left_frame)
    entry_income_amount.pack(fill=X, padx=5, pady=2)

    Label(left_frame, text="🏦 Source:", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_income_source = Entry(left_frame)
    entry_income_source.pack(fill=X, padx=5, pady=2)

    Label(left_frame, text="📅 Date (YYYY-MM-DD):", fg='white', bg='#2c2c2e').pack(anchor='w')
    entry_income_date = Entry(left_frame)
    entry_income_date.pack(fill=X, padx=5, pady=2)

    Button(left_frame, text="➕ Add Income", bg='#4caf50', fg='white', 
           command=lambda: add_income(user_id, entry_income_amount.get(), entry_income_source.get(), entry_income_date.get())).pack(pady=5, fill=X)

    # Right Panel (Transaction History & Visualization)
    right_frame = Frame(root, bg='#3a3a3c', padx=20, pady=20, highlightbackground='#505050', highlightthickness=1)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    Label(right_frame, text="📜 Transaction History", fg='white', bg='#3a3a3c', font=('Roboto', 12, 'bold')).pack()

    transaction_text = Text(right_frame, height=20, width=50, bg='#2c2c2e', fg='white')
    transaction_text.pack(pady=5, fill=BOTH, expand=True)
    
    def show_all_transactions_display():
        transaction_text.delete(1.0, END)
        transactions = show_all_transactions(user_id)
        for transaction in transactions:
            transaction_text.insert(END, transaction + '\n')
    
    Button(right_frame, text="📂 View Full History", bg='#505050', fg='white', command=show_all_transactions_display).pack(pady=5, fill=X)
    Button(right_frame, text="📊 Visualize Data", bg='#505050', fg='white', command=lambda: show_chart(user_id)).pack(pady=5, fill=X)

    # Logout Button
  
    Button(root, text="🚪 Logout", bg='#d32f2f', fg='white', font=('Roboto', 8, 'bold'), 
       command=root.destroy, width=15, height=2).pack(pady=10, fill=X, padx=20)
    Button(right_frame, text="💾 Save to Excel", bg='#505050', fg='white', command=lambda: save_to_excel(user_id, username)).pack(pady=5, fill=X)


    root.mainloop()


def login():
    username = username_input.get().strip()
    password = password_input.get().strip()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = sqlite3.connect("Expense_Tracker_System.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    
    conn.close()
    
    if user:
        messagebox.showinfo("Success", f"Welcome {username}!")
        username_input.delete(0, END)
        password_input.delete(0, END)
        open_main_app(username)  # Function to open main application
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def signup():
    username = username_input.get().strip()
    password = password_input.get().strip()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = sqlite3.connect("Expense_Tracker_System.db")
    c = conn.cursor()
    
    try:
        c.execute("INSERT INTO User (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account Created! Please Log In.")
        username_input.delete(0, END)
        password_input.delete(0, END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    
    conn.close()

# Login Window
root = Tk()
root.title('Login & Signup')
root.geometry('400x550')
root.configure(background='#292a2d')

try:
    img = Image.open('logo.png')
    resized_img = img.resize((100, 100))
    img = ImageTk.PhotoImage(resized_img)
    Label(root, image=img, bg='#292a2d').pack(pady=(9, 9))
except Exception as e:
    messagebox.showerror("Error", f"Error loading image: {e}")

Label(root, text='Expense Tracker System', fg='white', bg='#292a2d', font=('Roboto', '18')).pack()
Label(root, text='Username', fg='white', bg='#292a2d', font=('Roboto', '14')).pack(pady=(20, 5))

username_input = Entry(root, width=50)
username_input.pack(ipady=6, pady=(1, 15))

Label(root, text='Password', fg='white', bg='#292a2d', font=('Roboto', '14')).pack(pady=(20, 5))
password_input = Entry(root, show='*', width=50)
password_input.pack(ipady=6, pady=(1, 15))

button_frame = Frame(root, bg='#292a2d')
button_frame.pack(pady=(10, 20))

Button(button_frame, text='Login', bg='#404045', fg='white', width=15, height=2, command=login).pack(side=LEFT, padx=10)
Button(button_frame, text='Signup', bg='#404045', fg='white', width=15, height=2, command=signup).pack(side=LEFT, padx=10)

root.mainloop()