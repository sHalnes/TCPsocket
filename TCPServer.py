from socket import *
from threading import Thread
from time import strftime


'''This is the server side socket with simple authorization'''

class TCPServer(object):

    def __init__(self, host, port):
        #Initializing an object of the class with host name and port number and creating a server socket

        self.server_host = host
        self.server_port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        # in setsockopt(): SO_REUSEADDR allows us to reuse a lockal socket in TIME_WAIT state (after previous execution)
        # 1 stays for buffer size
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_host, self.server_port))

    def listen_all(self):

        # Listen to new connections to server. Creates new thread for a new connection only
        # if authorization was successfull.

        self.server_socket.listen(4)
        while True:
            client, address = self.server_socket.accept()
            print('New connection from {ip} just started'.format(ip=address))
            # some authorization when client connects to the server
            try:
                password = client.recv(1024).decode()
                if password == '123456':
                    client.send('Access allowed'.encode())
                    # Open new thread for new authorized client
                    new_thread = Thread(target=self.run, args=(client, address))
                    new_thread.start()
                else:
                    print('Access denied. Connection with {ip} is closed.'.format(ip=address))
                    client.send('Access denied'.encode())
                    client.close()
            except:
                print('Client\'s query is of wrong type or client disconnected.')

    def run(self, client, address):
        # Run the thread for one client

        expected_data = ['FULL', 'DATE', 'TIME', 'CLOSE'] # this will allow us to prevent irrelevant query

        while True:
            try:
                data = client.recv(1024).decode()
                response = ''
                if data and data in expected_data:
                    print('Message from {addr}: {msg}'.format(addr=address, msg=data))
                    # Set the response to client
                    if data == 'FULL':
                        response = strftime('%B %Y %X').lower()
                    elif data == 'DATE':
                        response = strftime('%B %Y').lower()
                    elif data == 'TIME':
                        response = strftime('%X')
                    elif data == 'CLOSE':
                        response = 'close session'
                    print('Response to {ip} : {rsp}'.format(ip=address, rsp=response))
                    client.send(response.encode())
                    if response == 'close session':
                        print('Connection with {ip} is off now'.format(ip=address))
                        client.close()

                else:
                    print('Client\'s query is of wrong type or client disconnected')
            except:
                client.close()
                return False


if __name__ == "__main__":
    port_num = 65535 # An arbitrary non-privileged port
    TCPServer('',port_num).listen_all()
