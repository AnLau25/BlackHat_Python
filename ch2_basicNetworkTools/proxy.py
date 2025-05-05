#technicaly, wireshark for when u don't have accces (tcp proxy)
import sys
import socket
import threading

HEX_FILTER = ''.join(
    [(len(repr(chr(i)))==3) and chr(i) or '.' for i in range(256)] #If length == 3, get char, else, '.'
)#String containing ASCII printable characters.
 #If not printable, print dot

def hexdump(src, length=16,show=True): #Displays coms between local and remote machines
    if isinstance(src,bytes):
        src = src.decode() #Decodes if any byte was passed
    
    results = list()
    
    for i in range(0, len(src),length): #Grabs pieces of the decode and places it in word
        word = str(src[i:i+length])
        
        printable = word.translate(HEX_FILTER) #Substitutes the strings by the raw printable, via .translate()
        hexa = ''.join([f'{ord(c):02X}' for c in word]) #Substitutes the raw printable by hex
        hexwidth =  length*3 
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')#New array containg the hex value of the first index, the hex value of the word and the word 
    if show:
        for line in results:
            print(line)
    else:
        return results
    #Usefull to find user credentials in plain text protocol and understanding unkown protocols
    
#receives local and remote data
def receive_from (connection):
    buffer = b"" #empty byte string, responces from socket
    connection.settimeout(5) #default, but can be modified based on need
    try:
        while True: #Loop to read data
            data = connection.recv(4096)
            if not data: #Until no more data or time out
                break
            buffer += data
    except Exception as e:
        pass
    return buffer #returns to remote or local caller
 
#To modify response/requests before proxy sends them   
def request_handler(buffer):
    #client modifs here
    return buffer
        
def response_handler(buffer):
    #client modifs here
    return buffer

#main logic
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #connect remote to host
    remote_socket.connect((remote_host, remote_port))
    
    #ensure we do not need a previous connection of handdling
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    
    #1, 2 and 3 but if there is data to be received first
    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." %len(remote_buffer))
        client_socket.send(remote_buffer)
    
    while True: #Goes on until there is no more data to read on either side of the connection
        #1. 𝘳𝘦𝘤𝘦𝘪𝘷𝘦_𝘧𝘳𝘰𝘮() is tried on both sides of the communication
        #2. h𝘦𝘹𝘥𝘶𝘮𝘱() the content of both packets to check for anything interesting
        #3. send received buffer to the respective reiver. Ie. client → remote, remote → client
        
        local_buffer = receive_from(client_socket) #1
        if len(local_buffer):    
            line = print("[==>] Received %d bytes from localhost." %len(local_buffer))
            print(line)
            hexdump(local_buffer)#2
    
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)#3
            print("[==>] Send to remote")
        
        remote_buffer =  receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." %len(remote_buffer))
            hexdump(remote_buffer)
            
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Send to localhost")
            
        if not(len(local_buffer)) or not(len(remote_buffer)):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections")
            break
                
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates socket
    
    try:
        server.bind((local_host, local_port)) #binds to the local host
    except Exception as e:
        print('problemon bind: %r' %e) 
        print("[!!] Failed to listen on %s:%d" %(local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        sys.exit(0)
    
    print("[*] Listening on %s:%d" %(local_host, local_port))
    server.listen(5) #listens
    
    while True: #threads 𝘱𝘳𝘰𝘹𝘺_𝘩𝘢𝘯𝘥𝘭𝘦𝘳() to catch packets at either side of the data stream
        client_socket, addr = server.accept()
        
        #printout local connection info
        line = "> Received incoming connection from %s:%d" %(addr[0], addr[1])
        print(line)
        
        #start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target = proxy_handler,
            args = (client_socket, remote_host, remote_port, receive_first)
        )
        
        proxy_thread.start()
                
if __name__ == "__main__":
    hexdump("python is a language\n and Aston is a car\n")

#some server deamons expect you to request data first, FTP for example, sends a banner first
