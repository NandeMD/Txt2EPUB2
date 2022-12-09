def txt_to_html_p(txt: str):
    splitted = txt.split("\n\n")
    uwu = []
    uwu.append("<p>")
    for sp in splitted:
        uwu.append(sp)
        uwu.append("</p><p>")

    uwu.append("</p>")
    return "".join(uwu)
    
