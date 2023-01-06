from os import mkdir, path, unlink
from shutil import rmtree

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


def check_if_exists(f_path: str) -> int:
    if path.isfile(f_path):
        unlink(f_path)
    elif path.isdir(f_path):
        rmtree(f_path)
