import sys
import socket
import threading

if(len(sys.argv) < 2 or not(sys.argv[1].isnumeric())):
    print('usage: server [port]')
    sys.exit()

host = '127.0.0.1'
port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for c in clients:
        c.send(message)


def handleMsg(c):
    while (True):
        try:
            msg = c.recv(1024).decode('utf-8')

            if (msg.strip()):
                broadcast(
                    f'{nicknames[clients.index(c)]}: {msg}'.encode('utf-8'))
        except:
            index = clients.index(c)
            clients.remove(c)
            c.close()
            nick = nicknames[index]
            broadcast(f'{nick} left...'.encode('utf-8'))
            nicknames.remove(nick)
            break


def main():
    while (True):
        try:
            client, address = server.accept()
            nick = str(address)
            nicknames.append(nick)
            clients.append(client)

            print(f'{str(address)} connected')
            broadcast(f'{nick} joined the chat\n'.encode('utf-8'))
            client.send('Connected to the room'.encode('utf-8'))

            thread = threading.Thread(target=handleMsg, args=(client,))

            thread.start()
        except:
            server.close()


print('Server running...')
main()
