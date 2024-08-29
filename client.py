import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def start_client(host='127.0.0.1', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # Enviar nickname
    nickname = input("Enter your nickname: ")
    client_socket.send(nickname.encode('utf-8'))

    # Iniciar thread para receber mensagens
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        try:
            message = input()
            if message:
                client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            break

    client_socket.close()

if __name__ == "__main__":
    start_client()
