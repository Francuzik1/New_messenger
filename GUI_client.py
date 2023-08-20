import sys
from socket import socket
import socket
from threading import Thread
from work_files.dark_title_bar import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import json
from PIL import ImageTk as IT
from vidstream import AudioSender
from vidstream import AudioReceiver
import threading


you_start_call = False
check_call = False
in_call = False
win_wait_call = None
callForPerson = None
call_for_you = None
receiver = None
sender = None
window_of_call_aud = None
name_of_call = None
sub_win_host_port = Tk()

sub_win_host_port.geometry("800x600")
sub_win_host_port.title("Port registration")
sub_win_host_port.configure(bg="#212121")

canvas = Canvas(
    sub_win_host_port,
    bg="#212121",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

entry_image_1 = PhotoImage(
    file="work_files/entry_host.png")
entry_bg_1 = canvas.create_image(
    402.5,
    395.5,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#616161",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=318.0,
    y=382.0,
    width=165.0,
    height=30.0
)

entry_image_2 = PhotoImage(
    file="work_files/entry_port.png")
entry_bg_2 = canvas.create_image(
    402.5,
    473.5,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#616161",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=318.0,
    y=460.0,
    width=165.0,
    height=30.0
)

logo = PhotoImage(
    file="work_files/image_logo.png")
image_logo = canvas.create_image(
    405.0,
    229.0,
    image=logo
)

canvas.create_text(
    336.0,
    350.0,
    anchor="nw",
    text="Enter HOST:",
    fill="#9E9E9E",
    font=("NTR", 24 * -1)
)

canvas.create_text(
    336.0,
    428.0,
    anchor="nw",
    text="Enter PORT:",
    fill="#9E9E9E",
    font=("NTR", 24 * -1)
)

canvas.create_text(
    250.0,
    14.0,
    anchor="nw",
    text="C-Chat",
    fill="#BDBDBD",
    font=("NTR", 96 * -1)
)

canvas.create_text(
    308.0,
    524.0,
    anchor="nw",
    text="Press Enter",
    fill="#BDBDBD",
    font=("NTR", 36 * -1)
)
sub_win_host_port.resizable(False, False)
dark_title_bar(sub_win_host_port)

fileRoad = None
catalog = None
workFiles = None
workFolders = None
workDirs = None


def up_select_win():
    global fileRoad
    global catalog
    catalog = os.getcwd()

    def backer():
        global catalog
        global workFiles
        global workFolders
        global workDirs
        catalog = os.path.dirname(catalog)

        for nowDirs, nowFolders, nowFiles in os.walk(catalog):
            workDirs = nowDirs
            workFolders = nowFolders
            workFiles = nowFiles
            break
        cursorSelect.delete(0, END)

        for newFiles in workFiles:
            cursorSelect.insert(tk.END, newFiles)

        for newFolders in workFolders:
            cursorSelect.insert(tk.END, newFolders)

        folder_info.delete(0, END)
        folder_info.insert(END, catalog)
        folder_info.xview_moveto(1)

    def new_iteration(event):

        global workFiles
        global workFolders
        global workDirs
        global catalog

        lenSelectElements = cursorSelect.curselection()
        cursorSelectVar = None

        if len(lenSelectElements) > 0:
            cursorSelectVar = cursorSelect.curselection()[0]

        if cursorSelectVar is not None:

            for nowDirs, nowFolders, nowFiles in os.walk(catalog):
                workDirs = nowDirs
                workFolders = nowFolders
                workFiles = nowFiles
                break

            if cursorSelect.get(cursorSelectVar) not in workFiles:

                if catalog[-1] != "\\":
                    catalog = catalog + "\\" + cursorSelect.get(cursorSelectVar)

                else:
                    catalog = catalog + cursorSelect.get(cursorSelectVar)

                for nowDirs, nowFolders, nowFiles in os.walk(catalog):
                    workDirs = nowDirs
                    workFolders = nowFolders
                    workFiles = nowFiles
                    break
                cursorSelect.delete(0, END)

                for newFiles in workFiles:
                    cursorSelect.insert(tk.END, newFiles)

                for newFolders in workFolders:
                    cursorSelect.insert(tk.END, newFolders)

                folder_info.delete(0, END)
                folder_info.insert(END, catalog)
                folder_info.xview_moveto(1)

    def road_sign(file_name_var, file_road_var):
        file_road_var = file_road_var.split("\\")
        index_element = r'\''
        index_element = index_element[0]
        file_road_var = index_element.join(file_road_var)
        fileSize = (os.stat(file_road_var)).st_size
        fullNumber1024 = fileSize // 1024
        fileRemainder = fileSize - (fullNumber1024 * 1024)

        dialog_window.insert(END, str(name) + ": " + file_name_var)
        dialog_window.yview_moveto(1)

        if person not in groups:

            work_socket.send(bytes(str(fullNumber1024) + "/fileName" + str(fileRemainder) + "/fileName" + file_name_var
                                   + "/fileName" + str(name), "utf8"))

            if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt") is False:

                file = open("story\\" + str(name) + " " + str(person) + ".txt", "lenSelectElements")
                file.write(str(name) + ": " + file_name_var)
                file.close()

            else:

                file = open("story\\" + str(name) + " " + str(person) + ".txt", "a")
                file.write("\n" + str(name) + ": " + file_name_var)
                file.close()

        else:

            work_socket.send(bytes(str(fullNumber1024) + "/file_group" + str(fileRemainder) + "/file_group" + file_name_var
                                   + "/file_group" + str(name) + "/file_group" + str(person), "utf8"))

            if os.path.exists("groups\\" + str(person) + ".txt") is False:

                file = open("groups\\" + str(person) + ".txt", "lenSelectElements")
                file.write(str(name) + ": " + file_name_var)
                file.close()

            else:

                file = open("groups\\" + str(person) + ".txt", "a")
                file.write("\n" + str(name) + ": " + file_name_var)
                file.close()

        fileRead = open(file_road_var, "rb")
        fileInfoPortion = fileRead.read(1024)

        while fileInfoPortion:
            work_socket.send(fileInfoPortion)
            fileInfoPortion = fileRead.read(1024)

        fileRead.close()

    def select():
        global fileRoad

        fileRoad = None
        cv = cursorSelect.curselection()

        if len(cv) > 0:
            fileRoad = cursorSelect.get(cv[0])
            fileName = fileRoad

            if workDirs[-1] != "\\":
                fileRoad = workDirs + "\\" + fileRoad

            else:
                fileRoad = workDirs + fileRoad

            road_sign(fileName, fileRoad)
            win.destroy()

    workFiles = None
    workFolders = None
    workDirs = None

    win = Toplevel()
    win.title("Searcher")
    win.geometry("800x600")
    win.resizable(False, False)
    dark_title_bar(win)
    win["bg"] = "#212121"

    sb_WorkDirs = ttk.Scrollbar(win, orient='vertical')

    searcher_style = ttk.Style()
    searcher_style.theme_use('classic')
    searcher_style.configure("Vertical.TScrollbar", background="#3A3A3A", troughcolor="#2F2F38", activebackground="red")

    cursorSelect = tk.Listbox(win, bg="#2F2F38", fg="#C1C1C1", font=("Rajdhani Regular", 20 * -1),
                          selectbackground="#77B5FE", selectmode=SINGLE, borderwidth=5, highlightthickness=5,
                          height=22, width=40, relief=GROOVE, bd=0, highlightbackground="#3A3A3A",
                          highlightcolor="#3A3A3A", yscrollcommand=sb_WorkDirs.set)

    sb_WorkDirs.config(command=cursorSelect.yview)
    image_back = IT.PhotoImage(file="work_files/back_button.png")
    image_select = IT.PhotoImage(file="work_files/select_button.png")

    tk.Button(win, image=image_back, command=backer, relief='flat',
              bg="#3A3A3A", activebackground="#212121").place(x=330, y=538)

    tk.Button(win, image=image_select, command=select, relief='flat',
              bg="#3A3A3A", activebackground="#212121").place(x=582, y=538)

    catalog = os.getcwd()

    for dirs, folder, files in os.walk(catalog):
        workDirs = dirs
        workFolders = folder
        workFiles = files
        break

    for new_files in workFiles:
        cursorSelect.insert(tk.END, new_files)

    for new_folders in workFolders:
        cursorSelect.insert(tk.END, new_folders)

    cursorSelect.place(x=330, y=0)

    sb_WorkDirs.place(x=780, y=0, height=538)

    Canvas_for_file_road = Canvas(win, width=29, height=56, bg="#2F2F38", bd=0, relief='ridge')
    Canvas_for_file_road.config(highlightbackground="#2F2F38", highlightthickness=3)
    Canvas_for_file_road.place(x=548, y=538)
    cursorSelect.bind("<Double-Button-1>", new_iteration)
    sb_file_road = ttk.Scrollbar(win, orient='horizontal')
    folder_info = Listbox(win, height=1, width=35, bg="#2F2F38", bd=0, font=("NTR", 15 * -1), fg="#77B5FE",
                           xscrollcommand=sb_file_road.set, highlightbackground="#3A3A3A", highlightcolor="#3A3A3A")
    folder_info.place(x=23, y=260)
    sb_file_road.place(x=21, y=280, width=284)
    sb_file_road.config(command=folder_info.xview)
    folder_info.insert(END, catalog)
    folder_info.xview_moveto(1)
    win.mainloop()

    return fileRoad


def host_port_e(event):
    host_port()


def host_port():
    try:
        HOST = str(entry_1.get())
        PORT = int(entry_2.get())

        data = {
            "SERVER_HOST": HOST,
            "SERVER_PORT": PORT
        }
        with open('config.json', 'w') as outfile:
            json.dump(data, outfile)

        sub_win_host_port.destroy()

    except Exception as k:
        entry_1.delete(0, END)
        entry_2.delete(0, END)


sub_win_host_port.bind("<Return>", host_port_e)
sub_win_host_port.mainloop()

with open('config.json') as f:
    templates = json.load(f)

SERVER_HOST = templates["SERVER_HOST"]
SERVER_PORT = templates["SERVER_PORT"]

work_socket = socket.socket()

try:
    work_socket.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(e)
    sys.exit()

clientList = []

groupMode = False

msg = work_socket.recv(1024).decode("utf8")

split_msg = msg.split(" ")

registration_client_list = split_msg[1].split(",")

person = None

if os.path.exists("story") is False:
    os.mkdir("story")

if os.path.exists("groups") is False:
    os.mkdir("groups")

if os.path.exists("send_files") is False:
    os.mkdir("send_files")

if os.path.exists("sent") is False:
    os.mkdir("sent")

groups = []
msg = None


# receiver
def incoming_calls():
    global in_call
    global check_call
    global msg
    global call_for_you
    global receiver
    global sender
    global name_of_call
    global window_of_call_aud

    if check_call is True:
        check_call = False
        msg = msg.split("/start_audio/")
        call_from_name = msg[2]
        name_of_call = call_from_name
        call_host = msg[1]
        call_for_you = Toplevel()
        call_for_you.geometry("600x700")
        call_for_you.resizable(False, False)
        call_for_you.title("Audio call")
        call_for_you.configure(bg="#212121")
        dark_title_bar(call_for_you)

        image_yes_call = IT.PhotoImage(file="work_files/yes_call.png")
        image_no_call = IT.PhotoImage(file="work_files/no_call.png")
        image_photo_call = IT.PhotoImage(file="work_files/def_user.png")

        def yes_call():

            global sender
            global receiver
            global window_of_call_aud
            global name_of_call

            MY_WORK_HOST = socket.gethostbyname(socket.gethostname())
            YOUR_WORK_HOST = call_host

            work_socket.send(bytes(call_from_name + "/yes_call/" + str(name) + "/yes_call/" + MY_WORK_HOST, "utf8"))

            receiver = AudioReceiver(MY_WORK_HOST, 9999)
            receiver_thread = threading.Thread(target=receiver.start_server)

            sender = AudioSender(YOUR_WORK_HOST, 5555)
            send_thread = threading.Thread(target=sender.start_stream)

            receiver_thread.start()
            send_thread.start()
            call_for_you.destroy()
            window_of_call_aud = Toplevel()
            window_of_call_aud.geometry("600x700")
            window_of_call_aud.resizable(False, False)
            window_of_call_aud.title("Audio call")
            window_of_call_aud.configure(bg="#212121")
            dark_title_bar(window_of_call_aud)

            who_talk_img = Label(window_of_call_aud, image=image_photo_call, bg="#212121",
                                 activebackground="#212121")
            who_talk_img.image = image_photo_call
            who_talk_img.place(x=250, y=100)

            person_call = Canvas(window_of_call_aud, bg="#2F2F38", width=596, height=40, borderwidth=0,
                                 bd=0,
                                 highlightbackground="#3A3A3A")
            person_call.place(x=0, y=200)
            person_call.create_text(298, 20, text=call_from_name, fill="#9E9E9E", font=("NTR", 24 * -1))

            image_off_call = IT.PhotoImage(file="work_files/off_audio_call.png")

            def stop_call_now():
                window_of_call_aud.destroy()
                sender.stop_stream()
                work_socket.send(bytes(name_of_call + "/stop_sender/" + name, "utf8"))

            Button(window_of_call_aud, image=image_off_call, command=stop_call_now, relief='flat',
                   bg="#212121",
                   activebackground="#212121").place(x=260, y=575)

            window_of_call_aud.mainloop()

        def no_call():
            call_for_you.destroy()
            work_socket.send(bytes(call_from_name + "/stop_call_me/", "utf8"))

        Button(call_for_you, image=image_yes_call, command=yes_call,
               relief='flat', bg="#212121", activebackground="#212121").place(x=0, y=575)
        Button(call_for_you, image=image_no_call, command=no_call,
               relief='flat', bg="#212121", activebackground="#212121").place(x=515, y=575)

        Label(call_for_you, image=image_photo_call, bg="#212121", activebackground="#212121").place(x=250, y=100)

        who_call = Canvas(call_for_you, bg="#2F2F38", width=596, height=40, borderwidth=0, bd=0,
                          highlightbackground="#3A3A3A")
        who_call.place(x=0, y=200)
        who_call.create_text(298, 20, text=call_from_name, fill="#9E9E9E", font=("NTR", 24 * -1))

        Thread(target=incoming_calls, daemon=True).start()
        call_for_you.mainloop()

    elif in_call is True:
        in_call = False
        # sender

        msg = msg.split("/yes_call/")
        MY_HOST = socket.gethostbyname(socket.gethostname())
        YOUR_HOST = msg[2]
        name_of_call = msg[1]
        receiver = AudioReceiver(MY_HOST, 5555)
        receiver_thread = threading.Thread(target=receiver.start_server)

        sender = AudioSender(YOUR_HOST, 9999)
        sender_thread = threading.Thread(target=sender.start_stream)

        receiver_thread.start()
        sender_thread.start()

        window_of_call_aud = Toplevel()
        window_of_call_aud.geometry("600x700")
        window_of_call_aud.resizable(False, False)
        window_of_call_aud.title("Audio call")
        window_of_call_aud.configure(bg="#212121")
        dark_title_bar(window_of_call_aud)

        image_photo_call = IT.PhotoImage(file="work_files/def_user.png")

        Label(window_of_call_aud, image=image_photo_call, bg="#212121", activebackground="#212121").place(
            x=250, y=100)

        who_call = Canvas(window_of_call_aud, bg="#2F2F38", width=596, height=40, borderwidth=0, bd=0,
                          highlightbackground="#3A3A3A")
        who_call.place(x=0, y=200)
        who_call.create_text(298, 20, text=name_of_call, fill="#9E9E9E", font=("NTR", 24 * -1))

        image_off_call = IT.PhotoImage(file="work_files/off_audio_call.png")

        def stop_call_now():
                work_socket.send(bytes(name_of_call + "/stop_call_other/", "utf8"))

        Button(window_of_call_aud, image=image_off_call, command=stop_call_now, relief='flat',
               bg="#212121",
               activebackground="#212121").place(x=260, y=575)

        Thread(target=incoming_calls, daemon=True).start()
        window_of_call_aud.mainloop()

    main_win.after(1000, incoming_calls)


def receive():
    global clientList
    global msg
    global check_call
    global in_call
    global you_start_call
    global name_of_call

    utfMode = True
    full_number = None
    other_number = None
    sendFile = None

    while True:
        try:
            if utfMode is True:

                msg = work_socket.recv(1024).decode("utf8")
                print(msg)

                if "/new_client_list " in msg:
                    split_msg = msg.split(" ")
                    clientList = split_msg[1].split(",")
                    person_list.delete(0, END)

                    if name in clientList:
                        clientList.remove(str(name))

                    for i in clientList:
                        person_list.insert(0, i)

                elif "/create_new_group " in msg:
                    msg = msg.split(" ")[1]
                    msg = msg.split(",")
                    name_of_group = msg.pop(0)
                    fileGroup = open("groups\\" + name_of_group + ".txt", "w")
                    fileGroup.write(",".join(msg))
                    fileGroup.close()
                    groups.append(name_of_group)
                    person_list.insert(0, name_of_group)

                elif "mes_group" in msg:
                    msg = msg.split("mes_group")
                    GroupNow = msg[0]
                    msg = msg[1]
                    fileGroup = open("groups\\" + GroupNow + ".txt", "a")
                    fileGroup.write("\n" + msg)
                    fileGroup.close()
                    if GroupNow == person:
                        dialog_window.insert(END, msg)
                        dialog_window.yview_moveto(1)

                elif "/abpers" in msg:
                    msg = msg.split("/abpers")[1]
                    msg_from = msg.split(":")[0]

                    if msg_from == person or msg_from == name:
                        dialog_window.insert(END, msg)
                        dialog_window.yview_moveto(1)

                    if msg_from != name and msg_from != person:

                        if os.path.exists("story\\" + str(name) + " " + str(msg_from) + ".txt") is False:
                            file = open("story\\" + str(name) + " " + str(msg_from) + ".txt", "w")
                            file.write(msg)
                            file.close()

                        else:
                            file = open("story\\" + str(name) + " " + str(msg_from) + ".txt", "a")
                            file.write("\n" + msg)
                            file.close()

                    else:
                        if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt") is False:
                            file = open("story\\" + str(name) + " " + str(person) + ".txt", "w")
                            file.write(msg)
                            file.close()

                        else:
                            file = open("story\\" + str(name) + " " + str(person) + ".txt", "a")
                            file.write("\n" + msg)
                            file.close()

                elif "/file_name" in msg:
                    msg = msg.split("/file_name")
                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    file_from = str(msg[3])

                    if file_from == person:
                        dialog_window.insert(END, str(file_from) + ": " + msg[2])
                        dialog_window.yview_moveto(1)

                    if os.path.exists("story\\" + str(name) + " " + str(file_from) + ".txt") is False:

                        file = open("story\\" + str(name) + " " + str(file_from) + ".txt", "w")
                        file.write(str(file_from) + ": " + msg[2])
                        file.close()

                    else:

                        file = open("story\\" + str(name) + " " + str(file_from) + ".txt", "a")
                        file.write("\n" + str(file_from) + ": " + msg[2])
                        file.close()

                    sendFile = open('sent/' + msg[2], 'wb')

                    utfMode = False

                elif "/fileGroup" in msg:

                    msg = msg.split("/fileGroup")

                    if msg[4] == person:
                        dialog_window.insert(END, msg[3] + ": " + msg[2])
                        dialog_window.yview_moveto(1)

                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    file_from_name = str(msg[3])
                    file_from_group = str(msg[4])
                    file = open("groups\\" + file_from_group + ".txt", "a")
                    file.write("\n" + str(file_from_name) + ": " + msg[2])
                    file.close()
                    sendFile = open('sent/' + msg[2], 'wb')

                    utfMode = False

                elif "/start_audio/" in msg:

                    check_call = True

                elif "/yes_call/" in msg:

                    if you_start_call is True:
                        you_start_call = False
                        win_wait_call.destroy()

                    in_call = True
                elif "/stop_calling/" in msg:

                    call_for_you.destroy()

                elif "/stop_sender/" in msg:

                    msg = msg.split("/stop_sender/")
                    sender.stop_stream()
                    work_socket.send(bytes(msg[1] + "/stop_reciver/" + msg[0], "utf8"))

                elif "/stop_reciver/" in msg:

                    msg = (msg.split("/stop_reciver/"))[1]
                    receiver.stop_server()
                    work_socket.send(bytes(msg + "/stop_last_recive/", "utf8"))

                    window_of_call_aud.destroy()

                elif "/stop_last_recive/" in msg:

                    window_of_call_aud.destroy()
                    receiver.stop_server()

                elif "/stop_call_me" in msg:

                    in_call = False
                    you_start_call = False
                    win_wait_call.destroy()

                elif "/stop_call_other/" in msg:

                    window_of_call_aud.destroy()
                    sender.stop_stream()
                    work_socket.send(bytes(name_of_call + "/stop_sender/" + name, "utf8"))

                else:

                    while full_number != 0:
                        msg = work_socket.recv(1024)
                        sendFile.write(msg)
                        full_number -= 1

                    if other_number != 0:
                        msg = work_socket.recv(int(other_number))
                        sendFile.write(msg)

                    sendFile.close()

                    utfMode = True

        except OSError:
            break


listOfGroup = []


def new_dialog(event):
    global image_base_user
    global person
    global listOfGroup
    global groupMode
    global canvas_person

    if groupMode is False and person_list.get(person_list.curselection()[0]) not in groups and person_list.get(
            person_list.curselection()[0]) != person:

        image_base_user = IT.PhotoImage(file="work_files/def_user.png")

        base_photo = Label(image=image_base_user, bg="#212121")
        base_photo.place(x=398, y=1)

        dialog_window.delete(0, END)

        person = person_list.get(person_list.curselection()[0])
        canvas_who_talk.itemconfigure(canvas_person, text=person)

        if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt"):

            file = open("story\\" + str(name) + " " + str(person) + ".txt", "r")
            oldString = file.readlines()

            for i in oldString:
                dialog_window.insert(END, i)

            dialog_window.yview_moveto(1)

        def send_e(event):
            send()

        def send():

            mes = entry_send.get()

            if mes is not None and mes != "" and person is not None and person != "":
                work_socket.send(bytes(str(name + "abpers" + mes + "abpers" + person), "utf8"))
                entry_send.delete(0, END)
                dialog_window.yview_moveto(1)

        def send_file():

            work_socket.send(bytes(str(name) + "/talk_person" + person, "utf8"))
            up_select_win()

        def start_audio():

            global win_wait_call
            global you_start_call
            global callForPerson
            you_start_call = True
            callForPerson = person

            work_socket.send(bytes(str(person + "/start_audio/" + socket.gethostbyname(socket.gethostname())) +
                         "/start_audio/" + str(name), "utf8"))

            win_wait_call = Toplevel()
            win_wait_call.geometry("600x700")
            win_wait_call.resizable(False, False)
            win_wait_call.title("Wait")
            win_wait_call.configure(bg="#212121")
            dark_title_bar(win_wait_call)

            image_off_call = IT.PhotoImage(file="work_files/off_audio_call.png")
            image_photo_call = IT.PhotoImage(file="work_files/def_user.png")

            Label(win_wait_call, image=image_photo_call, bg="#212121", activebackground="#212121").place(x=250, y=100)

            whoCall = Canvas(win_wait_call, bg="#2F2F38", width=596, height=40, borderwidth=0, bd=0,
                              highlightbackground="#3A3A3A")
            whoCall.place(x=0, y=200)
            whoCall.create_text(298, 20, text=person, fill="#9E9E9E", font=("NTR", 24 * -1))

            def stop_calling():
                win_wait_call.destroy()
                work_socket.send(bytes(callForPerson + "/stop_calling/", "utf8"))

            Button(win_wait_call, image=image_off_call, command=stop_calling, relief='flat', bg="#212121",
                   activebackground="#212121").place(x=260, y=575)

            Label(win_wait_call, text="Wait...", bg="#212121", activebackground="#212121", fg="#9E9E9E",
                  font=("NTR", 40 * -1)).place(x=250, y=500)

            win_wait_call.mainloop()

        main_win.bind("<Return>", send_e)

        tk.Button(main_win, image=image_send_msg, command=send,
                  relief='flat', bg="#212121", activebackground="#212121").place(x=910, y=680)

        tk.Button(main_win, image=image_send_file, command=send_file,
                  relief='flat', bg="#212121", activebackground="#212121").place(x=965, y=680)

        Button(main_win, image=image_audio_call, command=start_audio,
               relief='flat', bg="#212121", activebackground="#212121").place(x=904, y=0)

        Button(main_win, image=image_video_call, command=lambda: print(),
               relief='flat', bg="#212121", activebackground="#212121").place(x=1090, y=0)

        entry_send = Entry(
            bd=0,
            bg="#393944",
            fg="#C1C1C1",
            font=("Rajdhani Regular", 24 * -1),
            highlightthickness=0
        )
        entry_send.place(
            x=400.0,
            y=685.0,
            width=505.0,
            height=35.0
        )

    elif person_list.get(person_list.curselection()[0]) in groups and groupMode is False and person_list.get(
            person_list.curselection()[0]) != person:

        image_base_user = IT.PhotoImage(file="work_files/def_group.png")
        base_photo = Label(image=image_base_user, bg="#212121")
        base_photo.place(x=398, y=1)
        dialog_window.delete(0, END)

        person = person_list.get(person_list.curselection()[0])
        canvas_who_talk.itemconfigure(canvas_person, text=person)

        file = open("groups\\" + person + ".txt", "r")
        oldString = file.readlines()
        oldString.pop(0)

        for i in oldString:
            dialog_window.insert(END, i)

        def send_e_g(event):
            send_g()

        def send_g():
            mes = entry_send.get()

            if mes is not None and mes != "" and person is not None and person != "":
                with open("groups\\" + person + ".txt", "r") as f:
                    lines = f.readlines()
                    persons = lines[0]
                work_socket.send(bytes(str(person + "mes_group" + persons + "mes_group" + str(name) + ": " + mes), "utf8"))
            entry_send.delete(0, END)
            dialog_window.yview_moveto(1)

        def send_file_group():

            with open("groups\\" + person + ".txt", "r") as groupStory:
                lines = groupStory.readlines()
                persons = lines[0]
            work_socket.send(bytes(str(name) + "/talk_group" + person + "/talk_group" + persons, "utf8"))

            up_select_win()

        main_win.bind("<Return>", send_e_g)

        tk.Button(main_win, image=image_send_msg, command=send_g,
                  relief='flat', bg="#212121", activebackground="#212121").place(x=910, y=680)

        tk.Button(main_win, image=image_send_file, command=send_file_group,
                  relief='flat', bg="#212121", activebackground="#212121").place(x=965, y=680)

        entry_send = Entry(
            bd=0,
            bg="#393944",
            fg="#C1C1C1",
            font=("Rajdhani Regular", 24 * -1),
            highlightthickness=0
        )
        entry_send.place(
            x=400.0,
            y=685.0,
            width=505.0,
            height=35.0
        )

    else:

        if groupMode is True:

            if dialog_window.get(0) != "Your group: ":
                dialog_window.delete(0, END)
                dialog_window.insert(0, "Your group: ")
            group_person = person_list.get(person_list.curselection()[0])

            if group_person not in listOfGroup and group_person not in groups:
                listOfGroup.append(group_person)
                dialog_window.insert(END, group_person)

            def create_group():
                win_name_group = Toplevel()
                win_name_group.geometry('200x150')
                win_name_group.configure(bg="#212121")
                Label(win_name_group, bg="#212121", text="Enter name of your group: ", fg="#77B5FE").pack()
                group_name = Entry(win_name_group, bg="#616161")
                group_name.pack()

                def create_new_group():
                    global groupMode
                    global listOfGroup

                    if group_name.get() not in groups:
                        group_name_var = group_name.get()
                        groups.append(group_name_var)
                        g_file = open("groups\\" + group_name_var + ".txt", "w")
                        g_file.write(name + "," + ",".join(listOfGroup))
                        g_file.close()
                        person_list.insert(0, group_name_var)
                        dialog_window.delete(0, END)
                        groupMode = False
                        work_socket.send(
                            bytes(
                                "/create_new_group " + group_name_var + "," + str(name) + "," + ",".join(listOfGroup),
                                "utf8"))
                        listOfGroup = []
                        btn_send.destroy()
                        win_name_group.destroy()

                tk.Button(win_name_group, text="OK", command=create_new_group, bg="#212121", fg="#77B5FE").pack()
                dark_title_bar(win_name_group)

            if len(listOfGroup) >= 2:
                image_create = IT.PhotoImage(file="work_files/create_button.png")
                btn_send = tk.Button(main_win, image=image_create, command=create_group,
                                     relief='flat', bg="#3A3A3A", activebackground="#212121")
                btn_send.image = image_create
                btn_send.place(x=1062, y=668)


def new_group():
    global groupMode
    groupMode = True


def sub_close_e(event):
    sub_close()


def sub_close():
    global name
    name = entry.get()

    if name != "" and name not in registration_client_list and " " not in name:
        work_socket.send(bytes(name, "utf8"))
        sub_win.destroy()

    elif name in registration_client_list:
        xys = tk.Label(sub_win, text="login already exists", bg="#212121", foreground="red")
        xys.place(x=360, y=360)
        xys.destroy()

    elif " " in name or "," in name:
        xyz = tk.Label(sub_win, text="wrong character", bg="#212121", foreground="red")
        xyz.place(x=360, y=380)
        xyz.destroy()


name = None
sub_win = Tk()

sub_win.geometry("800x600")
sub_win.configure(bg="#212121")

canvas = Canvas(
    sub_win,
    bg="#212121",
    height=600,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    285.0,
    10.0,
    anchor="nw",
    text="C-Chat",
    fill="#BDBDBD",
    font=("NTR", 64 * -1)
)

canvas.create_text(
    300.0,
    235.0,
    anchor="nw",
    text="Enter your login:",
    fill="#9E9E9E",
    font=("NTR", 32 * -1)
)

entry_image_1 = PhotoImage(
    file="work_files/entry_login.png")
entry_bg_1 = canvas.create_image(
    413.5,
    316.5,
    image=entry_image_1
)
entry = Entry(
    bd=0,
    bg="#616161",
    fg="#000716",
    highlightthickness=0
)
entry.place(
    x=329.0,
    y=300.0,
    width=169.0,
    height=31.0
)

canvas.create_text(
    340.0,
    428.0,
    anchor="nw",
    text="Press Enter",
    fill="#BDBDBD",
    font=("NTR", 28 * -1)
)

image_image_1 = PhotoImage(
    file="work_files/small_logo.png")
image_1 = canvas.create_image(
    523.0,
    39.0,
    image=image_image_1
)

sub_win.resizable(False, False)
dark_title_bar(sub_win)
sub_win.bind("<Return>", sub_close_e)
sub_win.mainloop()

main_win = Tk()
main_win.geometry("500x500")
main_win.title("Chats")

sb_persons = ttk.Scrollbar(main_win, orient='vertical')

style = ttk.Style()
style.theme_use('classic')
style.configure("Vertical.TScrollbar", background="#3A3A3A", troughcolor="#2F2F38", activebackground="red")

image_create_group = IT.PhotoImage(file="work_files/new.png")
image_send_msg = IT.PhotoImage(file="work_files/plane.png")
image_send_file = IT.PhotoImage(file="work_files/x_file.png")
image_base_user = IT.PhotoImage(file="work_files/def_user.png")
image_audio_call = IT.PhotoImage(file="work_files/audio.png")
image_video_call = IT.PhotoImage(file="work_files/video.png")

person_list = tk.Listbox(main_win, bg="#2F2F38", fg="#C1C1C1", font=("Rajdhani Regular", 20 * -1),
                         selectbackground="#77B5FE", selectmode=SINGLE, borderwidth=5, highlightthickness=5,
                         height=20, width=15, relief=GROOVE, bd=0, highlightbackground="#3A3A3A",
                         highlightcolor="#3A3A3A", yscrollcommand=sb_persons.set)

person_list.bind("<Double-Button-1>", new_dialog)

sb_persons.config(command=person_list.yview)
sb_persons.place(x=175, y=173, height=490)

person_list.place(x=0, y=173)
dark_title_bar(main_win)
main_win["bg"] = "#212121"

Button(main_win, image=image_create_group, command=new_group,
       relief='flat', bg="#3A3A3A", activebackground="#212121").place(x=0, y=663)

image_of_user = Label(image=image_base_user, bg="#212121")
image_of_user.place(x=398, y=1)

canvas_who_talk = Canvas(width=401, height=91, bg="#2F2F38", bd=0, relief='ridge')
canvas_who_talk.config(highlightbackground="#3A3A3A", highlightthickness=3)
canvas_who_talk.place(x=498, y=3)
canvas_person = canvas_who_talk.create_text(200, 50, text="", fill="#C8C8C9", font=('NTR 24'))

sb_dialog = ttk.Scrollbar(main_win, orient='vertical')

dialog_window = tk.Listbox(main_win, bg="#2F2F38", fg="#C1C1C1", font=("Rajdhani Regular", 20 * -1),
                           selectbackground="#77B5FE", selectmode=SINGLE, borderwidth=5, highlightthickness=5,
                           height=23, width=43, relief=GROOVE, bd=0, highlightbackground="#3A3A3A",
                           highlightcolor="#3A3A3A", yscrollcommand=sb_dialog.set)

sb_dialog.config(command=dialog_window.yview)
sb_dialog.place(x=885, y=102, height=558)

dialog_window.place(x=400, y=98)

receive_thread = Thread(target=receive, daemon=True)
receive_thread.start()

if name is not None or name != "":
    def user_exit():
        work_socket.send(bytes("/user_exit " + str(name), "utf8"))
        sys.exit()


    main_win.protocol("WM_EXIT", user_exit)
    incoming_calls()
    main_win.mainloop()

work_socket.close()
