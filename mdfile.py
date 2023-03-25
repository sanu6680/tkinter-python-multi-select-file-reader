import tkinter as tk
from tkinter import filedialog
import sqlite3
import os


def browse_files():
    file_list = []
    files = filedialog.askopenfilenames(initialdir="/",
                                        title="Select files",
                                        filetypes=(("Markdown files", "*.md"),
                                                   ("Text files", "*.txt"),
                                                   ("All files", "*.*")))
    for file in files:
        file_list.append(file)
    listbox.delete(0, tk.END)
    for file in file_list:
        listbox.insert(tk.END, os.path.basename(file))


def add_files():
    file_list = []
    for index in listbox.curselection():
        file_list.append(listbox.get(index))
    for file in file_list:
        with open(file, "r") as f:
            content = f.read()
            cursor.execute("INSERT INTO records (filename, content) VALUES (?, ?)", (file, content))
            connection.commit()


def search_files():
    query = search_entry.get()
    cursor.execute("SELECT filename, content FROM records WHERE content LIKE ?", ('%' + query + '%',))
    results = cursor.fetchall()
    search_results.delete(0, tk.END)
    for result in results:
        search_results.insert(tk.END, result[0])


def show_content():
    index = search_results.curselection()[0]
    result = search_results.get(index)
    cursor.execute("SELECT content FROM records WHERE filename = ?", (result,))
    content = cursor.fetchone()[0]
    content_text.delete("1.0", tk.END)
    content_text.insert(tk.END, content)


connection = sqlite3.connect("files.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS records (filename TEXT, content TEXT)")
connection.commit()

root = tk.Tk()

listbox_label = tk.Label(root, text="Selected Files:")
listbox_label.pack()

listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack()

browse_button = tk.Button(root, text="Browse Files", command=browse_files)
browse_button.pack()

add_button = tk.Button(root, text="Add Files", command=add_files)
add_button.pack()

search_label = tk.Label(root, text="Search:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

search_button = tk.Button(root, text="Search", command=search_files)
search_button.pack()

show_content_button = tk.Button(root, text="Show Content", command=show_content)
show_content_button.pack()
search_results_label = tk.Label(root, text="Search Results:")
search_results_label.pack()

search_results = tk.Listbox(root)
search_results.pack()

content_label = tk.Label(root, text="Content:")
content_label.pack()

content_text = tk.Text(root)
content_text.pack()


root.mainloop()
