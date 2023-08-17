#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path
list_name_to_client = {}
talk_with = {}
if os.path.exists("sent") is False:
    os.mkdir("sent")


def accept_incoming_connections():

    while True:

        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        msg = "/new_client_list " + ",".join(client_list)
        print(msg)
        client.send(bytes(msg, "utf8"))
        Thread(target=handle_client, args=(client,), daemon=True).start()


def handle_client(client):  # Takes client socket as argument.

    global client_list

    name = client.recv(BUFSIZ).decode("utf8")
    client_list.append(name)
    msg = "/new_client_list " + ",".join(client_list)
    clients[client] = name
    list_name_to_client[name] = client
    broadcast(bytes(msg, "utf8"))

    utf_msg = True
    # file_size // 1024
    full_number = None
    # file % 1024
    other_number = None

    while True:
        try:
            if utf_msg is True:

                msg = client.recv(BUFSIZ).decode("utf8")
                print(msg)

                # from person to person msg, find a client address to receive msg
                if "abpers" in msg:

                    msg = msg.split("abpers")
                    from_person = msg[0]
                    to_person = msg[2]
                    list_name_to_client[from_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))
                    list_name_to_client[to_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))
                # receive invite group persons
                elif "/create_new_group " in msg:

                    msg = msg.split(" ")[1]
                    msg = msg.split(",")
                    group_name = msg.pop(0)
                    creator = msg.pop(0)

                    for i in msg:

                        list_name_to_client[i].send(bytes("/create_new_group " + group_name + "," + creator + "," + ",".join(msg), "utf8"))
                # to find all client address to receive msg
                elif "mes_group" in msg:

                    msg = msg.split("mes_group")
                    list_to_send = msg[1]
                    group = msg[0]
                    msg = msg[2]
                    if "\n" in list_to_send:
                        list_to_send = list_to_send.split("\n")[0]
                    list_to_send = list_to_send.split(",")
                    for e in list_to_send:
                        list_name_to_client[e].send(bytes(group + "mes_group" + msg, "utf8"))

                # inf about who receive bytes of file
                elif "/talk_person" in msg:
                    msg = msg.split("/talk_person")
                    person_1 = msg[0]
                    person_2 = msg[1]
                    talk_with[person_1] = person_2

                # inf about who receive bytes of file (all in groups)
                elif "/talk_group" in msg:

                    msg = msg.split("/talk_group")
                    group = msg[1]
                    persons = msg[2]
                    name_file_creator = msg[0]
                    if "\n" in persons:
                        persons = persons.split("\n")[0]
                    talk_with[name_file_creator] = name_file_creator + "/talk_group" + group + "/talk_group" + persons

                # start receive bytes of file. Unit with talkwith ?
                elif "/file_name" in msg:

                    full_number = None
                    other_number = None
                    list_name_to_client[talk_with[name]].send(bytes(msg, "utf8"))
                    msg = msg.split("/file_name")
                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    utf_msg = False

                # start receive bytes of file (in group). Unit with talkwith ?
                elif "/file_group" in msg:

                    full_number = None
                    other_number = None
                    persons_for_send = ((talk_with[name].split("/talk_group"))[2]).split(",")

                    if name in persons_for_send:

                        persons_for_send.remove(name)

                    for i in persons_for_send:

                        list_name_to_client[i].send(bytes(msg, "utf8"))

                    msg = msg.split("/file_group")
                    full_number = int(msg[0])
                    other_number = int(msg[1])

                    utf_msg = False

                # delete!
                elif "/start_audio/" in msg:

                    person_start_aud = msg.split("/start_audio/")
                    list_name_to_client[person_start_aud[0]].send(bytes(msg, "utf8"))

                # delete!
                elif "/yes_call/" in msg:

                    call_to = (msg.split("/yes_call/"))[0]
                    list_name_to_client[call_to].send(bytes(msg, "utf8"))

                elif "/stop_calling/" in msg:

                    person_for_stop = msg.split("/stop_calling/")[0]
                    list_name_to_client[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_sender/" in msg:

                    person_for_stop = msg.split("/stop_sender/")[0]
                    list_name_to_client[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_reciver/" in msg:

                    person_for_stop = msg.split("/stop_reciver/")[0]
                    list_name_to_client[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_last_recive/" in msg:

                    person_for_stop = msg.split("/stop_last_recive/")[0]
                    list_name_to_client[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_call_me/" in msg:

                    person_for_stop_call = msg.split("/stop_call_me/")[0]
                    list_name_to_client[person_for_stop_call].send(bytes(msg, "utf8"))

                elif "/ok_stop_call/" in msg:

                    person_for_stop_call = msg.split("/ok_stop_call/")[0]
                    list_name_to_client[person_for_stop_call].send(bytes(msg, "utf8"))

                elif "/stop_call_other/" in msg:

                    person_for_stop_call = msg.split("/stop_call_other/")[0]
                    list_name_to_client[person_for_stop_call].send(bytes(msg, "utf8"))

            # only for bytes of files
            else:

                if "/talk_group" not in talk_with[name]:

                    while full_number != 0:

                        msg = client.recv(BUFSIZ)

                        list_name_to_client[talk_with[name]].send(msg)
                        full_number -= 1

                    if other_number != 0:

                        msg = client.recv(int(other_number))
                        list_name_to_client[talk_with[name]].send(msg)

                    utf_msg = True

                else:

                    persons_for_send = ((talk_with[name].split("/talk_group"))[2]).split(",")

                    if name in persons_for_send:
                        persons_for_send.remove(name)

                    while full_number != 0:
                        msg = client.recv(BUFSIZ)
                        for i in persons_for_send:
                            list_name_to_client[i].send(msg)
                        full_number -= 1

                    if other_number != 0:
                        msg = client.recv(int(other_number))
                        for i in persons_for_send:
                            list_name_to_client[i].send(msg)

                    utf_msg = True

        except Exception as e:

            print(f"[!] Error: {e}")
            client_list.remove(name)
            del clients[client]
            to_send = "/new_client_list " + ",".join(client_list)
            broadcast(bytes(to_send, "utf8"))
            client.close()
            break


def broadcast(msg_q):  # prefix is for name identification.

    for sock in clients:

        sock.send(msg_q)


clients = {}
addresses = {}
client_list = []

HOST = None
PORT = None

BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)


def enter_host_port():

    global HOST
    global PORT
    global ADDR
    HOST = str(input("\nHOST: "))

    def porter():

        global PORT

        try:
            PORT = int(input("\nPORT: "))
        except Exception as y:
            porter()

    porter()
    ADDR = (HOST, PORT)

    try:
        SERVER.bind(ADDR)
    except Exception as y:
        enter_host_port()


if __name__ == "__main__":

    enter_host_port()
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections, daemon=True)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()

SERVER.close()
