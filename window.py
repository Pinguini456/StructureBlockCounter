import tkinter as tk
import customtkinter as ctk
import os
import methods as m

class InputWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.builds = m.load_saved_builds()

        self.title("Structure Block Counter")
        self.geometry("250x150")
        self.minsize(290, 120)
        self.maxsize(290, 120)

        self.label = tk.Label(self, text="Structure file")
        self.file = tk.Listbox(self, height=1, width=20)
        self.file.insert(0, 'No File Selected')
        self.file.configure(state=tk.DISABLED)
        self.import_file = tk.Button(self, text="Browse", command=lambda: m.upload_action(self))
        self.name_label = tk.Label(self, text="Name")
        self.name_text = tk.Text(self, width=15, height=1)
        self.start_count = tk.Button(self, text="Count", command=lambda: m.count(self))
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
                             command=lambda b=build_name: m.open_from_config("SavedBuilds/" + b + ".json"))

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


class ListWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.geometry("960x540")