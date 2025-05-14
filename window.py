import tkinter as tk
from tkinter import filedialog
from PIL import Image
import customtkinter as ctk
import os
import json

from customtkinter import CTkImage, CTkLabel

import parse


def load_saved_builds():
    saved_name = []
    buildlist = os.scandir("SavedBuilds")
    with buildlist as builds:
        for build in builds:
            saved_name.append(build.path.split("\\")[1].split(".")[0])
    return saved_name

class InputWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.builds = load_saved_builds()
        self.filepath = ""
        self.filename = ""
        self.data = {}

        self.title("Structure Block Counter")
        self.geometry("250x150")
        self.minsize(290, 120)
        self.maxsize(290, 120)

        self.label = tk.Label(self, text="Structure file")
        self.file = tk.Listbox(self, height=1, width=20)
        self.file.insert(0, 'No File Selected')
        self.file.configure(state=tk.DISABLED)
        self.import_file = tk.Button(self, text="Browse", command=lambda: self.upload_action())
        self.name_label = tk.Label(self, text="Name")
        self.name_text = tk.Text(self, width=15, height=1)
        self.name_text.config(wrap='none')
        self.start_count = tk.Button(self, text="Count", command=lambda: self.count())
        self.error = tk.Label(self, text="")

        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open saved builds",
                             command=lambda: os.startfile(os.path.abspath(os.getcwd()) + r'\SavedBuilds'))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.load = tk.Menu(self.menu)
        self.menu.add_cascade(label="Load saved build", menu=self.load)
        for build_name in self.builds:
            self.load.add_command(label=build_name,
                             command=lambda b=build_name: self.open_from_config("SavedBuilds/" + b + ".json"))

        self.file.place(x=0, y=0)
        self.start_count.place(x=0, y=0)
        self.error.place(x=0, y=0)
        self.update()
        self.label.place(x=5, y=0)
        self.name_label.place(x=37, y=35)
        self.name_text.place(x=(145 - (self.file.winfo_width() / 2)), y=38)
        self.import_file.place(x=230, y=0)
        self.file.place(x=(145 - (self.file.winfo_width() / 2)), y=3)
        self.start_count.place(x=(145 - (self.start_count.winfo_width() / 2)), y=80)

    def upload_action(self):
        self.filename = filedialog.askopenfilename(filetypes=(("Bedrock Structure Files", "*.mcstructure"),))
        if self.filename == "":
            return
        self.filepath = self.filename
        self.filename = self.filename.split("/")
        self.file.configure(state=tk.NORMAL)
        self.file.delete(0)
        self.file.insert(0, self.filename[-1])
        self.file.configure(state=tk.DISABLED)
        self.update()


    def count(self):
        if self.filepath == "":
            self.error.config(text="Please enter a file")
            self.update()
            self.error.place(x=(145 - (self.error.winfo_width() / 2)), y=60)
            self.update()
            return

        if self.name_text.get(1.0, tk.END)[:-1] == "":
            self.error.config(text="Please enter a name")
            self.update()
            self.error.place(x=(145 - (self.error.winfo_width() / 2)), y=60)
            self.update()
            return

        with open(self.filepath, "rb") as f:
            self.open_from_structure(f)
            self.open_new_window()

    def open_from_structure(self, file):
        a, b, c = parse.load(file)
        print(parse.total(a, b, c))
        self.data = parse.total(a, b, c)

        with open('SavedBuilds/' + self.name_text.get(1.0, tk.END)[:-1] + ".json", 'w+') as build:
            build.write(json.dumps(parse.total(a, b, c)))

    def open_from_config(self, path):
        with open(path, 'r') as f:
            self.data = json.loads(f.read())
            self.open_new_window()


    def open_new_window(self):
        app = ListWindow(self.name_text.get(1.0, tk.END)[:-1], self.data)
        self.destroy()
        app.mainloop()


class DataFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.frames = []
        self.frame_data = []
        self.populate(data)


    def populate(self, data: dict):
        for i in range(len(list(data.keys()))):
            frame = ctk.CTkFrame(self, fg_color='#333333', height=50)
            if i == 0 or i == len(data.keys()):
                pad = 10
            else:
                pad = 5
            frame.grid(row=i, column=0, padx=(10, 5), pady=(pad, 5), sticky='ew')
            self.frames.append(frame)

            image = Image.open("icons/" + list(data.keys())[i].replace(' ', "_").lower() + ".png")
            icon = ctk.CTkImage(dark_image=image, light_image=image)
            # label = ctk.CTkLabel(master=self, image=icon, text="")
            # label.grid(row=0, column=0, padx=2, pady=2, sticky='ns')
            # self.frame_data.append([label])





class ListWindow(ctk.CTk):
    def __init__(self, title, data):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.geometry("960x540")
        self.title(title + " material list")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = DataFrame(master=self, data=data)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")








