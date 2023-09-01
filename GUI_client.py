import sys
import time
from socket import socket
import socket
from threading import Thread
from work_files.dark_title_bar import *
import tkinter as tk
from tkinter import *
from tkinter import ttk
import os
import json
from PIL import ImageTk as img_tk
from file_choose import file_choose_win

from vidstream import AudioSender
from vidstream import AudioReceiver
import threading


def main():
    init_work_files()
    init_host_port()
    init_socket()
    init_login()
    chat_window()


you_start_call = False
check_call_for_you = False
agree_for_start_call = False
canvas_person = None
image_create_group = None
win_wait_call = None
main_win = None
name = None
call_for_person = None
call_for_you = None
receiver = None
sender = None
window_of_call_aud = None
name_of_call = None
file_now = None
catalog = None
work_files = None
work_folders = None
canvas_who_talk = None
work_dirs = None
msg = None
create_group_mode = False
person = None
SERVER_HOST = None
SERVER_PORT = None
work_socket = None
image_send_msg = None
image_send_file = None
image_audio_call = None
image_default_user = None
person_list = None
image_video_call = None
dialog_window = None
groups = []
list_of_group = []


def init_work_files():
    new_files = ["story", "groups", "send_files", "sent"]
    for init_files in new_files:
        if os.path.exists(init_files) is False:
            os.mkdir(init_files)


def init_host_port():
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
        relief="ridge",
    )
    canvas.place(x=0, y=0)

    entry_image_1 = PhotoImage(file="work_files/entry_host.png")
    canvas.create_image(402.5, 395.5, image=entry_image_1)
    entry_1 = Entry(bd=0, bg="#616161", fg="#000716", highlightthickness=0)
    entry_1.place(x=318.0, y=382.0, width=165.0, height=30.0)

    entry_image_2 = PhotoImage(file="work_files/entry_port.png")
    canvas.create_image(402.5, 473.5, image=entry_image_2)
    entry_2 = Entry(bd=0, bg="#616161", fg="#000716", highlightthickness=0)
    entry_2.place(x=318.0, y=460.0, width=165.0, height=30.0)

    logo = PhotoImage(file="work_files/image_logo.png")
    canvas.create_image(405.0, 229.0, image=logo)

    canvas.create_text(
        336.0,
        350.0,
        anchor="nw",
        text="Enter HOST:",
        fill="#9E9E9E",
        font=("NTR", 24 * -1),
    )

    canvas.create_text(
        336.0,
        428.0,
        anchor="nw",
        text="Enter PORT:",
        fill="#9E9E9E",
        font=("NTR", 24 * -1),
    )

    canvas.create_text(
        250.0, 14.0, anchor="nw", text="C-Chat", fill="#BDBDBD", font=("NTR", 96 * -1)
    )

    canvas.create_text(
        308.0,
        524.0,
        anchor="nw",
        text="Press Enter",
        fill="#BDBDBD",
        font=("NTR", 36 * -1),
    )
    sub_win_host_port.resizable(False, False)
    dark_title_bar(sub_win_host_port)
    entry_1.insert(0, "127.0.0.1")
    entry_2.insert(0, "5002")

    def host_port(event):
        try:
            HOST = str(entry_1.get())
            PORT = int(entry_2.get())

            data = {"SERVER_HOST": HOST, "SERVER_PORT": PORT}
            with open("config.json", "w") as outfile:
                json.dump(data, outfile)

            sub_win_host_port.destroy()

        except Exception as k:
            entry_1.delete(0, END)
            entry_2.delete(0, END)

    def if_no_host_port():
        sys.exit()

    sub_win_host_port.bind("<Return>", host_port)
    sub_win_host_port.protocol("WM_DELETE_WINDOW", if_no_host_port)
    sub_win_host_port.mainloop()


def init_socket():
    global SERVER_HOST
    global SERVER_PORT
    global work_socket

    with open("config.json") as f:
        templates = json.load(f)

    SERVER_HOST = templates["SERVER_HOST"]
    SERVER_PORT = templates["SERVER_PORT"]

    work_socket = socket.socket()

    try:
        work_socket.connect((SERVER_HOST, SERVER_PORT))
    except Exception as e:
        print(e)
        sys.exit()


