from socket import *

'''This is the client side socket with simple authorization.
In the first message to the server the client socket sends password and waiting for responce. If access is allowed
the socket can send messages like 'full', 'date' etc. If access denied the connection will stop.
Socket will keep connection on and allow user to send/get several messeges to/from server.
'''

def run_connection(client_socket):
    password = '123456'
    # or if you want you can type in the password:
    # password = input('Type in password')

    expected_input = ['FULL', 'DATE', 'TIME',
                      'CLOSE']  # we limit user input to prevent unexpected behaviour of the server

    # Sending password to connect with server socket
    client_socket.send(password.encode())
    server_answer = client_socket.recv(1024).decode()
    if server_answer == 'Access denied':
        print('Access denied. The password is incorrect')
        client_socket.close()
    else:
        print(server_answer)
        connecting_on = True
        while connecting_on:
            message = input('Input your mesage [FULL, DATE, TIME or CLOSE] >> ').upper()
            print('Your message: ', message)
            if message in expected_input:
                client_socket.send(message.encode())
                server_response = client_socket.recv(1024).decode()
                print('Response from server: ', server_response)
                if server_response == 'close session':
                    print('connecting off')
                    connecting_on = False
                    client_socket.close()
            else:
                print('Input is incorrect. Try better.')


if __name__ == "__main__":

    server_name = 'localhost'
    server_port = 65535
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect((server_name, server_port))  # connects to the destination address and port
        run_connection(client_socket)
    except:
        print('Can not connect to the server')
