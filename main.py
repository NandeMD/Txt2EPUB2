import os
from natsort import natsorted
from utils import txt_to_html_p
import jinja2
import shutil


book_title = input("Book title: ")
txt_folder = input("Enter the txt folder path: ")
txts = natsorted(os.listdir(txt_folder))
txts = [f"{txt_folder}/{txt}" for txt in txts]

os.mkdir(book_title)
os.mkdir(f"{book_title}/EPUB")
os.mkdir(f"{book_title}/META-INF")

with open(f"{book_title}/mimetype", "w") as file:
    file.write("application/epub+zip")

chlist = {}

for index, item in enumerate(txts):
    file = open(item, "r")
    chlist[index] = {
        "id": f"id-ch-{index}",
        "name": item.rsplit(".", 1)[0].replace("../RTW/", ""),
        "content": txt_to_html_p(file.read())
    }
    file.close()

with open("chapter.jinja", "r") as file:
    chapter_t = jinja2.Template(file.read())
with open("package.jinja", "r") as file:
    package_t = jinja2.Template(file.read())
with open("toc.jinja", "r") as file:
    toc_t = jinja2.Template(file.read())


pkg_chs = []
pkg_spine = []
toc_chs = []

for key, val in chlist.items():
    ch_x = chapter_t.render(
        {
            "title": val["name"],
            "chid": val["id"],
            "chcontent": val["content"]
        }
    )

    with open(f"{book_title}/EPUB/{val['name']}.xhtml", "w") as file:
        file.write(ch_x)

    pkg_chs.append(
        f'<item id="{val["id"]}" href="{val["name"]}.xhtml" media-type="application/xhtml+xml"/>'
    )
    pkg_spine.append(
        f'<itemref idref="{val["id"]}"/>'
    )
    toc_chs.append(
        f'<li><a href="{val["name"]}.xhtml">{val["name"]}</a></li>'
    )

pkg = package_t.render(
    {
        "title": book_title,
        "chapters": "\n".join(pkg_chs),
        "spine": "\n".join(pkg_spine)
    }
)

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


shutil.make_archive(book_title, "zip", book_title)
shutil.rmtree(book_title)
os.rename(f"{book_title}.zip", f"{book_title}.epub")