def incoming_calls():
    global agree_for_start_call
    global check_call_for_you
    global call_for_you
    global receiver
    global sender
    global name_of_call
    global window_of_call_aud

    if check_call_for_you is True:
        check_call_for_you = False
        name_of_call = msg["from"]
        YOUR_WORK_HOST = msg["text"]
        call_for_you = Toplevel()
        call_for_you.geometry("600x700")
        call_for_you.resizable(False, False)
        call_for_you.title("Audio call")
        call_for_you.configure(bg="#212121")
        dark_title_bar(call_for_you)

        image_yes_call = img_tk.PhotoImage(file="work_files/yes_call.png")
        image_no_call = img_tk.PhotoImage(file="work_files/no_call.png")
        photo_user_call = img_tk.PhotoImage(file="work_files/def_user.png")

        def enter_the_call():
            global sender
            global receiver
            global window_of_call_aud

            MY_WORK_HOST = socket.gethostbyname(socket.gethostname())

            work_socket.send(
                (
                    json.dumps(
                        {
                            "type": "connect_to_aud_call",
                            "text": MY_WORK_HOST,
                            "from": name,
                            "to": [name_of_call],
                            "group": None,
                            "file_size": None,
                        }
                    )
                ).encode("utf8")
            )

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

            who_talk_img = Label(
                window_of_call_aud,
                image=photo_user_call,
                bg="#212121",
                activebackground="#212121",
            )
            who_talk_img.image = photo_user_call
            who_talk_img.place(x=250, y=100)

            person_call = Canvas(
                window_of_call_aud,
                bg="#2F2F38",
                width=596,
                height=40,
                borderwidth=0,
                bd=0,
                highlightbackground="#3A3A3A",
            )
            person_call.place(x=0, y=200)
            person_call.create_text(
                298, 20, text=name_of_call, fill="#9E9E9E", font=("NTR", 24 * -1)
            )

            image_off_call = img_tk.PhotoImage(file="work_files/off_audio_call.png")

            def call_stop():
                window_of_call_aud.destroy()
                sender.stop_stream()
                work_socket.send(
                    (
                        json.dumps(
                            {
                                "type": "stop_aud_sender",
                                "text": None,
                                "from": name,
                                "to": [name_of_call],
                                "group": None,
                                "file_size": None,
                            }
                        )
                    ).encode("utf8")
                )

            Button(
                window_of_call_aud,
                image=image_off_call,
                command=call_stop,
                relief="flat",
                bg="#212121",
                activebackground="#212121",
            ).place(x=260, y=575)

            window_of_call_aud.mainloop()

        def reject_call():
            call_for_you.destroy()

            work_socket.send(
                (
                    json.dumps(
                        {
                            "type": "reject_call",
                            "text": None,
                            "from": name,
                            "to": [name_of_call],
                            "group": None,
                            "file_size": None,
                        }
                    )
                ).encode("utf8")
            )

        Button(
            call_for_you,
            image=image_yes_call,
            command=enter_the_call,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=0, y=575)
        Button(
            call_for_you,
            image=image_no_call,
            command=reject_call,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=515, y=575)

        Label(
            call_for_you,
            image=photo_user_call,
            bg="#212121",
            activebackground="#212121",
        ).place(x=250, y=100)

        who_call = Canvas(
            call_for_you,
            bg="#2F2F38",
            width=596,
            height=40,
            borderwidth=0,
            bd=0,
            highlightbackground="#3A3A3A",
        )
        who_call.place(x=0, y=200)
        who_call.create_text(
            298, 20, text=name_of_call, fill="#9E9E9E", font=("NTR", 24 * -1)
        )

        Thread(target=incoming_calls, daemon=True).start()
        call_for_you.mainloop()

    elif agree_for_start_call is True:
        agree_for_start_call = False
        YOUR_HOST = msg["text"]
        name_of_call = msg["from"]
        receiver = AudioReceiver(socket.gethostbyname(socket.gethostname()), 5555)
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

        photo_user_call = img_tk.PhotoImage(file="work_files/def_user.png")

        Label(
            window_of_call_aud,
            image=photo_user_call,
            bg="#212121",
            activebackground="#212121",
        ).place(x=250, y=100)

        who_call = Canvas(
            window_of_call_aud,
            bg="#2F2F38",
            width=596,
            height=40,
            borderwidth=0,
            bd=0,
            highlightbackground="#3A3A3A",
        )
        who_call.place(x=0, y=200)
        who_call.create_text(
            298, 20, text=name_of_call, fill="#9E9E9E", font=("NTR", 24 * -1)
        )

        image_off_call = img_tk.PhotoImage(file="work_files/off_audio_call.png")

        def stop_call_now():
            work_socket.send(
                (
                    json.dumps(
                        {
                            "type": "stop_aud_call_from_receiver",
                            "text": None,
                            "from": name,
                            "to": [call_for_person],
                            "group": None,
                            "file_size": None,
                        }
                    )
                ).encode("utf8")
            )

        Button(
            window_of_call_aud,
            image=image_off_call,
            command=stop_call_now,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=260, y=575)

        Thread(target=incoming_calls, daemon=True).start()
        window_of_call_aud.mainloop()

    main_win.after(1000, incoming_calls)


