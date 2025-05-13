import tkinter as tk
import window as w
import customtkinter as ctk
from tkinter import filedialog
import os
import parse
import json

filepath = ""

def open_new_window(root):
    root.destroy()

    app = w.ListWindow()
    app.mainloop()

def load_saved_builds():
    saved_name = []
    buildlist = os.scandir("SavedBuilds")
    with buildlist as builds:
        for build in builds:
            saved_name.append(build.path.split("\\")[1].split(".")[0])
    return saved_name


def open_from_config(path):
    with open(path, 'r') as f:
        print(json.loads(f.read()))

def open_from_structure(file, name_text):
    a, b, c = parse.load(file)
    print(parse.total(a, b, c))

    with open('SavedBuilds/' + name_text.get(1.0, tk.END)[:-1] + ".json", 'w+') as build:
        build.write(json.dumps(parse.total(a, b, c)))

def upload_action(root):
    filename = filedialog.askopenfilename(filetypes=(("Bedrock Structure Files", "*.mcstructure"),))
    if filename == "":
        return
    global filepath
    filepath = filename
    filename = filename.split("/")
    root.file.configure(state=tk.NORMAL)
    root.file.delete(0)
    root.file.insert(0, filename[-1])
    root.file.configure(state=tk.DISABLED)
    root.update()

def count(root):

    if filepath == "":
        root.error.config(text="Please enter a file")
        root.update()
        root.error.place(x=(145 - (root.error.winfo_width() / 2)), y=60)
        root.update()
        return

    if root.name_text.get(1.0, tk.END)[:-1] == "":
        root.error.config(text="Please enter a name")
        root.update()
        root.error.place(x=(145 - (root.error.winfo_width() / 2)), y=60)
        root.update()
        return

    with open(filepath, "rb") as f:
        open_from_structure(f, root.name_text)
        open_new_window(root)