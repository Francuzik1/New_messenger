from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path
import re
import json


name_to_clientList = {}
talk_with_list = {}
if os.path.exists("sent") is False:
    os.mkdir("sent")


def main():
    enter_host_port()
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=init_server, daemon=True)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()


def init_server():

    while True:

        client, client_address = SERVER.accept()
        addresses[client] = client_address
        msg = "/new_client_list " + ",".join(client_list)
        client.send(bytes(json.dumps({"type": "new_client_list", "msg": msg}), "utf8"))
        Thread(target=handle_client, args=(client,), daemon=True).start()


def handle_client(client):  # Takes client socket as argument.

    global client_list

    name = client.recv(BUF_SIZE).decode("utf8")
    client_list.append(name)
    msg = "/new_client_list " + ",".join(client_list)
    clients[client] = name
    name_to_clientList[name] = client
    broadcast(bytes(json.dumps({"type": "new_client_list", "msg": msg}), "utf8"))

    is_text_msg = True
    # file_size // 1024
    file_size = None
    # file - file_size * 1024
    file_remainder = None

    while True:
        try:
            if is_text_msg is True:

                msg = client.recv(BUF_SIZE).decode("utf8")
                msg = eval(msg)
                msg_type = msg["type"]
                msg = msg["msg"]
                print(msg)

                match msg_type:

                    case "personal_msg":

                        msg = msg.split("abpers")
                        from_person = msg[0]
                        to_person = msg[2]
                        personal_msg = "/abpers" + from_person + ": " + msg[1]
                        name_to_clientList[from_person].send(bytes(json.dumps({"type": "personal_msg",
                                                                               "msg": personal_msg}), "utf8"))
                        name_to_clientList[to_person].send(bytes(json.dumps({"type": "personal_msg",
                                                                             "msg": personal_msg}), "utf8"))

                    case "create_new_group":

                        msg = msg.split(" ")[1]
                        msg = msg.split(",")
                        group_name = msg.pop(0)
                        creator = msg.pop(0)
                        create_new_group = "/create_new_group " + group_name + "," + creator + "," + ",".join(msg)

                        for i in msg:
                            name_to_clientList[i].send(
                                bytes(json.dumps({"type": "create_new_group", "msg": create_new_group}), "utf8"))

                    case "group_msg":

                        msg = msg.split("mes_group")
                        list_to_send = msg[1]
                        group = msg[0]
                        msg = msg[2]
                        if "\n" in list_to_send:
                            list_to_send = list_to_send.split("\n")[0]
                        list_to_send = list_to_send.split(",")
                        group_msg = group + "mes_group" + msg
                        for e in list_to_send:
                            name_to_clientList[e].send(bytes(json.dumps({"type": "group_msg", "msg": group_msg}), "utf8"))

                    case "person_get_file":

                        msg = msg.split("/talk_person")
                        person_1 = msg[0]
                        person_2 = msg[1]
                        talk_with_list[person_1] = person_2

                    case "group_get_file":

                        msg = msg.split("/talk_group")
                        group = msg[1]
                        persons = msg[2]
                        name_file_creator = msg[0]
                        if "\n" in persons:
                            persons = persons.split("\n")[0]
                        talk_with_list[name_file_creator] = name_file_creator + "/talk_group" + group + \
                                                            "/talk_group" + persons

                    case "personal_file_configuration":

                        name_to_clientList[talk_with_list[name]].send(bytes(json.dumps(
                            {"type": "personal_file_configuration", "msg": msg}), "utf8"))

                        msg = msg.split("/file_name")
                        file_size = int(msg[0])
                        file_remainder = int(msg[1])

                        is_text_msg = False

                    case "group_file_configuration":

                        persons_for_send = ((talk_with_list[name].split("/talk_group"))[2]).split(",")

                        if name in persons_for_send:
                            persons_for_send.remove(name)

                        for i in persons_for_send:
                            name_to_clientList[i].send(bytes(json.dumps(
                                {"type": "group_file_configuration", "msg": msg}), "utf8"))

                        msg = msg.split("/file_group")
                        file_size = int(msg[0])
                        file_remainder = int(msg[1])

                        is_text_msg = False

                    case "start_aud_call":

                        person_start_aud = msg.split("/start_audio/")
                        name_to_clientList[person_start_aud[0]].send(bytes(json.dumps(
                            {"type": "start_aud_call", "msg": msg}), "utf8"))

                    case "connect_to_aud_call":

                        call_to = (msg.split("/yes_call/"))[0]
                        name_to_clientList[call_to].send(bytes(json.dumps(
                            {"type": "connect_to_aud_call", "msg": msg}), "utf8"))

                    case "stop_aud_calling":

                        person_for_stop = msg.split("/stop_calling/")[0]
                        name_to_clientList[person_for_stop].send(bytes(json.dumps(
                            {"type": "stop_aud_calling", "msg": msg}), "utf8"))

                    case "stop_aud_sender":

                        person_for_stop = msg.split("/stop_sender/")[0]
                        name_to_clientList[person_for_stop].send(bytes(json.dumps(
                            {"type": "stop_aud_sender", "msg": msg}), "utf8"))

                    case "stop_aud_receiver_person1":
                        person_for_stop = msg.split("/stop_reciver/")[0]
                        name_to_clientList[person_for_stop].send(bytes(json.dumps(
                            {"type": "stop_aud_receiver_person1", "msg": msg}), "utf8"))

                    case "stop_aud_receiver_person2":

                        person_for_stop = msg.split("/stop_last_recive/")[0]
                        name_to_clientList[person_for_stop].send(bytes(json.dumps(
                            {"type": "stop_aud_receiver_person2", "msg": msg}), "utf8"))

                    case "reject_call":

                        person_for_stop_call = msg.split("/stop_call_me/")[0]
                        name_to_clientList[person_for_stop_call].send(bytes(json.dumps(
                            {"type": "reject_call", "msg": msg}), "utf8"))

                    case "stop_aud_call_from_receiver":

                        person_for_stop_call = msg.split("/stop_call_other/")[0]
                        name_to_clientList[person_for_stop_call].send(bytes(json.dumps(
                            {"type": "stop_aud_call_from_receiver", "msg": msg}), "utf8"))

            # only for bytes of files
            else:

                if "/talk_group" not in talk_with_list[name]:

                    while file_size != 0:

                        msg = client.recv(BUF_SIZE)

                        name_to_clientList[talk_with_list[name]].send(msg)
                        file_size -= 1

                    if file_remainder != 0:

                        msg = client.recv(int(file_remainder))
                        name_to_clientList[talk_with_list[name]].send(msg)

                    is_text_msg = True

                else:

                    persons_for_send = ((talk_with_list[name].split("/talk_group"))[2]).split(",")

                    if name in persons_for_send:
                        persons_for_send.remove(name)

                    while file_size != 0:
                        msg = client.recv(BUF_SIZE)
                        for i in persons_for_send:
                            name_to_clientList[i].send(msg)
                        file_size -= 1

                    if file_remainder != 0:
                        msg = client.recv(int(file_remainder))
                        for i in persons_for_send:
                            name_to_clientList[i].send(msg)

                    is_text_msg = True

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

BUF_SIZE = 1024

SERVER = socket(AF_INET, SOCK_STREAM)


def enter_host_port():

    def enter_host():
        host_syntax = r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"

        host = input("HOST: ")
        CheckHost = re.fullmatch(host_syntax, host)
        if CheckHost is None:
            print("Host - a sequence of 4 numbers (from 0 to 255) separated by dots.")
            print("Enter a host such as: 0.0.0.0 - 255.255.255.255")
            enter_host()

        return host

    def enter_port():

        port = input("PORT: ")
        if port.isnumeric() is False or int(port) > 65535:
            print("Port is a number from 1 to 65535")
            enter_port()
        port = int(port)

        return port

    try:
        # return host port
        SERVER.bind((enter_host(), enter_port()))

    except Exception as y:
        enter_host_port()


# def server_bind():

if __name__ == "__main__":
    main()

SERVER.close()
