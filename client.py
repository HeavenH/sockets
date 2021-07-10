import sys
import socket
import threading

if(len(sys.argv) < 3 or not(sys.argv[2].isnumeric())):
    print('usage: client [host] [port]')
    sys.exit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((str(sys.argv[1]), int(sys.argv[2])))


def receive():
    while (True):
        try:
            msg = client.recv(1024).decode('utf-8')
            print(msg)
        except:
            print('Something went wrong...')
            client.close()
            break


def send():
    while(True):
        msg = input("")
        if(msg != ""):
            client.send(msg.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

send_thread = threading.Thread(target=send)
send_thread.start()
