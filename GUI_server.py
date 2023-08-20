from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path
import re


nameToClientList = {}
talkWithList = {}
if os.path.exists("sent") is False:
    os.mkdir("sent")


def accept_incoming_connections():

    while True:

        client, client_address = SERVER.accept()
        addresses[client] = client_address
        msg = "/new_client_list " + ",".join(clientList)
        client.send(bytes(msg, "utf8"))
        Thread(target=handle_client, args=(client,), daemon=True).start()


def handle_client(client):  # Takes client socket as argument.

    global clientList

    name = client.recv(BUFSIZ).decode("utf8")
    clientList.append(name)
    msg = "/new_client_list " + ",".join(clientList)
    clients[client] = name
    nameToClientList[name] = client
    broadcast(bytes(msg, "utf8"))

    utfMode = True
    # file_size // 1024
    fullNumber1024 = None
    # file - file_size * 1024
    fileRemainder = None

    while True:
        try:
            if utfMode is True:

                msg = client.recv(BUFSIZ).decode("utf8")
                print(msg)

                # from person to person msg, find a client address to receive msg
                if "abpers" in msg:

                    msg = msg.split("abpers")
                    from_person = msg[0]
                    to_person = msg[2]
                    nameToClientList[from_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))
                    nameToClientList[to_person].send(bytes("/abpers" + from_person + ": " + msg[1], "utf8"))
                # receive invite group persons
                elif "/create_new_group " in msg:

                    msg = msg.split(" ")[1]
                    msg = msg.split(",")
                    group_name = msg.pop(0)
                    creator = msg.pop(0)

                    for i in msg:

                        nameToClientList[i].send(bytes("/create_new_group " + group_name + "," + creator + "," + ",".join(msg), "utf8"))
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
                        nameToClientList[e].send(bytes(group + "mes_group" + msg, "utf8"))

                # inf about who receive bytes of file
                elif "/talk_person" in msg:
                    msg = msg.split("/talk_person")
                    person_1 = msg[0]
                    person_2 = msg[1]
                    talkWithList[person_1] = person_2

                # inf about who receive bytes of file (all in groups)
                elif "/talk_group" in msg:

                    msg = msg.split("/talk_group")
                    group = msg[1]
                    persons = msg[2]
                    name_file_creator = msg[0]
                    if "\n" in persons:
                        persons = persons.split("\n")[0]
                    talkWithList[name_file_creator] = name_file_creator + "/talk_group" + group + "/talk_group" + persons

                # start receive bytes of file. Unit with talkwith ?
                elif "/file_name" in msg:

                    nameToClientList[talkWithList[name]].send(bytes(msg, "utf8"))
                    msg = msg.split("/file_name")
                    fullNumber1024 = int(msg[0])
                    fileRemainder = int(msg[1])

                    utfMode = False

                # start receive bytes of file (in group). Unit with talkwith ?
                elif "/file_group" in msg:

                    persons_for_send = ((talkWithList[name].split("/talk_group"))[2]).split(",")

                    if name in persons_for_send:

                        persons_for_send.remove(name)

                    for i in persons_for_send:

                        nameToClientList[i].send(bytes(msg, "utf8"))

                    msg = msg.split("/file_group")
                    fullNumber1024 = int(msg[0])
                    fileRemainder = int(msg[1])

                    utfMode = False

                # delete!
                elif "/start_audio/" in msg:

                    person_start_aud = msg.split("/start_audio/")
                    nameToClientList[person_start_aud[0]].send(bytes(msg, "utf8"))

                # delete!
                elif "/yes_call/" in msg:

                    call_to = (msg.split("/yes_call/"))[0]
                    nameToClientList[call_to].send(bytes(msg, "utf8"))

                elif "/stop_calling/" in msg:

                    person_for_stop = msg.split("/stop_calling/")[0]
                    nameToClientList[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_sender/" in msg:

                    person_for_stop = msg.split("/stop_sender/")[0]
                    nameToClientList[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_reciver/" in msg:

                    person_for_stop = msg.split("/stop_reciver/")[0]
                    nameToClientList[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_last_recive/" in msg:

                    person_for_stop = msg.split("/stop_last_recive/")[0]
                    nameToClientList[person_for_stop].send(bytes(msg, "utf8"))

                elif "/stop_call_me/" in msg:

                    person_for_stop_call = msg.split("/stop_call_me/")[0]
                    nameToClientList[person_for_stop_call].send(bytes(msg, "utf8"))

                elif "/ok_stop_call/" in msg:

                    person_for_stop_call = msg.split("/ok_stop_call/")[0]
                    nameToClientList[person_for_stop_call].send(bytes(msg, "utf8"))

                elif "/stop_call_other/" in msg:

                    person_for_stop_call = msg.split("/stop_call_other/")[0]
                    nameToClientList[person_for_stop_call].send(bytes(msg, "utf8"))

            # only for bytes of files
            else:

                if "/talk_group" not in talkWithList[name]:

                    while fullNumber1024 != 0:

                        msg = client.recv(BUFSIZ)

                        nameToClientList[talkWithList[name]].send(msg)
                        fullNumber1024 -= 1

                    if fileRemainder != 0:

                        msg = client.recv(int(fileRemainder))
                        nameToClientList[talkWithList[name]].send(msg)

                    utfMode = True

                else:

                    persons_for_send = ((talkWithList[name].split("/talk_group"))[2]).split(",")

                    if name in persons_for_send:
                        persons_for_send.remove(name)

                    while fullNumber1024 != 0:
                        msg = client.recv(BUFSIZ)
                        for i in persons_for_send:
                            nameToClientList[i].send(msg)
                        fullNumber1024 -= 1

                    if fileRemainder != 0:
                        msg = client.recv(int(fileRemainder))
                        for i in persons_for_send:
                            nameToClientList[i].send(msg)

                    utfMode = True

        except Exception as e:

            print(f"[!] Error: {e}")
            clientList.remove(name)
            del clients[client]
            to_send = "/new_client_list " + ",".join(clientList)
            broadcast(bytes(to_send, "utf8"))
            client.close()
            break


def broadcast(msg_q):  # prefix is for name identification.

    for sock in clients:

        sock.send(msg_q)


clients = {}
addresses = {}
clientList = []

HOST = None
PORT = None

BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)


def enter_host_port():

    global HOST
    global PORT
    global ADDR
    host_syntax = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"

    def enter_host():

        global HOST

        HOST = input("HOST: ")
        CheckHost = re.fullmatch(host_syntax, HOST)
        if CheckHost is None:
            print("Host - a sequence of 4 numbers (from 0 to 255) separated by dots.")
            print("Enter a host such as: 0.0.0.0 - 255.255.255.255")
            enter_host()

    def enter_port():

        global PORT

        PORT = input("PORT: ")
        if PORT.isnumeric() is False or int(PORT) > 65535:
            print("Port is a number from 1 to 65535")
            enter_port()
        PORT = int(PORT)

    enter_host()
    enter_port()
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