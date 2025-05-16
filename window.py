import math
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from tkextrafont import Font
import os
import json
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
            name = path.split("/")[-1].split(".")[0]
            self.name_text.insert("1.0", name)
            self.open_new_window()


    def open_new_window(self):
        ListWindow(master=self, title=self.name_text.get(1.0, tk.END)[:-1], data=self.data)
        self.iconify()


class DataFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.frames = []
        self.frame_data = []
        self.icons = []
        self.image = None
        self.icon = None
        self.font_file = Font(file="fonts/minecraft_font.ttf", family="Minecraft")
        self.font = ctk.CTkFont('Minecraft')
        self.bold_font = ctk.CTkFont('Minecraft', 14, "bold")

        self.populate(data)

    def populate(self, data: dict):

        title_frame = ctk.CTkFrame(self, fg_color='#333333', height=50)

        title_frame.grid_columnconfigure(index=0, weight=0)
        title_frame.grid_columnconfigure(index=1, weight=1, uniform="equal_width")
        title_frame.grid_columnconfigure(index=2, weight=1, uniform="equal_width")
        title_frame.grid_columnconfigure(index=3, weight=1, uniform="equal_width")

        title_frame.grid(row=0, column=0, padx=(10, 5), pady=(10, 5), sticky='ew')

        icon_title = ctk.CTkLabel(master=title_frame, text="", width=200)
        name_title = ctk.CTkLabel(master=title_frame, text="Name", font=self.bold_font)
        amount_title = ctk.CTkLabel(master=title_frame, text="Stacks", font=self.bold_font)
        shulker_img = Image.open('icons/WIP/shulker_box.png')
        shulker_icon = ctk.CTkImage(light_image=shulker_img, dark_image=shulker_img, size=(32, 32))
        shulker_image = ctk.CTkLabel(master=title_frame, image=shulker_icon, text="")

        icon_title.grid(row=0, column=0, sticky='ns')
        name_title.grid(row=0, column=1, sticky='nsw')
        amount_title.grid(row=0, column=2, sticky='nsew')
        shulker_image.grid(row=0, column=3, sticky='nsew')

        for i, key in enumerate(data.keys()):
            img_path = f"icons/WIP/{key.replace(' ', '_').lower()}.png"

            frame = ListItemFrame(self, img_path, key, data[key], self.font, True, fg_color='#333333', height=50)

            pad = 10 if i == len(data.keys()) else 5
            frame.grid(row=i + 1, column=0, padx=(10, 5), pady=(pad, 5), sticky='ew')

            frame.bind("<Button-1>", lambda: frame.change_state())

            self.frames.append(frame)


class ListItemFrame(ctk.CTkFrame):
    def __init__(self, master, icon, name, amount, font, state, **kwargs):
        super().__init__(master, **kwargs)

        self.state = state

        self.grid_columnconfigure(index=0, weight=0)
        self.grid_columnconfigure(index=1, weight=1, uniform="equal_width")
        self.grid_columnconfigure(index=2, weight=1, uniform="equal_width")
        self.grid_columnconfigure(index=3, weight=1, uniform="equal_width")

        print("Loading image:", icon)
        assert os.path.exists(icon), f"Image file not found: {icon}"
        self.img = Image.open(icon)
        self.img = self.img.convert("RGBA")
        self.icon = ctk.CTkImage(light_image=self.img, dark_image=self.img, size=(32, 32))
        self.img_border = ctk.CTkFrame(master=self, fg_color="transparent")
        self.image = ctk.CTkLabel(master=self.img_border, image=self.icon, text="", width=200).pack()
        self.img_border.grid(row=0, column=0, sticky='ns')

        self.name = ctk.CTkLabel(master=self, text=name, font=font, anchor="w")
        self.name.grid(row=0, column=1, sticky="nsw")

        match parse.is_unstackable(name.replace(" ", "_").lower()):
            case 0:
                num = str(math.floor(amount / 64)) + " + " + str(amount % 64)
                shulker = str(round(amount / 1728, 1))
            case 1:
                num = str(amount)
                shulker = str(round(amount / 27, 1))
            case 2:
                num = str(math.floor(amount / 16)) + " + " + str(amount % 16)
                shulker = str(round(amount / 432, 1))

        if float(shulker) < 1:
            shulker = '0'

        self.count = ctk.CTkLabel(master=self, text=num, font=font)
        self.count.grid(row=0, column=2, sticky='nsew')

        self.shulker = ctk.CTkLabel(master=self, text=shulker, font=font)
        self.shulker.grid(row=0, column=3, sticky='nsew')


    def change_state(self):
        self.state = not self.state
        print(self.state)




class ListWindow(ctk.CTkToplevel):
    def __init__(self, master, title, data):
        super().__init__(master=master)

        ctk.set_appearance_mode("dark")
        self.geometry("960x540")
        self.title(title + " material list")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame = DataFrame(master=self, data=data)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")









