import sys

from os import mkdir, path, unlink
from shutil import rmtree
from cprint import cinput, cprint

def txt_to_html_p(txt: str) -> str:
    splitted = txt.split("\n\n")
    uwu = []
    uwu.append("<p>")
    for sp in splitted:
        uwu.append(sp)
        uwu.append("</p><p>")

    uwu.append("</p>")
    return "".join(uwu)
    

def generate_temp_folders(book_title: str) -> None:
    mkdir(book_title)
    mkdir(f"{book_title}/EPUB")
    mkdir(f"{book_title}/META-INF")

    with open(f"{book_title}/mimetype", "w") as file:
        file.write("application/epub+zip")


def remove_temp_folders(book_title: str) -> None:
    rmtree(book_title)


def check_if_exists(f_path: str) -> bool:
    if path.isfile(f_path):
        check = cinput("[WARN]", "magenta", f"There is already a file named '{f_path}' Do you want to overwrite? (y/n): ")
        if check.lower() in ["y", "n"]:
            if check == "n":
                return True
        else:
            cprint("[ERROR]", "red", "Unsupported input char!")
            return True
        
        unlink(f_path)
    elif path.isdir(f_path):
        rmtree(f_path)
        
    return False


def actual_path(file_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, file_path)
