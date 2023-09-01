import os
import json
from tkinter import *
from tkinter import ttk
from work_files.dark_title_bar import *
from PIL import ImageTk as img_tk


def file_choose_win(
    file_road,
    catalog,
    name,
    dialog_window,
    work_socket,
    person,
    groups,
    work_files,
    work_folders,
    work_dirs,
):
    catalog = os.getcwd()
    file_now = None

    def past_folder():
        global catalog
        global work_files
        global work_folders
        global work_dirs
        catalog = os.path.dirname(catalog)

        for now_dirs, now_folders, now_files in os.walk(catalog):
            work_dirs = now_dirs
            work_folders = now_folders
            work_files = now_files
            break
        curso_select.delete(0, END)

        for new_files in work_files:
            curso_select.insert(END, new_files)

        for new_folders in work_folders:
            curso_select.insert(END, new_folders)

        folder_info.delete(0, END)
        folder_info.insert(END, catalog)
        folder_info.xview_moveto(1)

    def open_new_file(event):
        global work_files
        global work_folders
        global work_dirs
        global catalog

        len_select_elements = curso_select.curselection()
        cursor_select_var = None

        if len(len_select_elements) > 0:
            cursor_select_var = len_select_elements[0]

        if cursor_select_var is not None:
            for now_dirs, now_folders, now_files in os.walk(catalog):
                work_dirs = now_dirs
                work_folders = now_folders
                work_files = now_files
                break

            if curso_select.get(cursor_select_var) not in work_files:
                if catalog[-1] != "\\":
                    catalog = catalog + "\\" + curso_select.get(cursor_select_var)

                else:
                    catalog = catalog + curso_select.get(cursor_select_var)

                for now_dirs, now_folders, now_files in os.walk(catalog):
                    work_dirs = now_dirs
                    work_folders = now_folders
                    work_files = now_files
                    break
                curso_select.delete(0, END)

                for new_files in work_files:
                    curso_select.insert(END, new_files)

                for new_folders in work_folders:
                    curso_select.insert(END, new_folders)

                folder_info.delete(0, END)
                folder_info.insert(END, catalog)
                folder_info.xview_moveto(1)

    def send_file(file_name_var, file_road_var):
        file_size = (os.stat(file_road_var)).st_size

        dialog_window.insert(END, str(name) + ": " + file_name_var)
        dialog_window.yview_moveto(1)
        if person in groups:
            with open("groups\\" + person + ".txt", "r") as GROUP_STORY:
                lines = GROUP_STORY.readlines()
                persons = lines[0]
                if "\n" in persons:
                    persons = person.split("\n")[0]
                persons = persons.split(",")
                work_socket.send(
                    (
                        json.dumps(
                            {
                                "type": "group_get_file",
                                "text": file_name_var,
                                "from": name,
                                "to": persons,
                                "group": person,
                                "file_size": file_size,
                            }
                        )
                    ).encode("utf8")
                )
        else:
            work_socket.send(
                (
                    json.dumps(
                        {
                            "type": "person_get_file",
                            "text": file_name_var,
                            "from": name,
                            "to": [person],
                            "group": None,
                            "file_size": file_size,
                        }
                    )
                ).encode("utf8")
            )
        file_for_send = open(file_road_var, "rb")

        if file_size > 1024:
            bytes_of_file = file_for_send.read(1024)
            while file_size > 1024:
                work_socket.send(bytes_of_file)
                bytes_of_file = file_for_send.read(1024)
                file_size -= 1024
            work_socket.send(file_for_send.read(file_size))
        else:
            work_socket.send(file_for_send.read(file_size))

        file_for_send.close()

    def select():
        global file_road
        global file_now

        file_road = None
        cursor_now = curso_select.curselection()

        if len(cursor_now) > 0:
            file_now = curso_select.get(cursor_now[0])
            if work_dirs[-1] != "\\":
                file_road = work_dirs + "\\" + file_now
            else:
                file_road = work_dirs + file_now
            send_file(file_now, file_now)
            win.destroy()

    work_files = None
    work_folders = None
    work_dirs = None

    win = Toplevel()
    win.title("Searcher")
    win.geometry("800x600")
    win.resizable(False, False)
    dark_title_bar(win)
    win["bg"] = "#212121"

    sb_work_dirs = Scrollbar(win, orient="vertical")

    searcher_style = ttk.Style()
    searcher_style.theme_use("classic")
    searcher_style.configure(
        "Vertical.TScrollbar",
        background="#3A3A3A",
        troughcolor="#2F2F38",
        activebackground="red",
    )

    curso_select = Listbox(
        win,
        bg="#2F2F38",
        fg="#C1C1C1",
        font=("Rajdhani Regular", 20 * -1),
        selectbackground="#77B5FE",
        selectmode=SINGLE,
        borderwidth=5,
        highlightthickness=5,
        height=22,
        width=40,
        relief=GROOVE,
        bd=0,
        highlightbackground="#3A3A3A",
        highlightcolor="#3A3A3A",
        yscrollcommand=sb_work_dirs.set,
    )

    sb_work_dirs.config(command=curso_select.yview)
    image_back = img_tk.PhotoImage(file="work_files/back_button.png")
    image_select = img_tk.PhotoImage(file="work_files/select_button.png")

    Button(
        win,
        image=image_back,
        command=past_folder,
        relief="flat",
        bg="#3A3A3A",
        activebackground="#212121",
    ).place(x=330, y=538)

    Button(
        win,
        image=image_select,
        command=select,
        relief="flat",
        bg="#3A3A3A",
        activebackground="#212121",
    ).place(x=582, y=538)

    catalog = os.getcwd()

    for dirs, folder, files in os.walk(catalog):
        work_dirs = dirs
        work_folders = folder
        work_files = files
        break

    for new_files in work_files:
        curso_select.insert(END, new_files)

    for new_folders in work_folders:
        curso_select.insert(END, new_folders)

    curso_select.place(x=330, y=0)

    sb_work_dirs.place(x=780, y=0, height=538)

    canvas_for_file_road = Canvas(
        win, width=29, height=56, bg="#2F2F38", bd=0, relief="ridge"
    )
    canvas_for_file_road.config(highlightbackground="#2F2F38", highlightthickness=3)
    canvas_for_file_road.place(x=548, y=538)
    curso_select.bind("<Double-Button-1>", open_new_file)
    sb_file_road = Scrollbar(win, orient="horizontal")
    folder_info = Listbox(
        win,
        height=1,
        width=35,
        bg="#2F2F38",
        bd=0,
        font=("NTR", 15 * -1),
        fg="#77B5FE",
        xscrollcommand=sb_file_road.set,
        highlightbackground="#3A3A3A",
        highlightcolor="#3A3A3A",
    )
    folder_info.place(x=23, y=260)
    sb_file_road.place(x=21, y=280, width=284)
    sb_file_road.config(command=folder_info.xview)
    folder_info.insert(END, catalog)
    folder_info.xview_moveto(1)
    win.mainloop()

    return file_now
