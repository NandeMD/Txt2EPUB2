import os
import sys
from natsort import natsorted
from pathlib import Path
import utils
from cprint import cprint
import jinja2
import shutil
from time import perf_counter


args = utils.create_arg_parser().parse_args(sys.argv[1:])

# Starting time
t_start = perf_counter()

# Check if an epub or folder already exists, then delete
if utils.check_if_exists(f"{args.book_title}.epub", args.outpath if args.outpath else "", args.yesall):
    t_finish = perf_counter()
    cprint("[DONE]", "green", f"Aborted! Took {round(t_finish-t_start, 2)} seconds.")
    sys.exit(0)
    
# Sort the txt names with natural order
cprint("[INFO]", "yellow", "Sorting txt names.")
try:
    txts = natsorted([f for f in os.listdir(args.input_folder_path) if f.endswith(".txt")])
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while sorting the txt names: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    sys.exit(0)

# Generate the txt paths for individual reads
cprint("[INFO]", "yellow", "Generating txt paths.")
txt_paths = [os.path.join(args.input_folder_path, txt) for txt in txts]

# For the storing of all the generated files before unzipping
try:
    main_temp_folder = ""
    EPUB_folder = ""
    METAINF_folder = ""
    cprint("[INFO]", "yellow", "Generating temporary folders.")
    if args.outpath:
        main_temp_folder, EPUB_folder, METAINF_folder = utils.generate_temp_folders(args.book_title, args.outpath)
    else:
        main_temp_folder, EPUB_folder, METAINF_folder = utils.generate_temp_folders(args.book_title, os.getcwd())
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while creating temporary files: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    sys.exit(0)
    
# Generate the chapter data before writing to xhtml and table of contents 
try:
    cprint("[INFO]", "yellow", "Creating chapter data.")
    chlist = {}
    for index, item in enumerate(txts):
        file = open(txt_paths[index], "r")
        chlist[index] = {
            "id": f"id-ch-{index}",
            "name": item.rsplit(".", 1)[0],
            "content": utils.txt_to_html_p(file.read())
        }
        file.close()
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while generating chapter data: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    shutil.rmtree(main_temp_folder)
    sys.exit(0)
    
# Initialize all the necessary jinja templates
try:
    cprint("[INFO]", "yellow", "Initializing templates.")
    with open(utils.actual_path("chapter.jinja"), "r") as file:
        chapter_t = jinja2.Template(file.read())
    with open(utils.actual_path("package.jinja"), "r") as file:
        package_t = jinja2.Template(file.read())
    with open(utils.actual_path("toc.jinja"), "r") as file:
        toc_t = jinja2.Template(file.read())
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while initializing templates: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    shutil.rmtree(main_temp_folder)
    sys.exit(0)


pkg_chs = []
pkg_spine = []
toc_chs = []

# Iterate over all the pregenerated chapter data
cprint("[INFO]", "yellow", "Writing chapters.")
try:
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
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while writing chapter data: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    shutil.rmtree(main_temp_folder)
    sys.exit(0)
    
try:
    # Render the package file
    cprint("[INFO]", "yellow", "Writing package data and table of contents.")
    pkg = package_t.render(
        {
            "title": args.book_title,
            "chapters": "\n".join(pkg_chs),
            "spine": "\n".join(pkg_spine)
        }
    )

    # Render the table of contents
    toc = toc_t.render(
        {
            "title": args.book_title,
            "toclis": "\n".join(toc_chs)
        }
    )

    with open(os.path.join(EPUB_folder, "package.opf"), "w") as file:
        file.write(pkg)

    with open(os.path.join(EPUB_folder, "toc.xhtml"), "w") as file:
        file.write(toc)

    shutil.copy(
        utils.actual_path("container.xml"),
        os.path.join(METAINF_folder, "container.xml")
    )
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while writing templates: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    shutil.rmtree(main_temp_folder)
    sys.exit(0)

# Generate the archive and rename to epub
try:
    cprint("[INFO]", "yellow", "Creating epub archive.")
    zip_path = shutil.make_archive(os.path.join(args.outpath, args.book_title) if args.outpath else args.book_title, "zip", main_temp_folder)
    out_fp = zip_path.rsplit(".", 1)[0] + ".epub"
    os.rename(zip_path, out_fp)
except Exception as e:
    cprint("[ERROR]", "red", f"An error occured while generating epub archive: {e}!\n"
           f"Aborted! Took {round(perf_counter()-t_start, 2)} seconds.")
    shutil.rmtree(main_temp_folder)
    sys.exit(0)

shutil.rmtree(main_temp_folder)

# Finish time
t_finish = perf_counter()

cprint("[DONE]", "green", f"{out_fp} finished in {round(t_finish-t_start, 2)} seconds!")
