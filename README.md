# chat-socket# Chat com Sockets em Python

Este projeto implementa um chat simples utilizando sockets em Python. O sistema inclui um servidor e um cliente. Os usuários podem trocar mensagens, trocar nicknames, e cutucar uns aos outros. O servidor gerencia as conexões e as mensagens, e notifica todos os usuários sobre eventos importantes, como a entrada e saída de usuários.

## Funcionalidades

- **Envio de Mensagens**: Usuários podem enviar mensagens para todos os participantes do chat.
- **Troca de Nickname**: Usuários podem alterar seu nickname a qualquer momento.
- **Cutucar Usuários**: Usuários podem cutucar outros usuários, e todos são notificados sobre isso.
- **Notificações de Entrada/Saída**: O servidor notifica todos os usuários quando alguém entra ou sai do chat.

## Requisitos

- Python 3.x

## Instalação

1. **Clone o Repositório**

   ```sh
   git clone https://github.com/CiceroLucas/chat-socket.git
   cd chat-socket
# Execução

Abra um terminal e crie um ambiente virtual com o seguinte comando:

```
py -m venv venv
```
Inicie o ambiente virtual com o seguinte comando:
```
source venv/Scripts/Activate
```

Instale as dependências com o seguinte comando:
```
pip install -r requirements.txt 
```

Inicie o servidor
```
py server.py
```

Inicie o cliente
```
py client.py
```

# Comandos do Cliente

* Enviar Mensagem: Envie uma mensagem para todos os usuários conectados.
```
!sendmsg sua mensagem aqui
```

* Trocar Nickname: Altere seu nickname para um novo nome.
```
!changenickname novo_nickname
```

* Cutucar Outro Usuário: Envie uma cutucada para outro usuário.
```
!poke nickname_do_usuario
```
