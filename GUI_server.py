from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path
import re
import json
from server_receive import handle_client

name_to_client_list = {}
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
        client, _ = SERVER.accept()
        client.send(
            (json.dumps({"type": "new_client_list", "msg": client_list})).encode("utf8")
        )
        Thread(
            target=handle_client,
            args=(
                client,
                BUF_SIZE,
                client_list,
                name_to_client_list,
            ),
            daemon=True,
        ).start()


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
            return enter_host()

        return host

    def enter_port():
        port = input("PORT: ")
        if port.isnumeric() is False or int(port) > 65535:
            print("Port is a number from 1 to 65535")
            return enter_port()

        return int(port)

    SERVER.bind((enter_host(), enter_port()))


if __name__ == "__main__":
    main()

SERVER.close()
