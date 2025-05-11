from mcstructure import Structure
import tkinter as tk
from tkinter import filedialog


def create_list(struct):
    block_count = {}

    for x in range(len(struct)):
        for y in range(len(struct[x])):
            for z in range(len(struct[x][y])):
                if struct[x][y][z].namespace_and_name[1] == 'air':
                    continue

                if struct[x][y][z].namespace_and_name[1] in block_count:
                    block_count[struct[x][y][z].namespace_and_name[1]] += 1
                else:
                    block_count[struct[x][y][z].namespace_and_name[1]] = 1

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

    print(create_list(struct.get_structure()))

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



root = tk.Tk()
root.geometry("250x150")
root.minsize(290, 120)
root.maxsize(290, 120)

filepath = ""

title = tk.Label(root, text="Structure Block Counter")
label = tk.Label(root, text="Structure file")
file = tk.Listbox(root, height=1, width=20)
file.insert(0, 'No File Selected')
file.configure(state=tk.DISABLED)
import_file = tk.Button(root, text="Browse", command=lambda: upload_action())
start_count = tk.Button(root, text="Count", command=lambda: count(filepath))
error = tk.Label(root, text="")

title.place(x=0, y=0)
file.place(x=0, y=0)
start_count.place(x=0, y=0)
error.place(x=0, y=0)
root.update()
title.place(x=(145 - (title.winfo_width() / 2)), y=0)
label.place(x=0, y=30)
import_file.place(x=230, y=30)
file.place(x=(145 - (file.winfo_width() / 2)), y=33)
start_count.place(x=(145 - (start_count.winfo_width() / 2)), y=80)


root.mainloop()








