import os
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox
import pdfplumber
import docx

def open_file():
    selected_index = results_listbox.curselection()
    if selected_index:
        line = selected_index[0]
        clicked_file = results_listbox.get(line)
        os.system(f'start {clicked_file}')  # For Win
        # os.system(f'open {clicked_file}')  # For macOS

def search_text():
    search_query = search_entry.get()
    if search_query == "":
        messagebox.showinfo("Alert", "Query is empty!")
        return
    results_listbox.delete(0, tk.END)
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.txt', '.pdf', '.docx')):
                    file_path = os.path.join(root, file)

                    if file.endswith('.txt'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if search_query in content:
                                results_listbox.insert(tk.END, file_path)

                    elif file.endswith('.pdf'):
                        with pdfplumber.open(file_path) as pdf:
                            for page_num in range(len(pdf.pages)):
                                page = pdf.pages[page_num]
                                text = page.extract_text()
                                if search_query in text:
                                    results_listbox.insert(tk.END, file_path + f' (Page {page_num + 1})')

                    elif file.endswith('.docx'):
                        doc = docx.Document(file_path)
                        for para in doc.paragraphs:
                            if search_query in para.text:
                                results_listbox.insert(tk.END, file_path)
    except Exception as e:
        messagebox.showinfo("Alert", "Directory error! " + str(e))

def open_directory():
    global directory
    directory = filedialog.askdirectory()
    directory_label.config(text=f"Selected Directory: {directory}")

app = tk.Tk()
app.title("Document Search App")

app.geometry("400x300")

search_label = tk.Label(app, text="Enter text to search:")
search_label.pack(pady=10)

search_entry = tk.Entry(app)
search_entry.pack(padx=10, pady=5, fill=tk.X)

search_button = tk.Button(app, text="Search", command=search_text)
search_button.pack(pady=5)

directory_button = tk.Button(app, text="Select Directory", command=open_directory)
directory_button.pack(pady=5)

directory_label = tk.Label(app, text="Selected Directory: None")
directory_label.pack(pady=5)

results_listbox = Listbox(app, height=10, selectmode=tk.SINGLE)
results_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

open_button = tk.Button(app, text="Open Selected", command=open_file)
open_button.pack(pady=5)

app.mainloop()
