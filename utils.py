from os import mkdir
from shutil import rmtree

def txt_to_html_p(txt: str):
    splitted = txt.split("\n\n")
    uwu = []
    uwu.append("<p>")
    for sp in splitted:
        uwu.append(sp)
        uwu.append("</p><p>")

    uwu.append("</p>")
    return "".join(uwu)
    

def generate_temp_folders(book_title: str):
    mkdir(book_title)
    mkdir(f"{book_title}/EPUB")
    mkdir(f"{book_title}/META-INF")

    with open(f"{book_title}/mimetype", "w") as file:
        file.write("application/epub+zip")


def remove_temp_folders(book_title: str):
    rmtree(book_title)
