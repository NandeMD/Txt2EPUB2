from tkinter import Tk, Frame, END, PhotoImage
from tkinter.ttk import Progressbar, Label, Entry, Button
from os import getcwd
from utils import get_folder_path_to_entry
from script_utils import actual_path
import scripts


root_window = Tk()
root_window.title("TXT2EPUB")
root_window.geometry("500x180")

icon = PhotoImage(file=actual_path("icon.png"))
root_window.tk.call('wm', 'iconphoto', root_window._w, icon)

input_frame = Frame(master=root_window)
name_frame = Frame(master=root_window)
output_frame = Frame(master=root_window)

input_l = Label(master=input_frame, text="Input Folder:")
input_l.grid(column=0, row=0, padx=2, pady=12)

input_e = Entry(master=input_frame, width=38)
input_e.grid(column=1, row=0, padx=2, pady=12)

input_b = Button(master=input_frame, text="Open", command=lambda:get_folder_path_to_entry(input_e))
input_b.grid(column=2, row=0, padx=2, pady=12)

input_frame.grid(column=0, row=0, padx=5)

out_l = Label(master=output_frame, text="Output Folder:")
out_l.grid(column=0, row=0, padx=2, pady=12)

out_e = Entry(master=output_frame, width=36)
out_e.grid(column=1, row=0, padx=2, pady=12)
out_e.delete(0, END)
out_e.insert(0, getcwd())

out_b = Button(master=output_frame, text="Open", command=lambda:get_folder_path_to_entry(out_e))
out_b.grid(column=2, row=0, padx=2, pady=12)

output_frame.grid(column=0, row=1, padx=5)

name_l = Label(master=name_frame, text="Output Name:")
name_l.grid(column=0, row=0, padx=2, pady=6)

name_e = Entry(master=name_frame, width=20)
name_e.grid(column=1, row=0, padx=2, pady=6)

pbar = Progressbar(master=root_window, orient="horizontal", mode="determinate", length=430, maximum=100)

start_b = Button(master=name_frame, text="Start", command=lambda:scripts.start_thread(name_e, input_e, out_e, pbar, [input_b, out_b, start_b]))
start_b.grid(column=2, row=0, padx=2, pady=6)

name_frame.grid(column=0, row=2, padx=5)


pbar.grid(column=0, row=3, padx=2, pady=6)



if __name__ == "__main__":
    root_window.mainloop()