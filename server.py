import socket
import threading

clients = {}
lock = threading.Lock()

def broadcast(message, sender_nickname):
    with lock:
        for nickname, client_socket in clients.items():
            if nickname != sender_nickname:
                try:
                    client_socket.send(message)
                except:
                    client_socket.close()
                    del clients[nickname]

def handle_client(client_socket, address):
    global clients
    
    try:
        # Receber o nickname do cliente
        client_socket.send(b"Please provide your nickname: ")
        nickname = client_socket.recv(1024).decode('utf-8').strip()

        if not nickname:
            client_socket.send(b"Nickname is required. Disconnecting...")
            client_socket.close()
            return

        with lock:
            clients[nickname] = client_socket

        # Informar a todos sobre o novo usuário
        broadcast(f"[{nickname}] has joined the chat.".encode('utf-8'), nickname)
        send_user_list(client_socket)

        while True:
            try:
                # Receber e processar mensagens dos clientes
                message = client_socket.recv(1024).decode('utf-8').strip()
                if not message:
                    break

                command = message.split(' ', 1)
                if len(command) > 1:
                    action = command[0]
                    content = command[1]
                else:
                    action = command[0]
                    content = ""

                dispatch_action(action, content, nickname, client_socket)

            except ConnectionResetError:
                break

    finally:
        handle_disconnection(nickname)

def dispatch_action(action, content, nickname, client_socket):
    actions = {
        '!sendmsg': lambda msg: handle_sendmsg(msg, nickname),
        '!poke': lambda target: handle_poke(target, nickname),
        '!changenickname': lambda new_nick: handle_changenickname(new_nick, nickname, client_socket),
    }

    action_function = actions.get(action, handle_unknown_command)
    action_function(content)

def handle_sendmsg(message, nickname):
    broadcast(f"[{nickname}]: {message}".encode('utf-8'), nickname)

def handle_poke(target_nickname, nickname):
    if target_nickname in clients:
        clients[target_nickname].send(f"[{nickname}]: poked you".encode('utf-8'))
        broadcast(f"{nickname} poked {target_nickname}".encode('utf-8'), nickname)
    else:
        clients[nickname].send(f"User {target_nickname} not found.".encode('utf-8'))

def handle_changenickname(new_nickname, old_nickname, client_socket):
    with lock:
        if new_nickname in clients:
            client_socket.send(f"Nickname {new_nickname} already in use.".encode('utf-8'))
        else:
            del clients[old_nickname]
            clients[new_nickname] = client_socket
            client_socket.send(f"Nickname changed to {new_nickname}.".encode('utf-8'))
            broadcast(f"! changenickname {old_nickname} {new_nickname}".encode('utf-8'), new_nickname)

def handle_unknown_command(_):
    pass

def handle_disconnection(nickname):
    with lock:
        if nickname in clients:
            del clients[nickname]
            broadcast(f"! msg {nickname} has left the chat.".encode('utf-8'))

def send_user_list(client_socket):
    with lock:
        users_list = " ".join(clients.keys())
        client_socket.send(f"Users currently online: {users_list}".encode('utf-8'))

def start_server(host='0.0.0.0', port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