def receive():
    global msg
    global check_call_for_you
    global agree_for_start_call
    global you_start_call
    global name_of_call

    while True:
        try:
            msg = json.loads(work_socket.recv(1024).decode("utf8"))
            msg_type = msg["type"]
            print(msg)

            match msg_type:
                case "new_client_list":
                    person_list.delete(0, END)

                    if name in msg["msg"]:
                        msg["msg"].remove(str(name))

                    for i in msg["msg"]:
                        person_list.insert(0, i)

                case "create_new_group":
                    file_group = open("groups\\" + msg["group"] + ".txt", "w")
                    file_group.write(",".join(msg["to"]))
                    file_group.close()
                    groups.append(msg["group"])
                    person_list.insert(0, msg["group"])

                case "group_msg":
                    file_group = open("groups\\" + msg["group"] + ".txt", "a")
                    file_group.write("\n" + msg["from"] + ": " + msg["text"])
                    file_group.close()
                    if msg["group"] == person:
                        dialog_window.insert(END, msg["from"] + ": " + msg["text"])
                        dialog_window.yview_moveto(1)

                case "personal_msg":
                    if msg["from"] == person:
                        dialog_window.insert(END, msg["from"] + ": " + msg["text"])
                        dialog_window.yview_moveto(1)

                    if (
                        os.path.exists(
                            "story\\" + str(name) + " " + msg["from"] + ".txt"
                        )
                        is False
                    ):
                        file = open(
                            "story\\" + str(name) + " " + msg["from"] + ".txt", "w"
                        )
                        file.write(msg["from"] + ": " + msg["text"])
                        file.close()

                    else:
                        file = open(
                            "story\\" + str(name) + " " + msg["from"] + ".txt", "a"
                        )
                        file.write("\n" + msg["from"] + ": " + msg["text"])
                        file.close()

                case "person_get_file":
                    if msg["from"] == person:
                        dialog_window.insert(END, msg["from"] + ": " + msg["text"])
                        dialog_window.yview_moveto(1)

                    if (
                        os.path.exists(
                            "story\\" + str(name) + " " + msg["from"] + ".txt"
                        )
                        is False
                    ):
                        file = open(
                            "story\\" + str(name) + " " + msg["from"] + ".txt", "w"
                        )
                        file.write(msg["from"] + ": " + msg["text"])
                        file.close()

                    else:
                        file = open(
                            "story\\" + str(name) + " " + msg["from"] + ".txt", "a"
                        )
                        file.write("\n" + msg["from"] + ": " + msg["text"])
                        file.close()
                    if os.path.exists("sent/" + msg["text"]):
                        os.remove("sent/" + msg["text"])
                    send_file = open("sent/" + msg["text"], "wb")
                    file_size = int(msg["file_size"])

                    while file_size > 1024:
                        msg = work_socket.recv(1024)
                        send_file.write(msg)
                        file_size -= 1024
                    msg = work_socket.recv(file_size)
                    send_file.write(msg)

                    send_file.close()

                case "group_get_file":
                    if msg["from"] == person:
                        dialog_window.insert(END, msg["from"] + ": " + msg["text"])
                        dialog_window.yview_moveto(1)

                    file = open("groups\\" + msg["group"] + ".txt", "a")
                    file.write("\n" + msg["from"] + ": " + msg["text"])
                    file.close()
                    if os.path.exists("sent/" + msg["text"]):
                        os.remove("sent/" + msg["text"])
                    send_file = open("sent/" + msg["text"], "wb")
                    file_size = int(msg["file_size"])

                    while file_size > 1024:
                        msg = work_socket.recv(1024)
                        send_file.write(msg)
                        file_size -= 1024
                    msg = work_socket.recv(file_size)
                    send_file.write(msg)

                    send_file.close()

                case "start_aud_call":
                    check_call_for_you = True

                case "connect_to_aud_call":
                    if you_start_call is True:
                        you_start_call = False
                        win_wait_call.destroy()

                    agree_for_start_call = True

                case "stop_aud_calling":
                    call_for_you.destroy()

                case "stop_aud_sender":
                    sender.stop_stream()
                    work_socket.send(
                        (
                            json.dumps(
                                {
                                    "type": "stop_aud_receiver_person1",
                                    "text": None,
                                    "from": name,
                                    "to": [msg["from"]],
                                    "group": None,
                                    "file_size": None,
                                }
                            )
                        ).encode("utf8")
                    )

                case "stop_aud_receiver_person1":
                    receiver.stop_server()
                    work_socket.send(
                        (
                            json.dumps(
                                {
                                    "type": "stop_aud_receiver_person2",
                                    "text": None,
                                    "from": name,
                                    "to": [msg["from"]],
                                    "group": None,
                                    "file_size": None,
                                }
                            )
                        ).encode("utf8")
                    )

                    window_of_call_aud.destroy()

                case "stop_aud_receiver_person2":
                    window_of_call_aud.destroy()
                    receiver.stop_server()

                case "reject_call":
                    agree_for_start_call = False
                    you_start_call = False
                    win_wait_call.destroy()

                case "stop_aud_call_from_receiver":
                    window_of_call_aud.destroy()
                    sender.stop_stream()
                    work_socket.send(
                        (
                            json.dumps(
                                {
                                    "type": "stop_aud_sender",
                                    "text": None,
                                    "from": name,
                                    "to": [msg["from"]],
                                    "group": None,
                                    "file_size": None,
                                }
                            )
                        ).encode("utf8")
                    )

        except OSError:
            break


