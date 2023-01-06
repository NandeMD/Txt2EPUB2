import os
from natsort import natsorted
from utils import txt_to_html_p, generate_temp_folders, remove_temp_folders
from cprint import cprint
import jinja2
import shutil


# Get the book title and txt folder
book_title = input("Book title: ")
txt_folder = input("Enter the txt folder path: ")

# Sort the txt names with natural order
cprint("[INFO]", "yellow", "Sorting txt names.")
txts = natsorted(os.listdir(txt_folder))

# Generate the txt paths for individual reads
cprint("[INFO]", "yellow", "Generating txt paths.")
txt_paths = []
if txt_folder.endswith("/") or txt_folder.endswith("\\"):
    txt_paths = [f"{txt_folder}{txt}" for txt in txts]
else:
    txt_paths = [f"{txt_folder}/{txt}" for txt in txts]
    
# For the storing of all the generated files before unzipping
cprint("[INFO]", "yellow", "Generating temporary folders.")
generate_temp_folders(book_title)

# Generate the chapter data before writing to xhtml and table of contents 
cprint("[INFO]", "yellow", "Creating chapter data.")
chlist = {}
for index, item in enumerate(txts):
    file = open(txt_paths[index], "r")
    chlist[index] = {
        "id": f"id-ch-{index}",
        "name": item.rsplit(".", 1)[0],
        "content": txt_to_html_p(file.read())
    }
    file.close()

# Initialize all the necessary jinja templates
cprint("[INFO]", "yellow", "Initializing templates.")
with open("chapter.jinja", "r") as file:
    chapter_t = jinja2.Template(file.read())
with open("package.jinja", "r") as file:
    package_t = jinja2.Template(file.read())
with open("toc.jinja", "r") as file:
    toc_t = jinja2.Template(file.read())


pkg_chs = []
pkg_spine = []
toc_chs = []

# Iterate over all the pregenerated chapter data
cprint("[INFO]", "yellow", "Writing chapters.")
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
    with open(f"{book_title}/EPUB/{val['name']}.xhtml", "w") as file:
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

# Render the package file
cprint("[INFO]", "yellow", "Writing package data and table of contents.")
pkg = package_t.render(
    {
        "title": book_title,
        "chapters": "\n".join(pkg_chs),
        "spine": "\n".join(pkg_spine)
    }
)

# Render the table of contents
toc = toc_t.render(
    {
        "title": book_title,
        "toclis": "\n".join(toc_chs)
    }
)

with open(f"{book_title}/EPUB/package.opf", "w") as file:
    file.write(pkg)

with open(f"{book_title}/EPUB/toc.xhtml", "w") as file:
    file.write(toc)

shutil.copy(
    "container.xml",
    f"{book_title}/META-INF/container.xml"
)

# Generate the archive and rename to epub
cprint("[INFO]", "yellow", "Creating epub archive.")
shutil.make_archive(book_title, "zip", book_title)
os.rename(f"{book_title}.zip", f"{book_title}.epub")

remove_temp_folders(book_title)
cprint("[FINISH]", "green", "Done!")
