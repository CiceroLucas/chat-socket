import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 5000         # Porta que o servidor irá escutar

# Lista para armazenar os clientes conectados e seus nomes de usuário
clients = []
usernames = {}

# Função para broadcast de mensagens para todos os clientes
def broadcast(message):
    for client in clients:
        client.send(message)

# Função para lidar com clientes individuais
def handle_client(client):
    try:
        # Recebe o nome de usuário inicial
        username = client.recv(1024).decode('utf-8')
        usernames[client] = username
        welcome_message = f"{username} entrou no chat!".encode('utf-8')
        print(welcome_message.decode('utf-8'))
        broadcast(welcome_message)

        while True:
            message = client.recv(1024)
            if message:
                decoded_message = message.decode('utf-8')

                if decoded_message.startswith('/nome'):
                    old_username = usernames[client]
                    new_username = decoded_message.split(' ', 1)[1]
                    usernames[client] = new_username
                    name_change_message = f"{old_username} alterou seu nome para {new_username}".encode('utf-8')
                    print(name_change_message.decode('utf-8'))
                    broadcast(name_change_message)

                elif decoded_message.startswith('/cutucar'):
                    target_username = decoded_message.split(' ', 1)[1]
                    poke_user(client, target_username)

                else:
                    full_message = f"{usernames[client]}: {decoded_message}".encode('utf-8')
                    print(full_message.decode('utf-8'))
                    broadcast(full_message)
            else:
                remove_client(client)
                break
    except:
        remove_client(client)

# Nova função para cutucar um usuário
def poke_user(client, target_username):
    found = False
    for c, name in usernames.items():
        if name == target_username:
            poke_message = f"{usernames[client]} te cutucou!".encode('utf-8')
            c.send(poke_message)
            found = True
            break
    
    if not found:
        client.send(f"Usuário {target_username} não encontrado.".encode('utf-8'))

def remove_client(client):
    if client in clients:
        clients.remove(client)
        leave_message = f"{usernames[client]} saiu do chat.".encode('utf-8')
        print(leave_message.decode('utf-8'))
        broadcast(leave_message)
        client.close()
        del usernames[client]

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Conexão estabelecida com {str(address)}")

        client.send("NOME".encode('utf-8'))
        threading.Thread(target=handle_client, args=(client,)).start()
        clients.append(client)

if __name__ == "__main__":
    receive_connections()
