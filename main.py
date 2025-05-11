from mcstructure import Structure
import tkinter as tk
from tkinter import filedialog
import os

def load_saved_builds():
    saved_name = []
    buildlist = os.scandir("SavedBuilds")
    with buildlist as builds:
        for build in builds:
            saved_name.append(build.path.split("\\")[1].split(".")[0])
    return saved_name

def create_list(struct):
    block_count = {}

    for x in range(len(struct)):
        for y in range(len(struct[x])):
            for z in range(len(struct[x][y])):
                if struct[x][y][z].namespace_and_name[1] == 'air':
                    continue

                name = struct[x][y][z].namespace_and_name[1]
                match name:
                    case "unlit_redstone_torch":
                        name = "redstone_torch"
                    case "unpowered_repeater":
                        name = "repeater"
                    case "powered_repeater":
                        name = "repeater"
                    case "lit_redstone_lamp":
                        name = "redstone_lamp"
                    # case "bed":




                if name in block_count:
                    block_count[name] += 1
                else:
                    block_count[name] = 1

    return block_count

def count(nbt):

    if filepath == "":
        error.config(text="Please enter a file")
        root.update()
        error.place(x=(145 - (error.winfo_width() / 2)), y=60)
        root.update()
        return

    with open(nbt, "rb") as f:
        struct = Structure.load(f)

    print(struct.palette)
    open_from_structure(create_list(struct.get_structure()))

def upload_action():
    filename = filedialog.askopenfilename(filetypes=(("Bedrock Structure Files", "*.mcstructure"),))
    global filepath
    filepath = filename
    filename = filename.split("/")
    file.configure(state=tk.NORMAL)
    file.delete(0)
    file.insert(0, filename[-1])
    file.configure(state=tk.DISABLED)
    root.update()


def open_from_config(path):
    print(path)

def open_from_structure(palette):
    print(palette)

builds = load_saved_builds()

root = tk.Tk()
root.title("Structure Block Counter")
root.geometry("250x150")
root.minsize(290, 120)
root.maxsize(290, 120)

filepath = ""

label = tk.Label(root, text="Structure file")
file = tk.Listbox(root, height=1, width=20)
file.insert(0, 'No File Selected')
file.configure(state=tk.DISABLED)
import_file = tk.Button(root, text="Browse", command=lambda: upload_action())
name_label = tk.Label(root, text="Name")
name_text = tk.Text(root, width=15, height=1)
start_count = tk.Button(root, text="Count", command=lambda: count(filepath))
error = tk.Label(root, text="")

menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open saved builds")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
load = tk.Menu(menu)
menu.add_cascade(label="Load saved build", menu=load)
for build_name in builds:
    load.add_command(label=build_name, command=lambda b=build_name: open_from_config("SavedBuilds/" + b + ".json"))



file.place(x=0, y=0)
start_count.place(x=0, y=0)
error.place(x=0, y=0)
root.update()
label.place(x=5, y=0)
name_label.place(x=37, y=40)
name_text.place(x=(145 - (file.winfo_width() / 2)), y=43)
import_file.place(x=230, y=0)
file.place(x=(145 - (file.winfo_width() / 2)), y=3)
start_count.place(x=(145 - (start_count.winfo_width() / 2)), y=80)


root.mainloop()








