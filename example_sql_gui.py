import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import pandas as pd

# Set up SQLite database
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# Create tables
cursor.executescript('''
CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT
);

CREATE TABLE Activities (
    activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    game TEXT,
    score INTEGER,
    date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
''')

# Load data from CSV files into pandas DataFrames
users_df = pd.read_csv('users.csv')
activities_df = pd.read_csv('activities.csv')

# Insert data from the DataFrames into the SQLite database
users_df.to_sql('Users', connection, if_exists='append', index=False)
activities_df.to_sql('Activities', connection, if_exists='append', index=False)
connection.commit()

def list_tables():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    return [table[0] for table in cursor.fetchall()]

def list_columns(table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [col[1] for col in cursor.fetchall()]

def show_tables_and_columns():
    output_text.delete("1.0", tk.END)
    for table in list_tables():
        output_text.insert(tk.END, f"Tabelle: {table}\n")
        for col in list_columns(table):
            output_text.insert(tk.END, f"  - {col}\n")
        output_text.insert(tk.END, "\n")

def generate_query():
    username, game = entry_username.get(), entry_game.get()
    base_query = (
        "SELECT\n"
        "Users.username,\n"
        "Activities.game,\n"
        "Activities.score,\n"
        "Activities.date\n"
        "FROM Activities\n"
        "JOIN Users ON Activities.user_id = Users.user_id"
    )
    conditions = [f"Users.username = '{username}'" if username else "",
                  f"Activities.game = '{game}'" if game else ""]
    query = base_query + "\nWHERE " + " AND ".join(filter(None, conditions)) if any(conditions) else base_query

    output_query.delete("1.0", tk.END)
    output_query.insert(tk.END, query)  # Keep user ability to manually input
    apply_syntax_highlighting()

def run_query():
    query = output_query.get("1.0", tk.END).strip()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        tree.delete(*tree.get_children())
        col_names = [description[0] for description in cursor.description]
        tree["columns"] = col_names
        for col in col_names:
            tree.column(col, anchor=tk.W, width=120, minwidth=100, stretch=tk.NO)
            tree.heading(col, text=col, anchor=tk.W)
        for row in result:
            tree.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_avg_score_query():
    username, game = entry_username.get(), entry_game.get()
    if not (username and game):
        messagebox.showerror("Error", "Please enter both Username and Game to calculate the average score.")
        return

    query = (
        f"SELECT AVG(Activities.score)\n"
        f"FROM Activities\n"
        f"JOIN Users ON Activities.user_id = Users.user_id\n"
        f"WHERE Users.username = '{username}' AND Activities.game = '{game}';"
    )
    output_query.delete("1.0", tk.END)
    output_query.insert(tk.END, query)  # Allow user to see query generation
    apply_syntax_highlighting()

# Enhanced SQL syntax highlighting
def apply_syntax_highlighting(event=None):
    keywords = ["SELECT", "FROM", "JOIN", "WHERE", "AND", "OR", "AVG", "COUNT", "DISTINCT", "ON", "IN", "ORDER", "BY","PARTITION", "WITH",
                "DESC", "ASC", "GROUP", "AS", "LIMIT", "IS NULL", "IS", "LEFT", "RIGHT", "AS"]
    output_query.tag_remove("keyword", "1.0", tk.END)  # Clear previous tags
    text = output_query.get("1.0", tk.END)
    
    for keyword in keywords:
        start_idx = "1.0"
        while True:
            start_idx = output_query.search(keyword, start_idx, nocase=1, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(keyword)}c"
            output_query.tag_add("keyword", start_idx, end_idx)
            output_query.tag_config("keyword", foreground="blue")
            start_idx = end_idx

def open_add_window():
    add_window = Toplevel(root)
    add_window.title("Add User and Activity")

    labels = [("New Username:", "new_username"), ("New Email:", "new_email"),
              ("Activity Username:", "activity_username"), ("Game:", "activity_game"),
              ("Score:", "activity_score"), ("Date (YYYY-MM-DD):", "activity_date")]

    entries = {}
    for text, var in labels:
        tk.Label(add_window, text=text).pack()
        entries[var] = tk.Entry(add_window)
        entries[var].pack()

    tk.Button(add_window, text="Add New User", command=lambda: add_user(entries["new_username"], entries["new_email"])).pack()
    tk.Button(add_window, text="Add New Activity", command=lambda: add_activity(entries["activity_username"], entries["activity_game"], entries["activity_score"], entries["activity_date"])).pack()

def add_user(username_entry, email_entry):
    new_username, new_email = username_entry.get(), email_entry.get()
    if not (new_username and new_email):
        messagebox.showerror("Error", "Please enter both Username and Email.")
        return
    try:
        cursor.execute('INSERT INTO Users (username, email) VALUES (?, ?)', (new_username, new_email))
        connection.commit()
        messagebox.showinfo("Success", f"User {new_username} added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_activity(username_entry, game_entry, score_entry, date_entry):
    activity_username, game, score, date = username_entry.get(), game_entry.get(), score_entry.get(), date_entry.get()
    if not (activity_username and game and score and date):
        messagebox.showerror("Error", "Please fill out all fields to add an activity.")
        return
    try:
        cursor.execute('SELECT user_id FROM Users WHERE username = ?', (activity_username,))
        user_id = cursor.fetchone()
        if user_id is None:
            messagebox.showerror("Error", f"User {activity_username} does not exist.")
            return
        cursor.execute('INSERT INTO Activities (user_id, game, score, date) VALUES (?, ?, ?, ?)', (user_id[0], game, score, date))
        connection.commit()
        messagebox.showinfo("Success", f"Activity for {activity_username} in {game} added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Dynamic SQL Query Generator")

show_tables_button = ttk.Button(root, text="Your Database", command=show_tables_and_columns)
show_tables_button.pack(pady=10)

output_text = tk.Text(root, height=6, width=80)
output_text.pack(pady=10)

label_username = tk.Label(root, text="Enter Username:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_game = tk.Label(root, text="Enter Game:")
label_game.pack()
entry_game = tk.Entry(root)
entry_game.pack()

frame_buttons_generate = tk.Frame(root)
frame_buttons_generate.pack()

button_generate = tk.Button(frame_buttons_generate, text="Generate SQL Query", command=generate_query)
button_generate.pack(side=tk.LEFT, padx=5)

button_generate_avg = tk.Button(frame_buttons_generate, text="Generate Avg Score Query", command=generate_avg_score_query)
button_generate_avg.pack(side=tk.LEFT, padx=5)

output_query = tk.Text(root, height=8, width=80, wrap="word")
output_query.pack()
output_query.bind("<KeyRelease>", apply_syntax_highlighting)  # Re-enable real-time highlighting

scroll_y = tk.Scrollbar(root, orient=tk.VERTICAL, command=output_query.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
output_query.configure(yscrollcommand=scroll_y.set)

frame_buttons_run = tk.Frame(root)
frame_buttons_run.pack()

button_run = tk.Button(frame_buttons_run, text="Run Query", command=run_query)
button_run.pack(side=tk.LEFT, padx=5)

tree = ttk.Treeview(root, show="headings", height=8)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

button_open_add_window = tk.Button(root, text="Add User/Activity", command=open_add_window)
button_open_add_window.pack(pady=10)

root.mainloop()
connection.close()
