from threading import Thread
import script_utils
import sys
import os
import shutil
import jinja2
from natsort import natsorted
from tkinter.ttk import Progressbar, Button, Entry
from tkinter.messagebox import showerror, showinfo


def start_thread(book_title_e: Entry, input_folder_path_e: Entry, outpath_e: Entry, pb: Progressbar, buttons: list[Button]) -> None:
    trd = Thread(
        target=do_the_work, 
        args=(book_title_e, input_folder_path_e, outpath_e, pb, buttons),
        daemon=True
    )
    trd.start()


def do_the_work(book_title_e: Entry, input_folder_path_e: Entry, outpath_e: Entry, pb: Progressbar, buttons: list[Button]) -> None:
    pb["value"] = 0
    book_title = book_title_e.get()
    outpath = outpath_e.get()
    input_folder_path = input_folder_path_e.get()
    entries = [book_title_e, input_folder_path_e, outpath_e]
    
    if book_title == "" or book_title == " " or outpath == "" or outpath == " " or input_folder_path == "" or input_folder_path == " ":
        showerror(title="ERROR", message="You need to fill all entries.")
        return
    
    script_utils.set_state_all(buttons + entries, "disabled")
    
    
    # Check if an epub or folder already exists, then delete
    script_utils.check_if_exists(f"{book_title}.epub", outpath if outpath else "", True)
    pb["value"] += 1  # 1
        
    # Sort the txt names with natural order
    try:
        txts = natsorted([f for f in os.listdir(input_folder_path) if f.endswith(".txt")])
        pb["value"] += 9  # 10
    except Exception as e:
        showerror(title="ERROR", message=str(e))
        script_utils.set_state_all(buttons + entries, "normal")
        return

    # Generate the txt paths for individual reads
    txt_paths = [os.path.join(input_folder_path, txt) for txt in txts]
    pb["value"] += 5  # 15

    # For the storing of all the generated files before unzipping
    try:
        main_temp_folder = ""
        EPUB_folder = ""
        METAINF_folder = ""
        if outpath:
            main_temp_folder, EPUB_folder, METAINF_folder = script_utils.generate_temp_folders(book_title, outpath)
        else:
            main_temp_folder, EPUB_folder, METAINF_folder = script_utils.generate_temp_folders(book_title, os.getcwd())
        pb["value"] += 5  # 20
    except Exception as e:
        showerror(title="ERROR", message=f"Error while generating temporary folders: {e}")
        script_utils.set_state_all(buttons + entries, "normal")
        return
        
    # Generate the chapter data before writing to xhtml and table of contents 
    try:
        chlist = {}
        count = len(txts)
        for index, item in enumerate(txts):
            file = open(txt_paths[index], "r")
            chlist[index] = {
                "id": f"id-ch-{index}",
                "name": item.rsplit(".", 1)[0],
                "content": script_utils.txt_to_html_p(file.read())
            }
            file.close()
            pb["value"] += 1/count*20  # 40
    except Exception as e:
        shutil.rmtree(main_temp_folder, ignore_errors=True)
        showerror(title="ERROR", message=f"Error while generating chapter data: {e}")
        script_utils.set_state_all(buttons + entries, "normal")
        return
        
    # Initialize all the necessary jinja templates
    
    with open(script_utils.actual_path("chapter.jinja"), "r") as file:
        chapter_t = jinja2.Template(file.read())
    with open(script_utils.actual_path("package.jinja"), "r") as file:
        package_t = jinja2.Template(file.read())
    with open(script_utils.actual_path("toc.jinja"), "r") as file:
        toc_t = jinja2.Template(file.read())

    pb["value"] += 5  # 45

    pkg_chs = []
    pkg_spine = []
    toc_chs = []

    # Iterate over all the pregenerated chapter data
    try:
        count = len(chlist)
        for val in chlist.values():
            # Render xhtml from the chapter template
            ch_x = chapter_t.render(
                {
                    "title": val["name"],
                    "chid": val["id"],
                    "chcontent": val["content"]
                }
            )

            # Write the xhtml to temporary folder
            with open(os.path.join(EPUB_folder, f"{val['name']}.xhtml"), "w") as file:
                file.write(ch_x)

            # Generate the necessary package, spine and TOC data
            pkg_chs.append(
                f'<item id="{val["id"]}" href="{val["name"]}.xhtml" media-type="application/xhtml+xml"/>'
            )
            pkg_spine.append(
                f'<itemref idref="{val["id"]}"/>'
            )
            toc_chs.append(
                f'<li><a href="{val["name"]}.xhtml">{val["name"]}</a></li>'
            )
            pb["value"] += 1/count*25  # 70
    except Exception as e:
        shutil.rmtree(main_temp_folder)
        showerror(title="ERROR", message=f"Error while writing chapter data: {e}")
        script_utils.set_state_all(buttons + entries, "normal")
        return
        
    try:
        # Render the package file
        pkg = package_t.render(
            {
                "title": book_title,
                "chapters": "\n".join(pkg_chs),
                "spine": "\n".join(pkg_spine)
            }
        )
        pb["value"] += 10  # 80

        # Render the table of contents
        toc = toc_t.render(
            {
                "title": book_title,
                "toclis": "\n".join(toc_chs)
            }
        )
        pb["value"] += 10  # 90

        with open(os.path.join(EPUB_folder, "package.opf"), "w") as file:
            file.write(pkg)

        with open(os.path.join(EPUB_folder, "toc.xhtml"), "w") as file:
            file.write(toc)

        shutil.copy(
            script_utils.actual_path("container.xml"),
            os.path.join(METAINF_folder, "container.xml")
        )
        pb["value"] += 5  # 95
    except Exception as e:
        shutil.rmtree(main_temp_folder)
        showerror(title="ERROR", message=f"Error while writing package and TOC files: {e}")
        script_utils.set_state_all(buttons + entries, "normal")
        return

    # Generate the archive and rename to epub
    try:
        zip_path = shutil.make_archive(os.path.join(outpath, book_title) if outpath else book_title, "zip", main_temp_folder)
        out_fp = zip_path.rsplit(".", 1)[0] + ".epub"
        os.rename(zip_path, out_fp)
        pb["value"] += 4  # 99
    except Exception as e:
        shutil.rmtree(main_temp_folder)
        showerror(title="ERROR", message=f"Error while generating the epub archive: {e}")
        script_utils.set_state_all(buttons + entries, "normal")
        return

    shutil.rmtree(main_temp_folder)
    pb["value"] == 100  # Full
    showinfo(title="Success", message=f"Finished: {out_fp}")
    script_utils.set_state_all(buttons + entries, "normal")
    