def new_dialog(event):
    global person
    global list_of_group
    global create_group_mode
    global dialog_window
    global canvas_person

    if (
        create_group_mode is False
        and person_list.get(person_list.curselection()[0]) not in groups
        and person_list.get(person_list.curselection()[0]) != person
    ):
        image_def_user = img_tk.PhotoImage(file="work_files/def_user.png")

        default_user_photo = Label(image=image_def_user, bg="#212121")
        default_user_photo.image = image_def_user
        default_user_photo.place(x=398, y=1)

        dialog_window.delete(0, END)

        person = person_list.get(person_list.curselection()[0])
        canvas_who_talk.itemconfigure(canvas_person, text=person)

        if os.path.exists("story\\" + str(name) + " " + str(person) + ".txt"):
            file = open("story\\" + str(name) + " " + str(person) + ".txt", "r")
            old_string = file.readlines()

            for i in old_string:
                dialog_window.insert(END, i)

            dialog_window.yview_moveto(1)

        def send_e(event):
            send()

        def send():
            my_msg = entry_send.get()

            if (
                my_msg is not None
                and my_msg != ""
                and person is not None
                and person != ""
            ):
                if (
                    os.path.exists("story\\" + str(name) + " " + person + ".txt")
                    is False
                ):
                    story_file = open(
                        "story\\" + str(name) + " " + person + ".txt", "w"
                    )
                    story_file.write(name + ": " + my_msg)
                    story_file.close()

                else:
                    story_file = open(
                        "story\\" + str(name) + " " + person + ".txt", "a"
                    )
                    story_file.write("\n" + name + ": " + my_msg)
                    story_file.close()

                work_socket.send(
                    (
                        json.dumps(
                            {
                                "type": "personal_msg",
                                "text": my_msg,
                                "from": name,
                                "to": [person],
                                "group": None,
                                "file_size": None,
                            }
                        )
                    ).encode("utf8")
                )
                entry_send.delete(0, END)
                dialog_window.insert(END, name + ": " + my_msg)
                dialog_window.yview_moveto(1)

        def send_file():
            file_choose_win(
                file_now,
                catalog,
                name,
                dialog_window,
                work_socket,
                person,
                groups,
                work_files,
                work_folders,
                work_dirs,
            )

        def start_audio():
            global win_wait_call
            global you_start_call
            global call_for_person
            you_start_call = True
            call_for_person = person

            work_socket.send(
                (
                    json.dumps(
                        {
                            "type": "start_aud_call",
                            "text": socket.gethostbyname(socket.gethostname()),
                            "from": name,
                            "to": [call_for_person],
                            "group": None,
                            "file_size": None,
                        }
                    )
                ).encode("utf8")
            )

            win_wait_call = Toplevel()
            win_wait_call.geometry("600x700")
            win_wait_call.resizable(False, False)
            win_wait_call.title("Wait")
            win_wait_call.configure(bg="#212121")
            dark_title_bar(win_wait_call)

            image_off_call = img_tk.PhotoImage(file="work_files/off_audio_call.png")
            image_photo_call = img_tk.PhotoImage(file="work_files/def_user.png")

            Label(
                win_wait_call,
                image=image_photo_call,
                bg="#212121",
                activebackground="#212121",
            ).place(x=250, y=100)

            who_call = Canvas(
                win_wait_call,
                bg="#2F2F38",
                width=596,
                height=40,
                borderwidth=0,
                bd=0,
                highlightbackground="#3A3A3A",
            )
            who_call.place(x=0, y=200)
            who_call.create_text(
                298, 20, text=person, fill="#9E9E9E", font=("NTR", 24 * -1)
            )

            def stop_calling():
                win_wait_call.destroy()
                work_socket.send(
                    (
                        json.dumps(
                            {
                                "type": "stop_aud_calling",
                                "text": None,
                                "from": name,
                                "to": [call_for_person],
                                "group": None,
                                "file_size": None,
                            }
                        )
                    ).encode("utf8")
                )

            Button(
                win_wait_call,
                image=image_off_call,
                command=stop_calling,
                relief="flat",
                bg="#212121",
                activebackground="#212121",
            ).place(x=260, y=575)

            Label(
                win_wait_call,
                text="Wait...",
                bg="#212121",
                activebackground="#212121",
                fg="#9E9E9E",
                font=("NTR", 40 * -1),
            ).place(x=250, y=500)

            win_wait_call.mainloop()

        main_win.bind("<Return>", send_e)

        tk.Button(
            main_win,
            image=image_send_msg,
            command=send,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=910, y=680)

        tk.Button(
            main_win,
            image=image_send_file,
            command=send_file,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=965, y=680)

        Button(
            main_win,
            image=image_audio_call,
            command=start_audio,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=904, y=0)

        Button(
            main_win,
            image=image_video_call,
            command=lambda: print(),
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=1090, y=0)

        entry_send = Entry(
            bd=0,
            bg="#393944",
            fg="#C1C1C1",
            font=("Rajdhani Regular", 24 * -1),
            highlightthickness=0,
        )
        entry_send.place(x=400.0, y=685.0, width=505.0, height=35.0)

    elif (
        person_list.get(person_list.curselection()[0]) in groups
        and create_group_mode is False
        and person_list.get(person_list.curselection()[0]) != person
    ):
        image_def_user = img_tk.PhotoImage(file="work_files/def_group.png")
        default_user_photo = Label(image=image_def_user, bg="#212121")
        default_user_photo.place(x=398, y=1)
        dialog_window.delete(0, END)

        person = person_list.get(person_list.curselection()[0])
        canvas_who_talk.itemconfigure(canvas_person, text=person)

        file = open("groups\\" + person + ".txt", "r")
        old_string = file.readlines()
        old_string.pop(0)

        for i in old_string:
            dialog_window.insert(END, i)

        def send_e_g(event):
            send_g()

        def send_g():
            my_msg = entry_send.get()

            if (
                my_msg is not None
                and my_msg != ""
                and person is not None
                and person != ""
            ):
                with open("groups\\" + person + ".txt", "r") as f:
                    lines = f.readlines()
                    persons = lines[0]
                    if "\n" in persons:
                        persons = persons.split("\n")[0]
                    persons = persons.split(",")
                    work_socket.send(
                        (
                            json.dumps(
                                {
                                    "type": "group_msg",
                                    "text": my_msg,
                                    "from": name,
                                    "to": persons,
                                    "group": person,
                                    "file_size": None,
                                }
                            )
                        ).encode("utf8")
                    )
            entry_send.delete(0, END)
            dialog_window.yview_moveto(1)

        def send_file_group():
            file_choose_win(
                file_now,
                catalog,
                name,
                dialog_window,
                work_socket,
                person,
                groups,
                work_files,
                work_folders,
                work_dirs,
            )

        main_win.bind("<Return>", send_e_g)

        tk.Button(
            main_win,
            image=image_send_msg,
            command=send_g,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=910, y=680)

        tk.Button(
            main_win,
            image=image_send_file,
            command=send_file_group,
            relief="flat",
            bg="#212121",
            activebackground="#212121",
        ).place(x=965, y=680)

        entry_send = Entry(
            bd=0,
            bg="#393944",
            fg="#C1C1C1",
            font=("Rajdhani Regular", 24 * -1),
            highlightthickness=0,
        )
        entry_send.place(x=400.0, y=685.0, width=505.0, height=35.0)

    else:
        if create_group_mode is True:
            if dialog_window.get(0) != "Your group: ":
                dialog_window.delete(0, END)
                dialog_window.insert(0, "Your group: ")
            group_person = person_list.get(person_list.curselection()[0])

            if group_person not in list_of_group and group_person not in groups:
                list_of_group.append(group_person)
                dialog_window.insert(END, group_person)

            def create_group():
                win_name_group = Toplevel()
                win_name_group.geometry("200x150")
                win_name_group.configure(bg="#212121")
                Label(
                    win_name_group,
                    bg="#212121",
                    text="Enter name of your group: ",
                    fg="#77B5FE",
                ).pack()
                group_name = Entry(win_name_group, bg="#616161")
                group_name.pack()

                def create_new_group():
                    global create_group_mode
                    global list_of_group

                    if group_name.get() not in groups:
                        group_name_var = group_name.get()
                        groups.append(group_name_var)
                        g_file = open("groups\\" + group_name_var + ".txt", "w")
                        g_file.write(name + "," + ",".join(list_of_group))
                        g_file.close()
                        person_list.insert(0, group_name_var)
                        dialog_window.delete(0, END)
                        create_group_mode = False
                        work_socket.send(
                            (
                                json.dumps(
                                    {
                                        "type": "create_new_group",
                                        "text": None,
                                        "from": name,
                                        "to": list_of_group,
                                        "group": group_name_var,
                                        "file_size": None,
                                    }
                                )
                            ).encode("utf8")
                        )
                        list_of_group = []
                        btn_send.destroy()
                        win_name_group.destroy()

                tk.Button(
                    win_name_group,
                    text="OK",
                    command=create_new_group,
                    bg="#212121",
                    fg="#77B5FE",
                ).pack()
                dark_title_bar(win_name_group)

            if len(list_of_group) >= 2:
                image_create = img_tk.PhotoImage(file="work_files/create_button.png")
                btn_send = tk.Button(
                    main_win,
                    image=image_create,
                    command=create_group,
                    relief="flat",
                    bg="#3A3A3A",
                    activebackground="#212121",
                )
                btn_send.image = image_create
                btn_send.place(x=1062, y=668)


