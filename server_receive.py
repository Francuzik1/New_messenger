import json


def handle_client(client, BUF_SIZE, client_list, name_to_client_list):
    # del client_list
    def broadcast(msg_q):
        for sock in name_to_client_list.values():
            sock.send(msg_q)

    def connection_for_new_name(update_client_list, update_name_to_client_list):
        new_name = client.recv(BUF_SIZE).decode("utf8")
        update_client_list.append(new_name)
        update_name_to_client_list[new_name] = client
        broadcast(
            json.dumps({"type": "new_client_list", "msg": update_client_list}).encode()
        )
        return new_name

    name = connection_for_new_name(client_list, name_to_client_list)
    print(client_list, name_to_client_list)

    while True:
        try:
            msg = client.recv(BUF_SIZE).decode("utf8")
            msg = json.loads(msg)
            print(msg)

            for i in msg["to"]:
                name_to_client_list[i].send(json.dumps(msg).encode("utf8"))

            # add file_name
            if msg["file_size"] is not None:
                file_size = int(msg["file_size"])
                while file_size > 0:
                    files_data = client.recv(BUF_SIZE)
                    for i in msg["to"]:
                        name_to_client_list[i].send(files_data)
                    file_size -= BUF_SIZE

        except Exception as e:
            print(f"[!] Error: {e}")
            client_list.remove(name)
            del name_to_client_list[name]
            to_send = json.dumps({"type": "new_client_list", "msg": client_list})
            broadcast(to_send.encode())
            client.close()
            break
