#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path
list_name_to_client = {}
exit_persons = []
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
    f = None
    name = client.recv(BUFSIZ).decode("utf8")
    client_list.append(name)
    msg = "/new_client_list " + ",".join(client_list)
    clients[client] = name
    list_name_to_client[name] = client
    broadcast(bytes(msg, "utf8"))
    Ben = True
    full_number = None
    other_number = None
    while True:
        try:
            if Ben is True:

                msg = client.recv(BUFSIZ).decode("utf8")
                print(msg)

                if "abpers" in msg:

                    msg = msg.split("abpers")
                    from_person = msg[0]
                    to_person = msg[2]
                    list_name_to_client[from_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))
                    list_name_to_client[to_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))

                elif "/create_new_group " in msg:

                    msg = msg.split(" ")[1]
                    msg = msg.split(",")
                    group_name = msg.pop(0)
                    creator = msg.pop(0)

                    for i in msg:

                        list_name_to_client[i].send(bytes("/create_new_group " + group_name + "," + creator + "," + ",".join(msg), "utf8"))

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

                elif "/talk_person" in msg:
                    msg = msg.split("/talk_person")
                    person_1 = msg[0]
                    person_2 = msg[1]
                    talk_with[person_1] = person_2

                elif "/talk_group" in msg:

                    msg = msg.split("/talk_group")
                    group = msg[1]
                    persons = msg[2]
                    name_file_creator = msg[0]
                    if "\n" in persons:
                        persons = persons.split("\n")[0]
                    talk_with[name_file_creator] = name_file_creator + "/talk_group" + group + "/talk_group" + persons

                elif "/file_name" in msg:

                    full_number = None
                    other_number = None
                    list_name_to_client[talk_with[name]].send(bytes(msg, "utf8"))
                    msg = msg.split("/file_name")
                    full_number = int(msg[0])
                    other_number = int(msg[1])
                    Ben = False

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

                    Ben = False

                elif "/start_audio/" in msg:

                    person_start_aud = msg.split("/start_audio/")
                    list_name_to_client[person_start_aud[0]].send(bytes(msg, "utf8"))

                elif "/yes_call/" in msg:

                    call_to = (msg.split("/yes_call/"))[0]
                    list_name_to_client[call_to].send(bytes(msg, "utf8"))

            else:

                if "/talk_group" not in talk_with[name]:

                    while full_number != 0:

                        msg = client.recv(BUFSIZ)

                        list_name_to_client[talk_with[name]].send(msg)
                        full_number -= 1

                    if other_number != 0:

                        msg = client.recv(int(other_number))
                        list_name_to_client[talk_with[name]].send(msg)

                    Ben = True

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

                    Ben = True

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