def new_group():
    global create_group_mode
    create_group_mode = True


def init_login():
    def sub_close(event):
        global name
        name = entry.get()

        if name != "" and name not in registration_client_list and " " not in name:
            work_socket.send(name.encode("utf8"))
            sub_win.destroy()

        elif name in registration_client_list:
            xys = tk.Label(
                sub_win, text="login already exists", bg="#212121", foreground="red"
            )
            xys.place(x=360, y=360)
            xys.destroy()

        elif " " in name or "," in name:
            xyz = tk.Label(
                sub_win, text="wrong character", bg="#212121", foreground="red"
            )
            xyz.place(x=360, y=380)
            xyz.destroy()

    registration_client_list = work_socket.recv(1024).decode("utf8")

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
        relief="ridge",
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        285.0, 10.0, anchor="nw", text="C-Chat", fill="#BDBDBD", font=("NTR", 64 * -1)
    )

    canvas.create_text(
        300.0,
        235.0,
        anchor="nw",
        text="Enter your login:",
        fill="#9E9E9E",
        font=("NTR", 32 * -1),
    )

    entry_image_1 = PhotoImage(file="work_files/entry_login.png")
    canvas.create_image(413.5, 316.5, image=entry_image_1)
    entry = Entry(bd=0, bg="#616161", fg="#000716", highlightthickness=0)
    entry.place(x=329.0, y=300.0, width=169.0, height=31.0)

    canvas.create_text(
        340.0,
        428.0,
        anchor="nw",
        text="Press Enter",
        fill="#BDBDBD",
        font=("NTR", 28 * -1),
    )

    image_image_1 = PhotoImage(file="work_files/small_logo.png")
    canvas.create_image(523.0, 39.0, image=image_image_1)

    sub_win.resizable(False, False)
    dark_title_bar(sub_win)
    sub_win.bind("<Return>", sub_close)
    sub_win.mainloop()


