import socket
import threading

# Configurações do cliente
HOST = '127.0.0.1'  # Deve ser o mesmo do servidor
PORT = 5000         # Deve ser o mesmo do servidor

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NOME':
                client.send(username.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ocorreu um erro ao receber a mensagem.")
            client.close()
            break

def send_messages(client):
    while True:
        message = input()
        client.send(message.encode('utf-8'))

if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    username = input("Digite seu nome de usuário: ")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()
