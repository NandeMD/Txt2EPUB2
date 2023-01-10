import sys
import argparse

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
        check = cinput("[WARN]", "magenta", f"There is already a file named '{f_path}' Do you want to overwrite? (y/n): ")
        if check.lower() in ["y", "n"]:
            if check == "n":
                return True
        else:
            cprint("[ERROR]", "red", "Unsupported input char!")
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


def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="TXT2EPUB CLI",
        description="This is a command line interface for Txt2EPUB."
    )
    
    parser.add_argument(
        "input_folder_path",
        help="Path of the folder that contains all the .txt files."
    )
    
    parser.add_argument(
        "book_title",
        help="The name of the outted epub file."
    )
    
    parser.add_argument(
        "-o", "--outpath",
        required=False,
        help="Path to the folder where the files will be extracted to. Defaults to the executable's folder."
    )
    
    parser.add_argument(
        "-y", "--yesall",
        required=False,
        action='store_true',
        help="Considers all (y/n) answers YES."
    )
    
    return parser