def chat_window():
    global image_send_msg
    global image_send_file
    global image_audio_call
    global image_default_user
    global image_audio_call
    global image_video_call
    global main_win
    global person_list
    global canvas_who_talk
    global image_create_group
    global dialog_window
    global canvas_person

    main_win = Tk()
    main_win.geometry("1200x1200")
    main_win.title("Chats")

    sb_persons = ttk.Scrollbar(main_win, orient="vertical")

    style = ttk.Style()
    style.theme_use("classic")
    style.configure(
        "Vertical.TScrollbar",
        background="#3A3A3A",
        troughcolor="#2F2F38",
        activebackground="red",
    )

    image_create_group = img_tk.PhotoImage(file="work_files/new.png")
    image_send_msg = img_tk.PhotoImage(file="work_files/plane.png")
    image_send_file = img_tk.PhotoImage(file="work_files/x_file.png")
    image_default_user = img_tk.PhotoImage(file="work_files/def_user.png")
    image_audio_call = img_tk.PhotoImage(file="work_files/audio.png")
    image_video_call = img_tk.PhotoImage(file="work_files/video.png")

    person_list = tk.Listbox(
        main_win,
        bg="#2F2F38",
        fg="#C1C1C1",
        font=("Rajdhani Regular", 20 * -1),
        selectbackground="#77B5FE",
        selectmode=SINGLE,
        borderwidth=5,
        highlightthickness=5,
        height=20,
        width=15,
        relief=GROOVE,
        bd=0,
        highlightbackground="#3A3A3A",
        highlightcolor="#3A3A3A",
        yscrollcommand=sb_persons.set,
    )

    person_list.bind("<Double-Button-1>", new_dialog)

    sb_persons.config(command=person_list.yview)
    sb_persons.place(x=175, y=173, height=490)

    person_list.place(x=0, y=173)
    dark_title_bar(main_win)
    main_win["bg"] = "#212121"

    create_group_image = Button(
        main_win,
        image=image_create_group,
        command=new_group,
        relief="flat",
        bg="#3A3A3A",
        activebackground="#212121",
    )
    create_group_image.image = image_create_group
    create_group_image.place(x=0, y=663)

    image_of_user = Label(image=image_default_user, bg="#212121")
    image_of_user.place(x=398, y=1)

    canvas_who_talk = Canvas(width=401, height=91, bg="#2F2F38", bd=0, relief="ridge")
    canvas_who_talk.config(highlightbackground="#3A3A3A", highlightthickness=3)
    canvas_who_talk.place(x=498, y=3)
    canvas_person = canvas_who_talk.create_text(
        200, 50, text="", fill="#C8C8C9", font=("NTR 24")
    )

    sb_dialog = ttk.Scrollbar(main_win, orient="vertical")

    dialog_window = tk.Listbox(
        main_win,
        bg="#2F2F38",
        fg="#C1C1C1",
        font=("Rajdhani Regular", 20 * -1),
        selectbackground="#77B5FE",
        selectmode=SINGLE,
        borderwidth=5,
        highlightthickness=5,
        height=23,
        width=43,
        relief=GROOVE,
        bd=0,
        highlightbackground="#3A3A3A",
        highlightcolor="#3A3A3A",
        yscrollcommand=sb_dialog.set,
    )

    sb_dialog.config(command=dialog_window.yview)
    sb_dialog.place(x=885, y=102, height=558)

    dialog_window.place(x=400, y=98)

    receive_thread = Thread(target=receive, daemon=True)
    receive_thread.start()

    def user_exit():
        work_socket.close()
        sys.exit()

    main_win.protocol("WM_EXIT", user_exit)
    incoming_calls()
    main_win.mainloop()


if __name__ == "__main__":
    main()
