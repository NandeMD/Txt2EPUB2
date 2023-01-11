import sys

from os import mkdir, path, unlink
from shutil import rmtree
from tkinter.ttk import Widget

def txt_to_html_p(txt: str) -> str:
    splitted = txt.split("\n\n")
    uwu = []
    uwu.append("<p>")
    for sp in splitted:
        uwu.append(sp)
        uwu.append("</p><p>")

    uwu.append("</p>")
    return "".join(uwu)
    

def generate_temp_folders(book_title: str, op: str) -> tuple:
    main_temp_folder = path.join(op, book_title)
    EPUB_folder = path.join(main_temp_folder, "EPUB")
    METAINF_folder = path.join(main_temp_folder, "META-INF")
    
    try:
        mkdir(main_temp_folder)
    except FileExistsError:
        rmtree(main_temp_folder)
        mkdir(main_temp_folder)
    try:
        mkdir(EPUB_folder)
    except FileExistsError:
        rmtree(EPUB_folder)
        mkdir(EPUB_folder)
    try:
        mkdir(METAINF_folder)
    except FileExistsError:
        rmtree(METAINF_folder)
        mkdir(METAINF_folder)

    with open(path.join(main_temp_folder, "mimetype"), "w") as file:
        file.write("application/epub+zip")
        
    return main_temp_folder, EPUB_folder, METAINF_folder


def check_if_exists(f_path: str, op: str, yesall) -> bool:
    if path.isfile(f_path if not op else path.join(op, f_path)) and not yesall:
        check = "y"
        if check.lower() in ["y", "n"]:
            if check == "n":
                return True        
        unlink(f_path if not op else path.join(op, f_path))
    elif path.isdir(f_path if not op else path.join(op, f_path)):
        rmtree(f_path if not op else path.join(op, f_path))
        
    return False


def actual_path(file_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, file_path)


def set_state_all(widgets: list[Widget], state: str):
    for widget in widgets:
        widget.configure(state=state)
