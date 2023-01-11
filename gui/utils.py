from tkinter import END
from tkinter.ttk import Entry
from tkinter import filedialog as fd
from os import getcwd


def get_folder_path_to_entry(ent: Entry) -> str:
    folder_path = fd.askdirectory()
    if folder_path == () or folder_path == "":
        folder_path = getcwd()
    
    ent.delete(0, END)
    ent.insert(0, folder_path)
    return folder_path
