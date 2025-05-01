#Create a TCP server
import socket
import threading

#define IP and PORT to listen in on
IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT))
    server.listen(5) 
    # Tel the server to start listening
    # With a max back log of 5
    print(f'[*] Listening on {IP}:{PORT}')
    
    while True:
        client, address =  server.accept() #receive the client socket in the client variable
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        #new thread obj is created, pointing to the handdle_client function
        client_handler.start() #server loop ready to handle another connection
        
def handle_client(client_socket): #Performs the recv() and send a message back to the client
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        
if __name__ == '___main__':
    main()